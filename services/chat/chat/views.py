import io
import json
import traceback
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests

from .models import ChatSession, ChatMessage


def index(request):
    return render(request, "index.html")


def test_endpoint(request):
    return JsonResponse({"status": "ok", "message": "La API de NURA esta operativa"})


def make_json_safe(value):
    import numpy as np
    import pandas as pd
    if isinstance(value, dict):
        return {str(k): make_json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, np.ndarray)):
        return [make_json_safe(item) for item in value]
    if isinstance(value, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, np.float32, np.float16)):
        return float(value)
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if pd.isna(value):
        return None
    if hasattr(value, 'tolist'):
        return make_json_safe(value.tolist())
    if hasattr(value, 'item'):
        return make_json_safe(value.item())
    return value


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
    url = f"{settings.ANALYTICS_SERVICE_URL}/analyze"
    files = {"file": (filename, file_obj, "multipart/form-data")}
    response = requests.post(url, files=files, timeout=120)
    response.raise_for_status()
    return response.json()


def get_ai_report(context):
    url = f"{settings.AI_SERVICE_URL}/generate-report"
    response = requests.post(url, json={"context": context}, timeout=60)
    if response.status_code == 200:
        return response.json().get("report", None)
    print(f"[NURA] Error al generar reporte IA: {response.status_code} {response.text}")
    return None


def get_ai_chat_response(question, context, history):
    url = f"{settings.AI_SERVICE_URL}/chat"
    response = requests.post(url, json={"question": question, "context": context, "history": history}, timeout=60)
    if response.status_code == 200:
        return response.json().get("response", None)
    raise Exception(f"AI service returned {response.status_code}: {response.text}")


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
            ai_report = get_ai_report(safe_context)
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
            print(f"[NURA] CRASH EN ANALISIS: {err}")
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
            response_text = get_ai_chat_response(message, context, history)
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
