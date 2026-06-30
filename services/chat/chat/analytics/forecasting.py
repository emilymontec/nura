import pandas as pd
import numpy as np
from typing import Dict, List, Any


def simple_forecast(df: pd.DataFrame, target_col: str, periods: int = 3) -> Dict[str, Any]:
    if target_col not in df.columns or not pd.api.types.is_numeric_dtype(df[target_col]):
        return {}
    series = df[target_col].dropna().values
    if len(series) < 3:
        return {}
    x = np.arange(len(series))
    y = series
    slope, intercept = np.polyfit(x, y, 1)
    last_val = series[-1]
    projections = []
    for i in range(1, periods + 1):
        next_val = intercept + slope * (len(series) + i - 1)
        projections.append(round(float(max(0, next_val)), 2))
    growth_rate = (projections[-1] - last_val) / last_val if last_val != 0 else 0
    return {
        "column": target_col,
        "current_value": float(last_val),
        "projections": projections,
        "trend_slope": float(slope),
        "expected_growth": round(float(growth_rate * 100), 2)
    }