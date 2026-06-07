
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, List, Any

def detect_anomalies(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Detect anomalies and outliers using Isolation Forest."""
    numeric_df = df.select_dtypes(include=[np.number]).dropna(axis=1, how='all')
    
    if numeric_df.empty or len(numeric_df) < 5:
        return []
        
    # Fill NaN for isolation forest
    numeric_filled = numeric_df.fillna(numeric_df.median())
    
    # contamination is the expected proportion of outliers
    model = IsolationForest(contamination=0.05, random_state=42)
    preds = model.fit_predict(numeric_filled)
    
    anomalies = []
    anomaly_indices = np.where(preds == -1)[0]
    
    for idx in anomaly_indices[:10]: # Limit to top 10
        row = df.iloc[idx]
        anomalies.append({
            "index": int(idx),
            "data": row.to_dict(),
            "reason": "Comportamiento inusual detectado en métricas numéricas (Outlier)"
        })
        
    return anomalies

def check_fraud_signals(df: pd.DataFrame) -> List[str]:
    """Check for simple fraud signals in transaction data."""
    signals = []
    cols = [c.lower() for c in df.columns]
    
    # Check for duplicate transactions if it looks like finance/sales
    if any(c in cols for c in ["monto", "amount", "price", "precio"]):
        # Find potential duplicate transactions (same amount, same customer, close time if available)
        # For now, just look for very frequent identical amounts
        amount_col = next(c for c in df.columns if c.lower() in ["monto", "amount", "price", "precio"])
        counts = df[amount_col].value_counts()
        high_freq = counts[counts > (len(df) * 0.1)].index.tolist()
        if high_freq and len(df) > 20:
            signals.append(f"Alerta de duplicidad: El monto {high_freq[0]} se repite inusualmente (posible error o fraude).")
            
    return signals
