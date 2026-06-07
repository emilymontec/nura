
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def simple_forecast(df: pd.DataFrame, target_col: str, periods: int = 3) -> Dict[str, Any]:
    """Perform a simple linear trend projection for a numeric column."""
    if target_col not in df.columns or not pd.api.types.is_numeric_dtype(df[target_col]):
        return {}
        
    series = df[target_col].dropna().values
    if len(series) < 3:
        return {}
        
    # Simple linear regression proxy
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

def simulate_scenario(df: pd.DataFrame, variable: str, increase_pct: float) -> Dict[str, Any]:
    """Simulate the impact of increasing a variable on others based on correlations."""
    from .analyzer import compute_correlations
    
    if variable not in df.columns:
        return {"error": f"Variable {variable} no encontrada."}
        
    corrs = compute_correlations(df, threshold=0.4)
    impacts = []
    
    # Filter correlations involving our variable
    relevant_corrs = [c for c in corrs if c["col1"] == variable or c["col2"] == variable]
    
    for c in relevant_corrs:
        other_col = c["col2"] if c["col1"] == variable else c["col1"]
        # Simplified impact: delta_y = correlation * delta_x
        impact_pct = c["correlation"] * increase_pct
        impacts.append({
            "column": other_col,
            "impact_pct": round(float(impact_pct), 2),
            "type": "Positivo" if impact_pct > 0 else "Negativo"
        })
        
    return {
        "scenario": f"Incremento de {increase_pct}% en {variable}",
        "impacts": impacts
    }
