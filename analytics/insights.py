# analytics/insights.py
from typing import Dict, Any, List

def explain_importance(correlations: List[Dict[str, Any]], critical_vars: List[Dict[str, Any]] = None) -> List[str]:
    """Translate technical correlations into business 'Explain Importance' insights."""
    explanations = []
    
    if correlations:
        # Take the top 3 strongest correlations
        for corr in correlations[:3]:
            col1 = corr["col1"]
            col2 = corr["col2"]
            strength = corr["strength"]
            direction = corr["direction"]
            
            if direction == "Positiva":
                explanations.append(f"Vínculo detectado: '{col1}' está altamente relacionado con '{col2}'. Un incremento en uno suele impulsar al otro.")
            else:
                explanations.append(f"Dependencia inversa: Existe una relación opuesta entre '{col1}' y '{col2}'. Cuando uno sube, el otro tiende a bajar.")

    if critical_vars:
        for var in critical_vars[:2]:
            col = var["column"]
            importance = var["importance"]
            explanations.append(f"Variable Crítica: '{col}' es un eje central en tus datos, ya que influye directamente en múltiples métricas.")
            
    return explanations

def generate_ai_cards(summary: Dict, health: Dict, correlations: List, critical_vars: List, anomalies: List) -> Dict[str, Dict]:
    """Generate high-level 'AI Cards' for the Intelligent Dashboard."""
    cards = {
        "top_risk": {
            "title": "Top Riesgo",
            "icon": "⚠️",
            "value": "Bajo",
            "color": "green",
            "description": "No se detectan riesgos críticos."
        },
        "top_opportunity": {
            "title": "Top Oportunidad",
            "icon": "🚀",
            "value": "Estable",
            "color": "blue",
            "description": "Mantener estrategia actual."
        },
        "top_priority": {
            "title": "Top Prioridad",
            "icon": "🎯",
            "value": "Calidad",
            "color": "yellow",
            "description": "Optimizar recolección de datos."
        }
    }

    # 1. Logic for Top Risk
    if anomalies or health.get("health_score", 100) < 70:
        cards["top_risk"] = {
            "title": "Top Riesgo",
            "icon": "🚨",
            "value": "Crítico" if len(anomalies) > 5 else "Moderado",
            "color": "red",
            "description": f"Detectadas {len(anomalies)} anomalías en el comportamiento de los datos."
        }
    
    # 2. Logic for Top Opportunity
    if correlations:
        best_corr = correlations[0]
        cards["top_opportunity"] = {
            "title": "Top Oportunidad",
            "icon": "📈",
            "value": "Crecimiento",
            "color": "green",
            "description": f"Vínculo fuerte entre {best_corr['col1']} y {best_corr['col2']}."
        }
    
    # 3. Logic for Top Priority
    if critical_vars:
        best_var = critical_vars[0]
        cards["top_priority"] = {
            "title": "Top Prioridad",
            "icon": "⚡",
            "value": best_var["column"],
            "color": "purple",
            "description": f"Variable con mayor impacto detectada en el ecosistema."
        }
        
    return cards

