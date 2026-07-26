import io
import json
import traceback
import os
import pandas as pd
import chardet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q, Count
from django.db import models, IntegrityError

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ChatSession, ChatMessage, UserProfile, Workspace, Dataset, FileCategory, DatasetTag, DatasetVersion
from .serializers import UserProfileSerializer, UserSerializer, WorkspaceSerializer, DatasetSerializer, FileCategorySerializer, DatasetTagSerializer, DatasetVersionSerializer
from analytics.analyzer import (
    load_csv, prepare_dataframe, dataset_summary, column_info, evaluate_business,
    analyze_numeric_trends, compute_correlations, detect_industry,
    get_business_context, detect_critical_variables, detect_anomalies,
    check_fraud_signals, simple_forecast, get_chart_data, get_preview, get_kpis
)
from analytics.utils import make_json_safe
from ai.llm import generate_ai_report, chat_with_data

User = get_user_model()

# Constants
ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'json']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Workspace.objects.create(owner=instance, name=f"Espacio de trabajo de {instance.email}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


def test_endpoint(request):
    return JsonResponse({"status": "ok", "message": "La API esta operativa"})


class MemoryManager:
    RECENT_MESSAGE_LIMIT = 8
    RELEVANT_MESSAGE_LIMIT = 3
    SUMMARY_MESSAGE_LIMIT = 10
    MAX_SUMMARY_CHARS = 1500
    MAX_DECISIONS = 5
    MAX_DATASETS = 3
    MAX_CONTEXT_TOTAL_CHARS = 12000

    def _get_session(self, session_id: str) -> ChatSession:
        session, _ = ChatSession.objects.get_or_create(session_id=session_id)
        return session

    def add_message(self, session_id: str, role: str, content: str):
        session = self._get_session(session_id)
        ChatMessage.objects.create(session=session, role=role, content=content)
        if role == "user" and (not session.title or session.title in ["Nueva sesión", "Nuevo chat"]):
            session.title = content[:40] if len(content) > 40 else content
            session.save(update_fields=["title", "updated_at"])

    def store_dataset_context(self, session_id: str, context: dict):
        session = self._get_session(session_id)
        session.dataset_context = context or {}
        dataset_history = list(session.dataset_history or [])
        file_name = context.get("file_name", "dataset")
        snapshot = {
            "file_name": file_name,
            "rows": context.get("summary", {}).get("rows", 0),
            "columns": context.get("summary", {}).get("columns", 0),
        }
        if not dataset_history or dataset_history[-1] != snapshot:
            dataset_history.append(snapshot)
        session.dataset_history = dataset_history[-self.MAX_DATASETS:]
        session.save(update_fields=["dataset_context", "dataset_history", "updated_at"])

    def get_dataset_context(self, session_id: str) -> dict:
        session = self._get_session(session_id)
        return session.dataset_context or {}

    def get_history(self, session_id: str, question: str = "") -> str:
        session = self._get_session(session_id)
        messages = list(session.messages.all()[:20])
        history_parts = []
        for msg in messages:
            history_parts.append(f"{msg.role.upper()}: {msg.content}")
        return "\n".join(history_parts)


memory = MemoryManager()


def validate_file(file_obj):
    """Validar archivo: tamaño, formato, integridad, codificación, estructura"""
    errors = []
    
    # 1. Validar tamaño
    if file_obj.size > MAX_FILE_SIZE:
        errors.append(f"El archivo excede el tamaño máximo permitido de {MAX_FILE_SIZE / (1024*1024)} MB")
    
    # 2. Validar formato
    filename = file_obj.name.lower()
    file_type = None
    if filename.endswith('.csv'):
        file_type = 'csv'
    elif filename.endswith('.xlsx'):
        file_type = 'xlsx'
    elif filename.endswith('.json'):
        file_type = 'json'
    else:
        errors.append(f"Formato de archivo no permitido. Usa: {', '.join(ALLOWED_FILE_TYPES)}")
    
    if errors:
        return False, errors, file_type
    
    # 3. Validar integridad y estructura
    try:
        file_obj.seek(0)
        if file_type == 'csv':
            # Detectar codificación
            raw_data = file_obj.read(10000)
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
            file_obj.seek(0)
            
            # Cargar CSV para validar estructura
            df = pd.read_csv(file_obj, encoding=encoding, nrows=100)
            if df.empty:
                errors.append("El archivo CSV está vacío")
            if len(df.columns) == 0:
                errors.append("El archivo CSV no tiene columnas")
                
        elif file_type == 'xlsx':
            df = pd.read_excel(file_obj, nrows=100)
            if df.empty:
                errors.append("El archivo Excel está vacío")
            if len(df.columns) == 0:
                errors.append("El archivo Excel no tiene columnas")
                
        elif file_type == 'json':
            file_obj.seek(0)
            data = json.load(file_obj)
            if not data:
                errors.append("El archivo JSON está vacío")
                
    except pd.errors.EmptyDataError:
        errors.append("El archivo está vacío")
    except pd.errors.ParserError:
        errors.append("Error al parsear el archivo. Verifica la estructura")
    except json.JSONDecodeError:
        errors.append("Error al parsear el JSON. Verifica la sintaxis")
    except Exception as e:
        errors.append(f"Error de integridad: {str(e)}")
    
    return len(errors) == 0, errors, file_type


def get_analytics_context(file_obj, filename):
    df = load_csv(file_obj)
    df, cleaning_info = prepare_dataframe(df)
    summary = dataset_summary(df)
    cols = column_info(df)
    health = evaluate_business(summary)
    trends = analyze_numeric_trends(df)
    correlations = compute_correlations(df)
    industry = detect_industry(df)
    business_context = get_business_context(df, industry)
    critical_variables = detect_critical_variables(df)
    anomalies = detect_anomalies(df)
    fraud_signals = check_fraud_signals(df)
    numeric_cols = df.select_dtypes(include=['number']).columns
    forecasts = {}
    for col in numeric_cols[:2]:
        try:
            f = simple_forecast(df, col)
            if f:
                forecasts[col] = f
        except Exception as e:
            pass
    charts = get_chart_data(df)
    preview = get_preview(df)
    kpis = get_kpis(df)
    return {
        "file_name": filename,
        "cleaning": cleaning_info,
        "summary": summary,
        "columns": cols,
        "health": health,
        "trends": trends,
        "correlations": correlations,
        "charts": charts,
        "preview": preview,
        "kpis": kpis,
        "industry": industry,
        "business_context": business_context,
        "critical_variables": critical_variables,
        "anomalies": anomalies,
        "fraud_signals": fraud_signals,
        "forecasts": forecasts
    }


@csrf_exempt
def analyze_endpoint(request):
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No se ha subido ningún archivo"}, status=400)
        file = request.FILES['file']
        session_id = request.POST.get('session_id', 'default')
        session = memory._get_session(session_id)
        session.messages.all().delete()
        memory.add_message(session_id, "user", f"Archivo cargado: {file.name}")
        try:
            suffix = file.name.lower().split('.')[-1]
            if suffix not in ['csv', 'xlsx', 'xls', 'pdf', 'docx', 'doc']:
                return JsonResponse({"status": "rag_only", "file_name": file.name, "response": "Archivo cargado."})
            if suffix in ['pdf', 'docx', 'doc']:
                response_text = f"El archivo '{file.name}' fue cargado correctamente. El análisis detallado está disponible para archivos CSV y Excel. Para este tipo de archivo ({suffix.upper()}), por ahora solo se almacena."
                memory.add_message(session_id, "assistant", response_text)
                return JsonResponse({"status": "rag_only", "file_name": file.name, "response": response_text})
            file.seek(0)
            context = get_analytics_context(file, file.name)
            safe_context = make_json_safe(context)
            memory.store_dataset_context(session_id, safe_context)
            ai_report = generate_ai_report(safe_context)
            score = safe_context.get('health', {}).get('health_score', 0)
            message_parts = [
                f"¡Listo! Ya terminé de revisar tu archivo '{safe_context['file_name']}'.\n\nHe detectado que tu negocio pertenece al sector de {safe_context.get('industry', 'General / Negocios')}.\nAnalicé un total de {safe_context.get('summary', {}).get('rows', 0)} filas de información.\nEn cuanto a la salud de tus datos, les doy una puntuación de {score:.0f} sobre 100 (un nivel de riesgo {safe_context.get('health', {}).get('risk_level', 'desconocido').lower()})."
            ]
            if ai_report:
                message_parts.append(f"\n\n📝 Resumen Ejecutivo para ti:\n{ai_report}")
            full_response = "\n".join(message_parts)
            memory.add_message(session_id, "assistant", full_response)
            safe_context["response"] = full_response
            return JsonResponse(safe_context)
        except Exception as e:
            err = f"Error al analizar el archivo: {str(e)}"
            print(f"[ERROR] CRASH EN ANALISIS: {err}")
            traceback.print_exc()
            return JsonResponse({"error": err, "exception": type(e).__name__, "detail": repr(e), "response": err}, status=500)
    return JsonResponse({"error": "Se requiere una petición POST"}, status=400)


@csrf_exempt
def chat_endpoint(request):
    if request.method == "POST":
        try:
            data = json.load(request)
            message = (data.get("message", "") or "").strip()
            session_id = data.get("session_id", "default")
            if not message:
                return JsonResponse({"error": "El mensaje no puede estar vacío."}, status=400)
            memory.add_message(session_id, "user", message)
            history = memory.get_history(session_id, message)
            context = memory.get_dataset_context(session_id)
            response_text = chat_with_data(message, context, history)
            memory.add_message(session_id, "assistant", response_text)
            return JsonResponse({"response": response_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Se requiere una petición POST"}, status=400)


@csrf_exempt
def list_sessions(request):
    if request.method == "GET":
        sessions = ChatSession.objects.all().order_by('-updated_at')
        session_data = [
            {
                "session_id": s.session_id,
                "title": s.title,
                "updated_at": s.updated_at.isoformat(),
            }
            for s in sessions
        ]
        return JsonResponse({"sessions": session_data})
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def get_session_history(request, session_id):
    if request.method == "GET":
        session, _ = ChatSession.objects.get_or_create(session_id=session_id)
        messages = session.messages.filter(role__in=['user', 'assistant']).order_by('created_at')
        message_data = [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ]
        return JsonResponse({
            "session_id": session.session_id,
            "title": session.title,
            "dataset_context": session.dataset_context,
            "messages": message_data,
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def rename_session(request, session_id):
    if request.method == "PUT":
        try:
            data = json.load(request)
            new_title = data.get("title", "").strip()
            if not new_title:
                return JsonResponse({"error": "El título no puede estar vacío"}, status=400)
            session = ChatSession.objects.get(session_id=session_id)
            session.title = new_title
            session.save(update_fields=["title", "updated_at"])
            return JsonResponse({"status": "ok", "title": session.title})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesión no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def delete_session(request, session_id):
    if request.method == "DELETE":
        try:
            session = ChatSession.objects.get(session_id=session_id)
            session.delete()
            return JsonResponse({"status": "ok", "message": "Sesión eliminada correctamente"})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesión no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        user_data = data.pop('user', None)
        
        profile_serializer = UserProfileSerializer(profile, data=data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            
            if user_data:
                user_serializer = UserSerializer(request.user, data=user_data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
            
            return Response(UserProfileSerializer(profile).data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_workspace(request):
    workspace, created = Workspace.objects.get_or_create(owner=request.user, defaults={'name': f"Espacio de trabajo de {request.user.email}"})
    if request.method == 'GET':
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Dataset Endpoints
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dataset_list_create(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        file_type = request.query_params.get('type', '')
        status_filter = request.query_params.get('status', '')
        category_id = request.query_params.get('category', '')
        starred = request.query_params.get('starred', '')
        sort = request.query_params.get('sort', '-uploaded_at')
        
        datasets = Dataset.objects.filter(workspace=workspace)
        
        archived = request.query_params.get('archived', '')
        if archived == 'true':
            datasets = datasets.filter(archived=True)
        else:
            datasets = datasets.filter(archived=False)
        
        if search:
            datasets = datasets.filter(
                Q(file_name__icontains=search) | 
                Q(original_name__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        if file_type:
            datasets = datasets.filter(file_type=file_type)
        if status_filter:
            datasets = datasets.filter(status=status_filter)
        if category_id:
            datasets = datasets.filter(category_id=category_id)
        if starred == 'true':
            datasets = datasets.filter(starred=True)

        allowed_sorts = ['uploaded_at', '-uploaded_at', 'file_name', '-file_name', 'file_size', '-file_size']
        if sort in allowed_sorts:
            datasets = datasets.order_by(sort)
        
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({"error": "No se ha subido ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        # Validar archivo
        is_valid, errors, file_type = validate_file(file)
        file.seek(0)
        
        # Crear dataset
        file_hash = Dataset.compute_file_hash_static(file)
        file.seek(0)

        existing = Dataset.objects.filter(file_hash=file_hash, workspace=workspace).first()
        if existing:
            serializer = DatasetSerializer(existing)
            return Response(
                {"error": "Ya existe un archivo idéntico en tu workspace", "existing": serializer.data},
                status=status.HTTP_409_CONFLICT
            )

        dataset = Dataset(
            file=file,
            original_name=file.name,
            file_name=file.name,
            file_size=file.size,
            file_type=file_type or 'unknown',
            uploaded_by=request.user,
            workspace=workspace,
            status='valid' if is_valid else 'invalid',
            validation_errors=errors
        )
        try:
            dataset.save()
        except IntegrityError:
            serializer = DatasetSerializer(existing) if existing else None
            return Response(
                {"error": "Ya existe un archivo idéntico en tu workspace"},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": f"Error al guardar el archivo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Si es válido, analizarlo
        if is_valid and file_type in ['csv', 'xlsx']:
            try:
                file.seek(0)
                context = get_analytics_context(file, file.name)
                dataset.analysis_context = make_json_safe(context)
                dataset.status = 'valid'
                dataset.save()
            except Exception as e:
                dataset.status = 'invalid'
                dataset.validation_errors.append(f"Error en análisis: {str(e)}")
                dataset.save()
        
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    elif request.method in ('PUT', 'PATCH'):
        if 'file_name' in request.data:
            dataset.file_name = request.data['file_name']
        if 'description' in request.data:
            dataset.description = request.data['description']
        if 'tags' in request.data:
            dataset.tags = request.data['tags']
        if 'starred' in request.data:
            dataset.starred = request.data['starred']
        if 'category' in request.data:
            cat_id = request.data['category']
            if cat_id:
                try:
                    dataset.category = FileCategory.objects.get(pk=cat_id, workspace=workspace)
                except FileCategory.DoesNotExist:
                    return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
            else:
                dataset.category = None
        dataset.save()
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if dataset.file:
            dataset.file.delete(save=False)
        dataset.delete()
        return Response({"status": "ok", "message": "Dataset eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_activate(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    session_id = request.data.get('session_id', 'default')
    session, _ = ChatSession.objects.get_or_create(session_id=session_id, user=request.user, workspace=workspace)
    
    session.dataset = dataset
    session.dataset_context = dataset.analysis_context
    session.save()
    
    return Response({"status": "ok", "message": "Dataset activado correctamente"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_rename(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    new_name = request.data.get('file_name', '').strip()
    if not new_name:
        return Response({"error": "El nombre no puede estar vacío"}, status=status.HTTP_400_BAD_REQUEST)

    dataset.file_name = new_name
    dataset.save(update_fields=['file_name', 'updated_at'])
    return Response(DatasetSerializer(dataset).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_bulk_delete(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    ids = request.data.get('ids', [])
    if not ids:
        return Response({"error": "No se proporcionaron IDs"}, status=status.HTTP_400_BAD_REQUEST)

    datasets = Dataset.objects.filter(pk__in=ids, workspace=workspace)
    count = datasets.count()
    for ds in datasets:
        if ds.file:
            ds.file.delete(save=False)
    datasets.delete()
    return Response({"status": "ok", "deleted": count})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_move(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    category_id = request.data.get('category_id')
    if category_id:
        try:
            category = FileCategory.objects.get(pk=category_id, workspace=workspace)
            dataset.category = category
        except FileCategory.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    else:
        dataset.category = None

    dataset.save(update_fields=['category', 'updated_at'])
    return Response(DatasetSerializer(dataset).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_toggle_star(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    dataset.starred = not dataset.starred
    dataset.save(update_fields=['starred', 'updated_at'])
    return Response({"starred": dataset.starred})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_stats(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    datasets = Dataset.objects.filter(workspace=workspace)

    total = datasets.count()
    by_type = {}
    for ds in datasets.values('file_type').annotate(count=models.Count('id')):
        by_type[ds['file_type']] = ds['count']

    by_status = {}
    for ds in datasets.values('status').annotate(count=models.Count('id')):
        by_status[ds['status']] = ds['count']

    total_size = sum(ds.file_size for ds in datasets)
    starred = datasets.filter(starred=True).count()

    return Response({
        "total": total,
        "by_type": by_type,
        "by_status": by_status,
        "total_size": total_size,
        "starred": starred,
    })


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)

    if request.method == 'GET':
        categories = FileCategory.objects.filter(workspace=workspace)
        serializer = FileCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get('name', '').strip()
        color = request.data.get('color', '#6366f1')
        if not name:
            return Response({"error": "El nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        cat, created = FileCategory.objects.get_or_create(
            name=name, workspace=workspace, defaults={'color': color}
        )
        return Response(FileCategorySerializer(cat).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        cat = FileCategory.objects.get(pk=pk, workspace=workspace)
    except FileCategory.DoesNotExist:
        return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    Dataset.objects.filter(category=cat).update(category=None)
    cat.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_duplicate(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    dataset.file.seek(0)
    new_name = request.data.get('file_name', f"Copia de {dataset.file_name}")
    new_ds = Dataset(
        file=dataset.file,
        original_name=dataset.original_name,
        file_name=new_name,
        file_size=dataset.file_size,
        file_type=dataset.file_type,
        file_hash=f"{dataset.file_hash}_{uuid.uuid4().hex[:8]}",
        uploaded_by=request.user,
        workspace=workspace,
        status=dataset.status,
        validation_errors=list(dataset.validation_errors),
        analysis_context=dict(dataset.analysis_context),
        description=dataset.description,
        tags=list(dataset.tags),
        category=dataset.category,
        starred=False,
    )
    new_ds.save()
    serializer = DatasetSerializer(new_ds)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_archive(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    from django.utils import timezone
    dataset.archived = not dataset.archived
    dataset.archived_at = timezone.now() if dataset.archived else None
    dataset.save(update_fields=['archived', 'archived_at', 'updated_at'])
    return Response({"archived": dataset.archived, "archived_at": dataset.archived_at})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_reanalyze(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if dataset.file_type not in ['csv', 'xlsx']:
        return Response({"error": "Solo se pueden analizar archivos CSV y Excel"}, status=status.HTTP_400_BAD_REQUEST)

    dataset.status = 'processing'
    dataset.save(update_fields=['status'])

    try:
        dataset.file.seek(0)
        context = get_analytics_context(dataset.file, dataset.file_name)
        dataset.analysis_context = make_json_safe(context)
        dataset.status = 'valid'
        dataset.save(update_fields=['analysis_context', 'status', 'updated_at'])
    except Exception as e:
        dataset.status = 'invalid'
        dataset.validation_errors.append(f"Error en re-análisis: {str(e)}")
        dataset.save(update_fields=['status', 'validation_errors', 'updated_at'])
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(DatasetSerializer(dataset).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_download(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    from django.http import FileResponse
    try:
        dataset.file.seek(0)
        response = FileResponse(dataset.file.open('rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{dataset.file_name}"'
        return response
    except Exception:
        return Response({"error": "No se pudo descargar el archivo"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_merge(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    ids = request.data.get('dataset_ids', [])
    merge_type = request.data.get('type', 'concat')
    new_name = request.data.get('file_name', 'Dataset fusionado')
    join_column = request.data.get('join_column', '')

    if len(ids) < 2:
        return Response({"error": "Se necesitan al menos 2 datasets para fusionar"}, status=status.HTTP_400_BAD_REQUEST)

    datasets = Dataset.objects.filter(pk__in=ids, workspace=workspace)
    if datasets.count() != len(ids):
        return Response({"error": "Algunos datasets no fueron encontrados"}, status=status.HTTP_404_NOT_FOUND)

    try:
        frames = []
        for ds in datasets:
            ds.file.seek(0)
            if ds.file_type == 'csv':
                df = pd.read_csv(ds.file)
            elif ds.file_type == 'xlsx':
                df = pd.read_excel(ds.file)
            else:
                continue
            frames.append(df)

        if not frames:
            return Response({"error": "No se pudieron leer los archivos"}, status=status.HTTP_400_BAD_REQUEST)

        if merge_type == 'concat':
            merged = pd.concat(frames, ignore_index=True)
        elif merge_type == 'join' and join_column:
            merged = frames[0]
            for f in frames[1:]:
                if join_column in merged.columns and join_column in f.columns:
                    merged = merged.merge(f, on=join_column, how='left', suffixes=('', '_dup'))
                else:
                    merged = pd.concat([merged, f], ignore_index=True)
        else:
            merged = pd.concat(frames, ignore_index=True)

        import io as _io
        buffer = _io.BytesIO()
        merged.to_csv(buffer, index=False)
        buffer.seek(0)

        from django.core.files.base import ContentFile
        file_content = ContentFile(buffer.read(), name=f"{new_name}.csv")
        file_hash = hashlib.sha256(buffer.getvalue()).hexdigest()
        buffer.seek(0)
        file_size = len(buffer.getvalue())

        ds = Dataset(
            file=file_content,
            original_name=f"{new_name}.csv",
            file_name=f"{new_name}.csv",
            file_size=file_size,
            file_type='csv',
            file_hash=f"{file_hash}_{uuid.uuid4().hex[:8]}",
            uploaded_by=request.user,
            workspace=workspace,
            status='valid',
            description=f"Fusionado de {datasets.count()} datasets: {', '.join(ds.file_name for ds in datasets)}",
        )
        ds.save()

        ds.file.seek(0)
        context = get_analytics_context(ds.file, ds.file_name)
        ds.analysis_context = make_json_safe(context)
        ds.save(update_fields=['analysis_context'])

        return Response(DatasetSerializer(ds).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        traceback.print_exc()
        return Response({"error": f"Error al fusionar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def tag_list_create(request):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)

    if request.method == 'GET':
        tag_filter = request.query_params.get('tag', '')
        tags = DatasetTag.objects.filter(workspace=workspace)
        if tag_filter:
            tags = tags.filter(name__icontains=tag_filter)
        serializer = DatasetTagSerializer(tags, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get('name', '').strip()
        color = request.data.get('color', '#6366f1')
        if not name:
            return Response({"error": "El nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        tag, created = DatasetTag.objects.get_or_create(
            name=name, workspace=workspace, defaults={'color': color}
        )
        return Response(DatasetTagSerializer(tag).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tag_detail(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        tag = DatasetTag.objects.get(pk=pk, workspace=workspace)
    except DatasetTag.DoesNotExist:
        return Response({"error": "Etiqueta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    tag.datasets.clear()
    tag.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_add_tags(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    tag_ids = request.data.get('tag_ids', [])
    tag_names = request.data.get('tags', [])

    for tag_id in tag_ids:
        try:
            tag = DatasetTag.objects.get(pk=tag_id, workspace=workspace)
            dataset.tag_objects.add(tag)
        except DatasetTag.DoesNotExist:
            pass

    for name in tag_names:
        tag, _ = DatasetTag.objects.get_or_create(name=name, workspace=workspace)
        dataset.tag_objects.add(tag)

    all_tags = list(dataset.tags or [])
    for name in tag_names:
        if name not in all_tags:
            all_tags.append(name)
    dataset.tags = all_tags
    dataset.save(update_fields=['tags', 'updated_at'])

    return Response(DatasetSerializer(dataset).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_remove_tags(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    tag_ids = request.data.get('tag_ids', [])
    tag_names = request.data.get('tags', [])

    for tag_id in tag_ids:
        try:
            tag = DatasetTag.objects.get(pk=tag_id, workspace=workspace)
            dataset.tag_objects.remove(tag)
        except DatasetTag.DoesNotExist:
            pass

    current_tags = list(dataset.tags or [])
    current_tags = [t for t in current_tags if t not in tag_names]
    dataset.tags = current_tags
    dataset.save(update_fields=['tags', 'updated_at'])

    return Response(DatasetSerializer(dataset).data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dataset_versions(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        versions = DatasetVersion.objects.filter(dataset=dataset)
        serializer = DatasetVersionSerializer(versions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        note = request.data.get('note', '')
        version_num = dataset.version + 1

        dataset.file.seek(0)
        file_content = dataset.file.read()
        dataset.file.seek(0)

        from django.core.files.base import ContentFile
        new_file = ContentFile(file_content, name=f"{dataset.file_name}_v{version_num}")

        version = DatasetVersion(
            dataset=dataset,
            version_number=version_num,
            file=new_file,
            file_name=dataset.file_name,
            file_size=dataset.file_size,
            file_hash=dataset.file_hash,
            analysis_context=dict(dataset.analysis_context),
            description=dataset.description,
            tags=list(dataset.tags),
            created_by=request.user,
            note=note,
        )
        version.save()

        dataset.version = version_num
        dataset.save(update_fields=['version', 'updated_at'])

        return Response(DatasetVersionSerializer(version).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_restore_version(request, pk, version_pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        version = DatasetVersion.objects.get(pk=version_pk, dataset=dataset)
    except DatasetVersion.DoesNotExist:
        return Response({"error": "Versión no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    dataset.file = version.file
    dataset.file_name = version.file_name
    dataset.file_size = version.file_size
    dataset.file_hash = version.file_hash
    dataset.analysis_context = version.analysis_context
    dataset.description = version.description
    dataset.tags = version.tags
    dataset.version = version.version_number
    dataset.save()

    return Response(DatasetSerializer(dataset).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_explore(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    ctx = dataset.analysis_context or {}
    return Response({
        "file_name": dataset.file_name,
        "summary": ctx.get("summary", {}),
        "columns": ctx.get("columns", []),
        "preview": ctx.get("preview", []),
        "kpis": ctx.get("kpis", {}),
        "charts": ctx.get("charts", {}),
        "health": ctx.get("health", {}),
        "correlations": ctx.get("correlations", {}),
        "cleaning": ctx.get("cleaning", []),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_preview(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    n = int(request.query_params.get('rows', 10))
    try:
        dataset.file.seek(0)
        if dataset.file_type == 'csv':
            df = pd.read_csv(dataset.file)
        elif dataset.file_type == 'xlsx':
            df = pd.read_excel(dataset.file)
        else:
            return Response({"error": "Tipo de archivo no soportado"}, status=status.HTTP_400_BAD_REQUEST)

        preview = get_preview(df, n)
        return Response({"preview": preview, "total_rows": len(df), "columns": list(df.columns)})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_columns(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    cols = (dataset.analysis_context or {}).get("columns", [])
    return Response({"columns": cols})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_statistics(request, pk):
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    ctx = dataset.analysis_context or {}
    return Response({
        "summary": ctx.get("summary", {}),
        "kpis": ctx.get("kpis", {}),
        "health": ctx.get("health", {}),
        "correlations": ctx.get("correlations", {}),
        "anomalies": ctx.get("anomalies", {}),
        "trends": ctx.get("trends", {}),
    })
