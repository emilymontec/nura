import pandas as pd
import numpy as np
from typing import Dict, Any


def compute_trend(series: pd.Series) -> float:
    if series.empty:
        return 0.0
    x = np.arange(len(series))
    y = series.values.astype(float)
    if np.allclose(y, y[0]):
        return 0.0
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def analyze_numeric_trends(df: pd.DataFrame) -> Dict[str, Any]:
    results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        series = df[col].dropna()
        results[col] = {
            "mean": series.mean(),
            "min": series.min(),
            "max": series.max(),
            "trend": compute_trend(series),
        }
    return results