def generate_insight_feed(summary: Dict[str, Any], trends: Dict[str, Any], health: Dict[str, Any], correlations: List[Dict[str, Any]] = None, critical_vars: List[Dict[str, Any]] = None, anomalies: List[Dict] = None, fraud_signals: List[str] = None) -> List[Dict[str, Any]]:
    """Generate a structured feed of proactive insights with business categorization and colors."""
    feed = []
    
    # 1. ROJO: Riesgos, Anomalías y Fraude
    if fraud_signals:
        for signal in fraud_signals:
            feed.append({
                "category": "Alerta de Fraude/Error",
                "type": "fraud",
                "color": "red",
                "message": signal
            })

    if anomalies:
        feed.append({
            "category": "Anomalía detectada",
            "type": "anomaly",
            "color": "red",
            "message": f"Se detectaron {len(anomalies)} registros con comportamiento fuera de lo común (Outliers)."
        })
    score = health.get("health_score", 0)
    if score < 60:
        feed.append({
            "category": "Riesgo detectado",
            "type": "risk",
            "color": "red",
            "message": f"Calidad de datos crítica ({score}/100). Se detectaron inconsistencias que podrían afectar la toma de decisiones."
        })
        
    missing = summary.get("total_missing", 0)
    if missing > (summary.get("rows", 0) * summary.get("columns", 0) * 0.1): # More than 10% missing
        feed.append({
            "category": "Riesgo detectado",
            "type": "risk",
            "color": "red",
            "message": f"Alta tasa de datos faltantes ({missing} celdas vacías). El análisis podría estar sesgado."
        })

    # 2. VERDE: Oportunidades
    if correlations:
        for corr in correlations[:2]:
            if corr["direction"] == "Positiva" and corr["strength"] in ["Fuerte", "Muy Fuerte"]:
                feed.append({
                    "category": "Oportunidad encontrada",
                    "type": "opportunity",
                    "color": "green",
                    "message": f"Palanca de crecimiento: Existe una relación muy fuerte entre '{corr['col1']}' y '{corr['col2']}'. Potenciar uno impulsará directamente al otro."
                })

    if critical_vars:
        for var in critical_vars[:1]:
            feed.append({
                "category": "Oportunidad encontrada",
                "type": "opportunity",
                "color": "green",
                "message": f"Eje estratégico: '{var['column']}' ha sido identificado como una variable crítica que influye en múltiples áreas del negocio."
            })

    # 3. AMARILLO: Tendencias Observadas
    for col, trend_data in trends.items():
        trend_val = trend_data.get("trend", 0)
        if abs(trend_val) > 0.05: # Significant trend
            direction = "crecimiento" if trend_val > 0 else "caída"
            status = "Tendencia observada"
            feed.append({
                "category": status,
                "type": "trend",
                "color": "yellow",
                "message": f"Movimiento detectado: Se observa una {direction} constante en la métrica '{col}' en los últimos registros."
            })
            
    if not feed:
        feed.append({
            "category": "Estabilidad",
            "type": "info",
            "color": "blue",
            "message": "No se detectaron anomalías ni movimientos bruscos. El negocio muestra un comportamiento estable."
        })
        
    return feed

def generate_insights(summary: Dict[str, Any], trends: Dict[str, Any], health: Dict[str, Any], correlations: List[Dict[str, Any]] = None, critical_vars: List[Dict[str, Any]] = None) -> List[str]:
    """Generate automated insights based on data summary, trends, and health score."""
    insights = []
    
    # Explain Importance (Nivel 8)
    if correlations:
        insights.extend(explain_importance(correlations, critical_vars))
        
    # Check health
    score = health.get("health_score", 0)
    if score < 50:
        insights.append(f"Atención con los datos: La calidad de la información es baja. Revisa si hay celdas vacías o filas repetidas.")
    elif score >= 80:
        insights.append("¡Excelente!: Tu información se ve limpia y completa.")
        
    # Check summary
    missing = summary.get("total_missing", 0)
    if missing > 0:
        insights.append(f"Información incompleta: Hay {missing} celdas vacías en tu archivo.")
        
    dupes = summary.get("duplicate_rows", 0)
    if dupes > 0:
        insights.append(f"Datos repetidos: Hay {dupes} filas exactamente iguales que podrían distorsionar tus totales.")
        
    # Check trends
    for col, trend_data in trends.items():
        trend_val = trend_data.get("trend", 0)
        if trend_val > 0:
            insights.append(f"Crecimiento en '{col}': Los datos muestran que esta métrica tiende a subir.")
        elif trend_val < 0:
            insights.append(f"Caída en '{col}': Los datos muestran que esta métrica tiende a bajar.")
            
    # Check correlations / Relationships
    if correlations:
        for corr in correlations:
            col1 = corr["col1"]
            col2 = corr["col2"]
            direction = corr["direction"]
            strength = corr["strength"]
            val = corr["correlation"]
            
            if direction == "Positiva":
                insights.append(f"Relación directa detectada: Cuando '{col1}' sube, '{col2}' también tiende a subir. Esto podría ser útil para impulsar el crecimiento.")
            else:
                insights.append(f"Relación inversa detectada: Cuando '{col1}' sube, '{col2}' tiende a bajar. Presta atención a esto para evitar problemas o compensaciones indeseadas.")
            
    if not insights:
        insights.append("A simple vista, no encontramos patrones ni relaciones fuertes. La información parece estable.")
        
    return insights
