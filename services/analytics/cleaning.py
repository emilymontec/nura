import re
import pandas as pd
import numpy as np


def _is_string_col(series):
    return pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series)


_SPANISH_KEYWORDS = {
    "fecha", "cliente", "monto", "total", "precio", "costo", "ventas", "pedido",
    "producto", "categoria", "estado", "cantidad", "importe", "saldo", "cuenta",
    "factura", "numero", "nombre", "direccion", "telefono", "email", "ciudad",
    "pais", "region", "departamento", "empleado", "proveedor", ".descripcion",
    "observacion", "created_at", "updated_at", "usuario", "contraseña", "sexo",
    "genero", "edad", "nacimiento", "ingreso", "egreso", "utilidad", "ganancia",
    "margen", "descuento", "impuesto", "iva", "subtotal", "unidad", "medida",
    "tipo", "canal", "origen", "destino", "responsable", "prioridad", "avance",
}

_ENGLISH_KEYWORDS = {
    "date", "client", "amount", "total", "price", "cost", "sales", "order",
    "product", "category", "status", "quantity", "import", "balance", "account",
    "invoice", "number", "name", "address", "phone", "email", "city", "country",
    "region", "department", "employee", "supplier", "description", "observation",
    "created_at", "updated_at", "user", "password", "gender", "age", "birth",
    "income", "expense", "profit", "gain", "margin", "discount", "tax",
    "subtotal", "unit", "measure", "type", "channel", "source", "destination",
    "responsible", "priority", "progress",
}


def detect_language(columns):
    if not columns:
        return "es"
    cols_lower = [str(c).lower().strip() for c in columns]
    es_score = sum(1 for c in cols_lower if any(k in c for k in _SPANISH_KEYWORDS))
    en_score = sum(1 for c in cols_lower if any(k in c for k in _ENGLISH_KEYWORDS))
    return "es" if es_score >= en_score else "en"


def detect_headers(df_raw):
    if df_raw is None or df_raw.empty:
        return df_raw, False
    cols = [str(c).strip() for c in df_raw.columns]
    all_numeric = all(re.match(r'^-?\d+(\.\d+)?$', c) for c in cols)
    all_same = len(set(cols)) == 1
    has_empty = any(c == '' or c == 'Unnamed' or c.startswith('Unnamed') for c in cols)
    if all_numeric or all_same or has_empty:
        df_raw.columns = [f'col_{i}' for i in range(len(cols))]
        return df_raw, True
    return df_raw, False


def _normalize_number_value(val):
    if pd.isna(val) or not isinstance(val, str):
        return val
    cleaned = val.strip()
    if not cleaned:
        return val
    cleaned = re.sub(r'[\$\u00a2\u20b1\s]', '', cleaned)
    if not cleaned:
        return val
    has_comma_decimal = bool(re.search(r',\d{1,2}$', cleaned))
    has_dot_decimal = bool(re.search(r'\.\d{1,2}$', cleaned))
    has_thousand_dot = bool(re.search(r'\d{1,3}\.\d{3}', cleaned))
    has_thousand_comma = bool(re.search(r'\d{1,3},\d{3}', cleaned))
    if has_comma_decimal and has_thousand_dot:
        cleaned = cleaned.replace('.', '')
        cleaned = cleaned.replace(',', '.')
    elif has_dot_decimal and has_thousand_comma:
        cleaned = cleaned.replace(',', '')
    elif has_comma_decimal and not has_thousand_dot:
        cleaned = cleaned.replace(',', '.')
    elif has_thousand_comma and not has_dot_decimal:
        cleaned = cleaned.replace(',', '')
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return val


def normalize_numbers(df):
    changes = []
    for col in df.columns:
        if not _is_string_col(df[col]):
            continue
        sample = df[col].dropna().head(200)
        if len(sample) < 3:
            continue
        converted = sample.apply(_normalize_number_value)
        numeric_count = converted.apply(lambda x: isinstance(x, (int, float))).sum()
        ratio = numeric_count / max(len(sample), 1)
        if ratio >= 0.7:
            full = df[col].apply(_normalize_number_value)
            df[col] = pd.to_numeric(full, errors='coerce')
            changes.append(f"'{col}': texto -> numérico")
    return df, changes


_DATE_PATTERNS = [
    (r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$', ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y', '%m/%d/%Y', '%m-%d-%Y', '%m/%d/%y']),
    (r'^\d{4}[/-]\d{1,2}[/-]\d{1,2}$', ['%Y-%m-%d', '%Y/%m/%d']),
    (r'^\d{1,2}\s+\w{3,9}\s+\d{2,4}$', ['%d %B %Y', '%d %b %Y']),
    (r'^\w{3,9}\s+\d{1,2},?\s+\d{2,4}$', ['%B %d, %Y', '%B %d %Y', '%b %d, %Y', '%b %d %Y']),
]


def _is_likely_date(val):
    if pd.isna(val) or not isinstance(val, str):
        return False
    val = val.strip()
    if not val:
        return False
    for pattern, _ in _DATE_PATTERNS:
        if re.match(pattern, val, re.IGNORECASE):
            return True
    return False


