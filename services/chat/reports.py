"""
Módulo 4 - Visualización y Reportes.

Antes de este cambio, el botón "exportar_reporte_pdf()" del frontend era
texto estático sin ningún handler, y no existía ninguna librería de
generación de PDF instalada ni ninguna vista que lo produjera. Este módulo
genera un PDF real (resumen ejecutivo, salud de datos, KPIs, hallazgos y
recomendaciones) a partir del `dataset_context` ya calculado por el motor
de analítica.
"""
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)


PALETTE = {
    "purple": colors.HexColor("#7C3AED"),
    "dark": colors.HexColor("#1F2937"),
    "gray": colors.HexColor("#6B7280"),
    "red": colors.HexColor("#DC2626"),
    "green": colors.HexColor("#16A34A"),
    "yellow": colors.HexColor("#CA8A04"),
    "light_bg": colors.HexColor("#F3F4F6"),
}


def _styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(name="NuraTitle", fontSize=22, leading=26, textColor=PALETTE["dark"], spaceAfter=4))
    base.add(ParagraphStyle(name="NuraSubtitle", fontSize=11, textColor=PALETTE["gray"], spaceAfter=20))
    base.add(ParagraphStyle(name="NuraH2", fontSize=14, textColor=PALETTE["purple"], spaceBefore=16, spaceAfter=8))
    base.add(ParagraphStyle(name="NuraBody", fontSize=10, leading=15, textColor=PALETTE["dark"]))
    base.add(ParagraphStyle(name="NuraBullet", fontSize=10, leading=15, textColor=PALETTE["dark"], leftIndent=12))
    return base


def _score_color(score: float):
    if score >= 80:
        return PALETTE["green"]
    if score >= 50:
        return PALETTE["yellow"]
    return PALETTE["red"]


def generate_pdf_report(context: dict, generated_for: str = "") -> bytes:
    """
    Genera un reporte ejecutivo en PDF a partir de un dataset_context ya
    calculado (el mismo dict que produce services/analytics/analyzer.py).
    Devuelve los bytes del PDF; no toca el sistema de archivos.
    """
    if not context or not context.get("file_name"):
        raise ValueError("No hay un dataset analizado en esta sesión para generar un reporte.")

    styles = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    )
    story = []

    file_name = context.get("file_name", "dataset")
    industry = context.get("industry", "General / Negocios")
    summary = context.get("summary", {})
    health = context.get("health", {})
    kpis = context.get("kpis", [])
    insights = context.get("insights", [])
    anomalies = context.get("anomalies", [])
    correlations = context.get("correlations", [])
    fraud_signals = context.get("fraud_signals", [])

    # Portada / encabezado
    story.append(Paragraph("Reporte Ejecutivo Nura", styles["NuraTitle"]))
    subtitle = f"Archivo: {file_name} · Sector: {industry} · Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    if generated_for:
        subtitle += f" · Para: {generated_for}"
    story.append(Paragraph(subtitle, styles["NuraSubtitle"]))

    # Resumen del dataset
    story.append(Paragraph("Resumen de la información", styles["NuraH2"]))
    resumen_data = [
        ["Filas analizadas", str(summary.get("rows", "—"))],
        ["Columnas", str(summary.get("columns", "—"))],
        ["Celdas vacías", str(summary.get("total_missing", "—"))],
        ["Filas duplicadas", str(summary.get("duplicate_rows", "—"))],
    ]
    resumen_table = Table(resumen_data, colWidths=[7 * cm, 7 * cm])
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PALETTE["light_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, -1), PALETTE["dark"]),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
    ]))
    story.append(resumen_table)

    # Salud de los datos
    score = health.get("health_score", 0)
    risk = health.get("risk_level", "desconocido")
    story.append(Paragraph("Salud de los datos", styles["NuraH2"]))
    score_style = ParagraphStyle(name="ScoreStyle", parent=styles["NuraBody"], textColor=_score_color(score), fontSize=13)
    story.append(Paragraph(f"Puntuación: {score}/100 — Riesgo {risk}", score_style))
    story.append(Spacer(1, 8))

    # KPIs
    if kpis:
        story.append(Paragraph("Indicadores clave (KPIs)", styles["NuraH2"]))
        kpi_rows = [["Indicador", "Valor"]] + [[k.get("label", "—"), str(k.get("value", "—"))] for k in kpis[:12]]
        kpi_table = Table(kpi_rows, colWidths=[9 * cm, 5 * cm])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PALETTE["purple"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALETTE["light_bg"]]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(kpi_table)

    # Alertas de fraude/errores
    if fraud_signals:
        story.append(Paragraph("Alertas de fraude / error", styles["NuraH2"]))
        for s in fraud_signals:
            story.append(Paragraph(f"⚠ {s}", ParagraphStyle(name="Fraud", parent=styles["NuraBullet"], textColor=PALETTE["red"])))

    # Anomalías
    if anomalies:
        story.append(Paragraph("Anomalías detectadas", styles["NuraH2"]))
        story.append(Paragraph(
            f"Se detectaron {len(anomalies)} registros con comportamiento fuera de lo común "
            "(mostrando hasta 5 ejemplos):", styles["NuraBody"]
        ))
        for a in anomalies[:5]:
            story.append(Paragraph(f"• Fila {a.get('index')}: {a.get('reason', '')}", styles["NuraBullet"]))

    # Correlaciones
    if correlations:
        story.append(Paragraph("Relaciones encontradas entre variables", styles["NuraH2"]))
        for c in correlations[:5]:
            story.append(Paragraph(
                f"• {c.get('col1')} y {c.get('col2')}: relación {c.get('direction', '').lower()} "
                f"({c.get('strength', '')})", styles["NuraBullet"]
            ))

    # Hallazgos / insights en lenguaje natural
    if insights:
        story.append(PageBreak())
        story.append(Paragraph("Hallazgos y recomendaciones", styles["NuraH2"]))
        for i in insights:
            story.append(Paragraph(f"• {i}", styles["NuraBullet"]))
            story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
