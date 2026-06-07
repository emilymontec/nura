# analytics/analyzer.py
"""Utilities to analyze business datasets using pandas."""
from typing import Dict, Any, List

import pandas as pd

from .utils import detect_file_type
import numpy as np


def load_csv(file_obj) -> pd.DataFrame:
    """Load a CSV or Excel file into a pandas DataFrame."""
    file_type = detect_file_type(file_obj)
    readers = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
    }
    reader = readers.get(file_type)
    if not reader:
        raise ValueError("Tipo de archivo no soportado. Sube un archivo CSV o Excel.")
    return reader(file_obj)

def _infer_semantic_type(col_name: str, dtype_str: str) -> str:
    """Infer the business semantic type of a column based on its name and dtype."""
    col_lower = col_name.lower()
    
    # Financial / Monetary / Sales
    if any(word in col_lower for word in ["precio", "price", "costo", "cost", "monto", "amount", "total", "subtotal", "tax", "impuesto", "profit", "ganancia", "margen", "margin", "ingreso", "revenue"]):
        return "Financiero"
    
    # Sales specific
    if any(word in col_lower for word in ["ventas", "sales", "pedido", "order", "invoice", "factura", "transaccion", "transaction", "compra", "purchase"]):
        return "Ventas"
    
    # Temporal
    if any(word in col_lower for word in ["fecha", "date", "tiempo", "time", "año", "year", "mes", "month", "dia", "day", "hora", "hour", "created", "updated", "timestamp"]):
        return "Temporal"
    
    # Identifiers
    if any(word in col_lower for word in ["id", "codigo", "code", "sku", "uuid", "pk", "fk", "key", "llave"]):
        return "Identificador"
        
    # Customers / Users
    if any(word in col_lower for word in ["cliente", "client", "customer", "usuario", "user", "lead", "prospecto", "contacto", "email", "correo", "nombre", "name", "apellido", "phone", "telefono"]):
        return "Clientes"
        
    # Categorical/Business Dimensions
    if any(word in col_lower for word in ["categoria", "category", "tipo", "type", "estado", "status", "producto", "product", "region", "pais", "country", "ciudad", "city", "canal", "channel", "brand", "marca", "modelo", "model"]):
        return "Dimensión Categórica"
        
    # Quantities / Metrics
    if any(word in col_lower for word in ["cantidad", "quantity", "qty", "volumen", "volume", "peso", "weight", "stock", "inventario", "units", "unidades"]):
        return "Métrica/Cantidad"

    # Risks / Anomalies (Signals)
    if any(word in col_lower for word in ["riesgo", "risk", "churn", "fraude", "fraud", "error", "falla", "failure", "alert", "alerta", "warning", "advertencia", "atraso", "delay", "mora"]):
        return "Riesgo"
        
    if "object" in dtype_str or "str" in dtype_str:
        return "Texto/Categoría"
    elif "int" in dtype_str or "float" in dtype_str:
        return "Numérico Genérico"
    return "Desconocido"

def detect_industry(df: pd.DataFrame) -> str:
    """Detect the industry of the dataset based on column names."""
    cols = [c.lower() for c in df.columns]
    
    industries = {
        "Ecommerce": ["order", "pedido", "cart", "carrito", "sku", "shipping", "envio", "delivery", "product", "producto", "variant", "variante", "stock", "inventory", "tienda", "store"],
        "SaaS": ["subscription", "suscripcion", "plan", "mrr", "arr", "churn", "trial", "prueba", "user_id", "active", "feature", "upgrade", "license", "licencia", "recurring", "recurrente"],
        "Finanzas": ["transaction", "transaccion", "balance", "account", "cuenta", "credit", "debito", "debit", "loan", "prestamo", "interest", "interes", "asset", "activo", "liability", "pasivo", "investment", "inversion"],
        "Marketing": ["campaign", "campaña", "click", "impression", "impresion", "ctr", "cpc", "conversion", "lead", "source", "fuente", "medium", "medio", "ad_group", "keyword", "reach", "alcance"],
        "Recursos Humanos": ["employee", "empleado", "payroll", "nomina", "salary", "salario", "department", "departamento", "hiring", "contratacion", "turnover", "performance", "desempeño", "vacation", "vacaciones", "bonus", "bono"]
    }
    
    scores = {industry: 0 for industry in industries}
    for industry, keywords in industries.items():
        for keyword in keywords:
            if any(keyword in col for col in cols):
                scores[industry] += 2 # Match in column name
            # Also check if industry name itself is in columns
            if industry.lower() in cols:
                scores[industry] += 5
                
    # Get industry with highest score
    best_industry = max(scores, key=scores.get)
    if scores[best_industry] > 0:
        return best_industry
    return "General / Negocios"

