# analytics/utils.py
"""Utility functions for analytics operations.

Provides common helper methods for file validation, type inference,
statistical calculations, and JSON-safe serialization.
"""
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import pandas as pd

def infer_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """Return a mapping of column names to inferred data types.
    Uses pandas dtypes and maps them to generic types.
    """
    type_map = {
        "int64": "integer",
        "float64": "float",
        "bool": "boolean",
        "datetime64[ns]": "datetime",
        "object": "string",
    }
    return {col: type_map.get(str(dtype), "unknown") for col, dtype in df.dtypes.items()}

def detect_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """Return a dict with count of missing values per column."""
    return df.isnull().sum().to_dict()

def detect_duplicates(df: pd.DataFrame) -> List[int]:
    """Return list of duplicate row indices (0‑based)."""
    dup_mask = df.duplicated(keep=False)
    return list(df[dup_mask].index)

def calculate_basic_stats(series: pd.Series) -> Dict[str, Any]:
    """Calculate mean, min, max, and standard deviation for a numeric series.
    Returns empty dict if series is non‑numeric.
    """
    if pd.api.types.is_numeric_dtype(series):
        return {
            "mean": series.mean(),
            "min": series.min(),
            "max": series.max(),
            "std": series.std(),
        }
    return {}


def detect_file_type(file_obj: Any) -> str:
    """Infer the uploaded file type from its filename."""
    filename = getattr(file_obj, "name", "") or str(file_obj)
    return Path(filename).suffix.lower()


def make_json_safe(value: Any) -> Any:
    """Recursively convert pandas/numpy values into JSON-safe Python types."""
    if isinstance(value, dict):
        return {str(key): make_json_safe(item) for key, item in value.items()}
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
    if hasattr(value, 'tolist'): # Handle other numpy-like objects
        return make_json_safe(value.tolist())
    if hasattr(value, 'item'): # Handle numpy scalars
        return make_json_safe(value.item())
    return value