def _try_parse_dates(series):
    sample = series.dropna().head(200)
    if len(sample) < 3:
        return series, False
    date_ratio = sample.apply(_is_likely_date).sum()
    if date_ratio / max(len(sample), 1) < 0.6:
        return series, False
    for _, formats in _DATE_PATTERNS:
        for fmt in formats:
            try:
                parsed = pd.to_datetime(sample, format=fmt, errors='coerce')
                if parsed.notna().sum() / max(len(sample), 1) >= 0.7:
                    full = pd.to_datetime(series, format=fmt, errors='coerce')
                    if full.notna().sum() / max(len(series.dropna()), 1) >= 0.6:
                        return full, True
            except Exception:
                continue
    try:
        parsed = pd.to_datetime(sample, format='mixed', dayfirst=True, errors='coerce')
        if parsed.notna().sum() / max(len(sample), 1) >= 0.7:
            full = pd.to_datetime(series, format='mixed', dayfirst=True, errors='coerce')
            if full.notna().sum() / max(len(series.dropna()), 1) >= 0.6:
                return full, True
    except Exception:
        pass
    return series, False


def normalize_dates(df):
    changes = []
    date_cols_detected = []
    for col in df.columns:
        if not _is_string_col(df[col]):
            continue
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        col_lower = col.lower()
        is_date_keyword = any(k in col_lower for k in [
            'fecha', 'date', 'time', 'tiempo', 'created', 'updated', 'timestamp',
            'dia', 'day', 'mes', 'month', 'año', 'year', 'hora', 'hour',
            'nacimiento', 'birth', 'vencimiento', 'due', 'expir', 'register',
        ])
        new_col, converted = _try_parse_dates(df[col])
        if converted:
            df[col] = new_col
            date_cols_detected.append(col)
            changes.append(f"'{col}': texto -> fecha")
        elif is_date_keyword:
            try:
                full = pd.to_datetime(df[col], format='mixed', dayfirst=True, errors='coerce')
                if full.notna().sum() / max(len(df[col].dropna()), 1) >= 0.5:
                    df[col] = full
                    date_cols_detected.append(col)
                    changes.append(f"'{col}': texto -> fecha (por nombre de columna)")
            except Exception:
                pass
    return df, changes, date_cols_detected


_BOOL_MAP = {
    'true': True, 'false': False,
    'yes': True, 'no': False,
    'si': True, 'sí': True,
    'verdadero': True, 'falso': False,
    '1': True, '0': False,
}


def correct_types(df):
    changes = []
    for col in df.columns:
        if not _is_string_col(df[col]):
            continue
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) == 0 or len(unique_vals) > 10:
            continue
        lower_vals = set(str(v).lower().strip() for v in unique_vals)
        if lower_vals.issubset(set(_BOOL_MAP.keys())):
            df[col] = df[col].str.lower().str.strip().map(_BOOL_MAP)
            changes.append(f"'{col}': texto -> booleano")
    return df, changes


def remove_duplicates(df):
    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        return df, [f"Eliminadas {dup_count} filas duplicadas"]
    return df, []


def handle_nulls(df):
    changes = []
    all_null_cols = [c for c in df.columns if df[c].isna().all()]
    if all_null_cols:
        df = df.drop(columns=all_null_cols)
        changes.append(f"Columnas eliminadas (100% nulas): {all_null_cols}")
    null_cols = {c: int(df[c].isna().sum()) for c in df.columns if df[c].isna().any()}
    for col, count in null_cols.items():
        pct = count / max(len(df), 1) * 100
        if pct > 80:
            df = df.drop(columns=[col])
            changes.append(f"Columna '{col}' eliminada ({pct:.0f}% nulos)")
        elif pd.api.types.is_numeric_dtype(df[col]):
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            changes.append(f"'{col}': {count} nulos reemplazados con mediana ({median_val:.2f})")
        else:
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col] = df[col].fillna(mode_val.iloc[0])
                changes.append(f"'{col}': {count} nulos reemplazados con moda")
    return df, changes


def normalize_whitespace(df):
    changes = []
    for col in df.columns:
        if not _is_string_col(df[col]):
            continue
        before = df[col].copy()
        df[col] = df[col].str.strip()
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
        if not before.equals(df[col]):
            changes.append(f"'{col}': espacios en blanco normalizados")
    return df, changes


def clean_dataframe(df):
    all_changes = []
    df, ch = normalize_whitespace(df)
    all_changes.extend(ch)
    df, ch = normalize_numbers(df)
    all_changes.extend(ch)
    df, ch, date_cols = normalize_dates(df)
    all_changes.extend(ch)
    df, ch = correct_types(df)
    all_changes.extend(ch)
    df, ch = remove_duplicates(df)
    all_changes.extend(ch)
    df, ch = handle_nulls(df)
    all_changes.extend(ch)
    return df, all_changes, date_cols