def get_business_context(df: pd.DataFrame, industry: str) -> str:
    """Generate a brief business context description based on detected columns."""
    cols_info = column_info(df)
    semantic_counts = {}
    for col, info in cols_info.items():
        stype = info["semantic_type"]
        semantic_counts[stype] = semantic_counts.get(stype, 0) + 1
    
    context_parts = [f"Este es un dataset de tipo {industry}."]
    
    if semantic_counts.get("Financiero", 0) > 0 or semantic_counts.get("Ventas", 0) > 0:
        context_parts.append("Contiene información financiera y de transacciones comerciales.")
    if semantic_counts.get("Clientes", 0) > 0:
        context_parts.append("Incluye datos detallados de clientes o usuarios.")
    if semantic_counts.get("Riesgo", 0) > 0:
        context_parts.append("Se detectaron indicadores de riesgo o señales de alerta.")
    if semantic_counts.get("Temporal", 0) > 0:
        context_parts.append("La información tiene un componente temporal para análisis de tendencias.")
        
    return " ".join(context_parts)

def column_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Return column-level information including business semantic type."""
    info = {}
    for col in df.columns:
        dtype_str = str(df[col].dtype)
        info[col] = {
            "dtype": dtype_str,
            "semantic_type": _infer_semantic_type(col, dtype_str),
            "missing": int(df[col].isna().sum()),
            "unique": int(df[col].nunique()),
        }
    return info

def compute_correlations(df: pd.DataFrame, threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Calculate Pearson correlation for numeric columns.
    Returns a list of significant correlations (absolute value >= threshold).
    """
    correlations = []
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) < 2:
        return correlations
        
    # Standardize columns to handle different scales
    corr_matrix = numeric_df.corr()
    
    # Get upper triangle to avoid duplicates
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]
            
            if pd.notna(corr_value) and abs(corr_value) >= threshold:
                strength = "Muy Fuerte" if abs(corr_value) >= 0.85 else ("Fuerte" if abs(corr_value) >= 0.7 else "Moderada")
                correlations.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation": round(float(corr_value), 2),
                    "strength": strength,
                    "direction": "Positiva" if corr_value > 0 else "Negativa"
                })
                
    # Sort by absolute correlation (strongest first)
    correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return correlations

def detect_critical_variables(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Detect variables that have the most influence on others (hub variables)."""
    corrs = compute_correlations(df, threshold=0.6)
    influence_counts = {}
    
    for c in corrs:
        influence_counts[c["col1"]] = influence_counts.get(c["col1"], 0) + 1
        influence_counts[c["col2"]] = influence_counts.get(c["col2"], 0) + 1
        
    critical = []
    for col, count in influence_counts.items():
        if count >= 2: # Influences at least 2 other variables
            critical.append({
                "column": col,
                "influence_score": count,
                "importance": "Alta" if count >= 4 else "Media"
            })
            
    critical.sort(key=lambda x: x["influence_score"], reverse=True)
    return critical

def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """High‑level summary of the dataset.
    Returns row count, column count, total missing cells and duplicate rows.
    """
    rows, cols = df.shape
    total_missing = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    return {
        "rows": rows,
        "columns": cols,
        "total_missing": total_missing,
        "duplicate_rows": duplicate_rows,
    }

def get_preview(df: pd.DataFrame, n: int = 10) -> List[Dict[str, Any]]:
    """Return the first n rows of the dataset as a list of dicts."""
    # Handle NaN values for JSON serialization
    return df.head(n).replace({np.nan: None}).to_dict(orient="records")

def get_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect suitable columns for charts and return their data.
    - Categorical: Top 5 categories for bar chart.
    - Numeric: Values for a histogram or line chart.
    """
    charts = []
    
    # Numeric distributions
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:3] # Limit to 3
    for col in numeric_cols:
        series = df[col].dropna()
        if not series.empty:
            charts.append({
                "type": "distribution",
                "column": col,
                "data": series.tolist()[:100] # Limit data points
            })
            
    # Categorical counts
    cat_cols = df.select_dtypes(include=["object", "category"]).columns[:3]
    for col in cat_cols:
        counts = df[col].value_counts().head(5)
        if not counts.empty:
            charts.append({
                "type": "categorical",
                "column": col,
                "labels": counts.index.tolist(),
                "values": counts.values.tolist()
            })
            
    return charts

def analyze_csv(file_path: str) -> Dict[str, Any]:
    """Convenient wrapper that loads a CSV and returns a full analysis.
    """
    df = load_csv(file_path)
    industry = detect_industry(df)
    return {
        "summary": dataset_summary(df),
        "columns": column_info(df),
        "preview": get_preview(df),
        "charts": get_chart_data(df),
        "industry": industry,
        "business_context": get_business_context(df, industry),
        "critical_variables": detect_critical_variables(df)
    }
