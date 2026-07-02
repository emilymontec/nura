from typing import Dict


def health_score(summary: Dict[str, int]) -> float:
    rows = summary.get("rows", 0)
    cols = summary.get("columns", 0)
    total_cells = rows * cols if rows > 0 and cols > 0 else 1
    total_missing = summary.get("total_missing", 0)
    duplicate_rows = summary.get("duplicate_rows", 0)
    if rows == 0:
        return 0.0
    missing_percent = (total_missing / total_cells) * 100
    duplicate_percent = (duplicate_rows / rows) * 100
    penalty = (missing_percent * 0.5) + (duplicate_percent * 0.3)
    score = max(0.0, 100.0 - penalty)
    return round(score, 2)


def risk_level(score: float) -> str:
    if score >= 80:
        return "bajo"
    if score >= 50:
        return "moderado"
    return "alto"


def evaluate_business(df_summary: Dict) -> Dict:
    score = health_score(df_summary)
    risk = risk_level(score)
    return {"health_score": score, "risk_level": risk}
