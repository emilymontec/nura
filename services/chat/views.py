import io
import json
import traceback
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ChatSession, ChatMessage, UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from analytics.analyzer import (
    load_csv, dataset_summary, column_info, evaluate_business,
    analyze_numeric_trends, compute_correlations, detect_industry,
    get_business_context, detect_critical_variables, detect_anomalies,
    check_fraud_signals, simple_forecast, get_chart_data, get_preview, get_kpis
)
from analytics.utils import make_json_safe
from ai.llm import generate_ai_report, chat_with_data

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

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
        try:
            session = ChatSession.objects.get(session_id=session_id)
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
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesión no encontrada"}, status=404)
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
