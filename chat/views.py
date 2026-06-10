import json
import traceback

import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ai.llm import chat_with_data, generate_ai_report
from ai.memory import memory
from .models import ChatSession, ChatMessage

def index(request):
    """Render the basic frontend HTML."""
    return render(request, "index.html")

def test_endpoint(request):
    """Health check endpoint."""
    return JsonResponse({"status": "ok", "message": "La API de NURA esta operativa"})

from analytics.analyzer import load_csv, dataset_summary, column_info, compute_correlations, get_preview, get_chart_data, detect_industry, get_business_context, detect_critical_variables, detect_anomalies, check_fraud_signals, simple_forecast, get_kpis
from analytics.rag_engine import rag_analytics
from analytics.scoring import evaluate_business
from analytics.trends import analyze_numeric_trends
from analytics.insights import generate_insights, generate_insight_feed, generate_ai_cards
from analytics.utils import make_json_safe

@csrf_exempt
def analyze_endpoint(request):
    """Endpoint to trigger dataset analysis."""
    if request.method == "POST":
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No se ha subido ningun archivo"}, status=400)
            
        file = request.FILES['file']
        session_id = request.POST.get('session_id', 'default')
        
        # Procesamiento RAG (PDF, Word, Excel, CSV)
        rag_result = rag_analytics.process_file(file, session_id)
        
        # Guardar mensaje de usuario de carga de archivo inmediatamente
        memory.add_message(session_id, "user", f"Archivo cargado: {file.name}")
        
        try:
            # Solo intentamos análisis profundo de datos si es CSV o Excel
            suffix = file.name.lower().split('.')[-1]
            if suffix not in ['csv', 'xlsx', 'xls']:
                # Para otros archivos (PDF, DOCX), solo confirmamos la carga vía RAG
                bot_msg_rag = f"He recibido tu documento '{file.name}'. Ya lo he leído y guardado en mi memoria; puedes hacerme preguntas sobre su contenido cuando quieras."
                memory.add_message(session_id, "assistant", bot_msg_rag)
                return JsonResponse({"status": "rag_only", "file_name": file.name})

            df = load_csv(file)
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
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            forecasts = {}
            for col in numeric_cols[:2]:
                try:
                    f = simple_forecast(df, col)
                    if f: forecasts[col] = f
                except:
                    pass

            insights = generate_insights(summary, trends, health, correlations, critical_variables)
            insight_feed = generate_insight_feed(summary, trends, health, correlations, critical_variables, anomalies, fraud_signals)
            ai_cards = generate_ai_cards(summary, health, correlations, critical_variables, anomalies)
            kpis = get_kpis(df)
            
            context = {
                "file_name": file.name,
                "summary": summary,
                "columns": cols,
                "health": health,
                "trends": trends,
                "correlations": correlations,
                "insights": insights,
                "insight_feed": insight_feed,
                "ai_cards": ai_cards,
                "kpis": kpis,
                "preview": get_preview(df),
                "charts": get_chart_data(df),
                "industry": industry,
                "business_context": business_context,
                "critical_variables": critical_variables,
                "anomalies": anomalies,
                "fraud_signals": fraud_signals,
                "forecasts": forecasts
            }
            safe_context = make_json_safe(context)
            memory.store_dataset_context(session_id, safe_context)
            
            # Generar reporte de IA opcionalmente
            ai_report = None
            try:
                ai_report = generate_ai_report(safe_context)
                safe_context["ai_report"] = ai_report
            except Exception as e:
                print(f"[NURA] Error al generar reporte IA: {e}")

            score = safe_context['health'].get('health_score', 0)
            score_str = f"{score:.0f}"
            bot_msg1 = (
                f"¡Listo! Ya terminé de revisar tu archivo '{safe_context['file_name']}'.\n\n"
                f"He detectado que tu negocio pertenece al sector de **{industry}**.\n"
                f"Analicé un total de **{safe_context['summary']['rows']} filas** de información.\n"
                f"En cuanto a la salud de tus datos, les doy una puntuación de **{score_str} sobre 100** "
                f"(un nivel de riesgo **{safe_context['health']['risk_level'].lower()}**)."
            )
            memory.add_message(session_id, "assistant", bot_msg1)
            
            if ai_report:
                memory.add_message(session_id, "assistant", f"### 📝 Resumen Ejecutivo para ti\n\n{ai_report}")
            
            if insight_feed:
                feed_items = []
                for item in insight_feed:
                    icon = "💡" if item['color'] == 'green' else ("⚠️" if item['color'] == 'red' else "✨")
                    feed_items.append(f"{icon} **{item['category']}**: {item['message']}")
                
                feed_text = "\n".join(feed_items)
                
                # Formatear AI Cards para el chat
                cards_text = ""
                if ai_cards:
                    cards_text = "\n\n**📊 Puntos clave del negocio**\n"
                    for key, card in ai_cards.items():
                        cards_text += f"{card['icon']} **{card['title']}**: {card['value']} - {card['description']}\n"
                
                memory.add_message(session_id, "assistant", f"### 🚀 Descubrimientos Proactivos\n{feed_text}{cards_text}")
            elif insights:
                insights_text = "\n- ".join(insights)
                bot_msg2 = f"Aquí tienes algunas cosas interesantes que encontré en tu negocio ({industry}):\n- {insights_text}"
                memory.add_message(session_id, "assistant", bot_msg2)
            
            return JsonResponse(safe_context)
        except Exception as e:
            err = f"Error al analizar el archivo: {str(e)}"
            print(f"[NURA] CRASH EN ANALISIS: {err}")
            traceback.print_exc()
            return JsonResponse({"error": err, "exception": type(e).__name__, "detail": repr(e)}, status=500)
            
    return JsonResponse({"error": "Se requiere una peticion POST"}, status=400)

