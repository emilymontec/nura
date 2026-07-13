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
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ChatSession, ChatMessage, UserProfile, Workspace, Dataset
from .serializers import UserProfileSerializer, UserSerializer, WorkspaceSerializer, DatasetSerializer
from analytics.analyzer import (
    load_csv, dataset_summary, column_info, evaluate_business,
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
            return JsonResponse({"error": err, "exception": type(e).__name__, "detail": repr(e)}, status=500)
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
    """Listar datasets o subir uno nuevo"""
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    if request.method == 'GET':
        # Búsqueda y filtrado
        search = request.query_params.get('search', '')
        file_type = request.query_params.get('type', '')
        status_filter = request.query_params.get('status', '')
        
        datasets = Dataset.objects.filter(workspace=workspace)
        
        if search:
            datasets = datasets.filter(
                Q(file_name__icontains=search) | 
                Q(original_name__icontains=search)
            )
        if file_type:
            datasets = datasets.filter(file_type=file_type)
        if status_filter:
            datasets = datasets.filter(status=status_filter)
        
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
        dataset.save()
        
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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, pk):
    """Obtener, renombrar o eliminar un dataset"""
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Renombrar
        new_name = request.data.get('file_name')
        if new_name:
            dataset.file_name = new_name
            dataset.save()
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Eliminar archivo físico y registro
        if dataset.file:
            dataset.file.delete(save=False)
        dataset.delete()
        return Response({"status": "ok", "message": "Dataset eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dataset_activate(request, pk):
    """Activar un dataset para una sesión de chat"""
    workspace, _ = Workspace.objects.get_or_create(owner=request.user)
    
    try:
        dataset = Dataset.objects.get(pk=pk, workspace=workspace)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    session_id = request.data.get('session_id', 'default')
    session, _ = ChatSession.objects.get_or_create(session_id=session_id, user=request.user, workspace=workspace)
    
    # Activar dataset en la sesión
    session.dataset = dataset
    session.dataset_context = dataset.analysis_context
    session.save()
    
    return Response({"status": "ok", "message": "Dataset activado correctamente"})
