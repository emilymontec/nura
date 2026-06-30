from typing import Dict, Any, List
import pandas as pd
import numpy as np
from .utils import detect_file_type
from .scoring import evaluate_business
from .trends import analyze_numeric_trends
from .anomalies import detect_anomalies, check_fraud_signals
from .forecasting import simple_forecast


def load_csv(file_obj) -> pd.DataFrame:
    file_type = (detect_file_type(file_obj) or "").strip().lower()

    def _read_csv_fallback() -> pd.DataFrame:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "utf-16"]
        separators = [",", ";", "\t", "|"]
        last_err: Exception | None = None
        for enc in encodings:
            for sep in separators:
                try:
                    try:
                        file_obj.seek(0)
                    except Exception:
                        pass
                    df = pd.read_csv(file_obj, encoding=enc, sep=sep)
                    if df is None or df.empty or len(df.columns) == 0:
                        raise ValueError("No columns parsed from CSV.")
                    return df
                except Exception as e:
                    last_err = e
        raise ValueError(f"CSV no compatible o vacío. Error original: {last_err}") from last_err

    if file_type in [".xlsx", ".xls"]:
        try:
            try:
                file_obj.seek(0)
            except Exception:
                pass
            df = pd.read_excel(file_obj)
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo Excel: {e}") from e
        if df is None or df.empty or len(df.columns) == 0:
            raise ValueError("El Excel está vacío o no contiene columnas válidas.")
        return df
    if file_type == ".csv":
        return _read_csv_fallback()
    return _read_csv_fallback()


def _infer_semantic_type(col_name: str, dtype_str: str) -> str:
    col_lower = col_name.lower()
    if any(word in col_lower for word in ["precio", "price", "costo", "cost", "monto", "amount", "total", "subtotal", "tax", "impuesto", "profit", "ganancia", "margen", "margin", "ingreso", "revenue"]):
        return "Financiero"
    if any(word in col_lower for word in ["ventas", "sales", "pedido", "order", "invoice", "factura", "transaccion", "transaction", "compra", "purchase"]):
        return "Ventas"
    if any(word in col_lower for word in ["fecha", "date", "tiempo", "time", "año", "year", "mes", "month", "dia", "day", "hora", "hour", "created", "updated", "timestamp"]):
        return "Temporal"
    if any(word in col_lower for word in ["id", "codigo", "code", "sku", "uuid", "pk", "fk", "key", "llave"]):
        return "Identificador"
    if any(word in col_lower for word in ["cliente", "client", "customer", "usuario", "user", "lead", "prospecto", "contacto", "email", "correo", "nombre", "name", "apellido", "phone", "telefono"]):
        return "Clientes"
    if any(word in col_lower for word in ["categoria", "category", "tipo", "type", "estado", "status", "producto", "product", "region", "pais", "country", "ciudad", "city", "canal", "channel", "brand", "marca", "modelo", "model"]):
        return "Dimensión Categórica"
    if any(word in col_lower for word in ["cantidad", "quantity", "qty", "volumen", "volume", "peso", "weight", "stock", "inventario", "units", "unidades"]):
        return "Métrica/Cantidad"
    if any(word in col_lower for word in ["riesgo", "risk", "churn", "fraude", "fraud", "error", "falla", "failure", "alert", "alerta", "warning", "advertencia", "atraso", "delay", "mora"]):
        return "Riesgo"
    if "object" in dtype_str or "str" in dtype_str:
        return "Texto/Categoría"
    elif "int" in dtype_str or "float" in dtype_str:
        return "Numérico Genérico"
    return "Desconocido"


def detect_industry(df: pd.DataFrame) -> str:
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
                scores[industry] += 2
            if industry.lower() in cols:
                scores[industry] += 5
    best_industry = max(scores, key=scores.get)
    if scores[best_industry] > 0:
        return best_industry
    return "General / Negocios"


def get_business_context(df: pd.DataFrame, industry: str) -> str:
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
    correlations = []
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) < 2:
        return correlations
    corr_matrix = numeric_df.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]
            if pd.notna(corr_value) and abs(corr_value) >= threshold:
                strength = "Muy Fuerte" if abs(corr_value) >= 0.85 else ("Fuerte" if abs(corr_value) >= 0.7 else "Moderado")
                correlations.append({
                    "col1": col1,
                    "col2": col2,
                    "correlation": round(float(corr_value), 2),
                    "strength": strength,
                    "direction": "Positiva" if corr_value > 0 else "Negativa"
                })
    correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return correlations


def detect_critical_variables(df: pd.DataFrame) -> List[Dict[str, Any]]:
    corrs = compute_correlations(df, threshold=0.6)
    influence_counts = {}
    for c in corrs:
        influence_counts[c["col1"]] = influence_counts.get(c["col1"], 0) + 1
        influence_counts[c["col2"]] = influence_counts.get(c["col2"], 0) + 1
    critical = []
    for col, count in influence_counts.items():
        if count >= 2:
            critical.append({
                "column": col,
                "influence_score": count,
                "importance": "Alta" if count >= 4 else "Media"
            })
    critical.sort(key=lambda x: x["influence_score"], reverse=True)
    return critical


def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
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
    return df.head(n).replace({np.nan: None}).to_dict(orient="records")


def get_chart_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    charts = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:3]
    for col in numeric_cols:
        series = df[col].dropna()
        if not series.empty:
            charts.append({
                "type": "distribution",
                "column": col,
                "data": series.tolist()[:100]
            })
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


def get_kpis(df: pd.DataFrame) -> List[Dict[str, Any]]:
    kpis = []
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return kpis
    for col in numeric_df.columns:
        col_lower = col.lower()
        if any(w in col_lower for w in ["total", "monto", "amount", "revenue", "ventas", "sales", "profit", "ganancia"]):
            kpis.append({
                "label": f"Total {col}",
                "value": round(float(numeric_df[col].sum()), 2),
                "type": "currency"
            })
            kpis.append({
                "label": f"Promedio {col}",
                "value": round(float(numeric_df[col].mean()), 2),
                "type": "currency"
            })
        elif any(w in col_lower for w in ["count", "cantidad", "qty", "items", "unidades", "units"]):
            kpis.append({
                "label": f"Volumen {col}",
                "value": int(numeric_df[col].sum()),
                "type": "number"
            })
    if not kpis:
        kpis.append({
            "label": "Registros Totales",
            "value": len(df),
            "type": "number"
        })
        kpis.append({
            "label": "Columnas Analizadas",
            "value": len(df.columns),
            "type": "number"
        })
    return kpis[:4]