@csrf_exempt
def chat_endpoint(request):
    """Endpoint for chat interactions."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = (data.get("message", "") or "").strip()
            session_id = data.get("session_id", "default")
            if not message:
                return JsonResponse({"error": "El mensaje no puede estar vacio."}, status=400)
            
            # Guardar el mensaje del usuario inmediatamente para que no se pierda
            memory.add_message(session_id, "user", message)
            
            history = memory.get_history(session_id, message)
            
            context = memory.get_dataset_context(session_id) or {
                "has_dataset": False,
                "message": "No hay ningun dataset cargado en esta sesion.",
                "mode": "chat_general",
            }
            
            # This calls the LLM
            response = chat_with_data(message, context, history)
            
            # Guardar la respuesta del asistente
            memory.add_message(session_id, "assistant", response)
            
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Se requiere una peticion POST"}, status=400)


@csrf_exempt
def list_sessions(request):
    """List all chat sessions."""
    if request.method == "GET":
        sessions = ChatSession.objects.all().order_by('-updated_at')
        session_data = [
            {
                "session_id": s.session_id,
                "title": s.title,
                "updated_at": s.updated_at.isoformat()
            }
            for s in sessions
        ]
        return JsonResponse({"sessions": session_data})
    return JsonResponse({"error": "Metodo no permitido"}, status=405)


@csrf_exempt
def get_session_history(request, session_id):
    """Get chat history and context for a specific session."""
    if request.method == "GET":
        try:
            session = ChatSession.objects.get(session_id=session_id)
            messages = session.messages.filter(role__in=['user', 'assistant']).order_by('created_at')
            message_data = [
                {
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.isoformat()
                }
                for m in messages
            ]
            return JsonResponse({
                "session_id": session.session_id,
                "title": session.title,
                "dataset_context": session.dataset_context,
                "messages": message_data
            })
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesion no encontrada"}, status=404)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)


@csrf_exempt
def rename_session(request, session_id):
    """Rename a specific chat session."""
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_title = data.get("title", "").strip()
            if not new_title:
                return JsonResponse({"error": "El titulo no puede estar vacio"}, status=400)
            
            session = ChatSession.objects.get(session_id=session_id)
            session.title = new_title
            session.save(update_fields=['title', 'updated_at'])
            return JsonResponse({"status": "ok", "title": session.title})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesion no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)


@csrf_exempt
def delete_session(request, session_id):
    """Delete a specific chat session."""
    if request.method == "DELETE":
        try:
            session = ChatSession.objects.get(session_id=session_id)
            session.delete()
            return JsonResponse({"status": "ok", "message": "Sesion eliminada correctamente"})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Sesion no encontrada"}, status=404)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)
