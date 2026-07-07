from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import analyzer, utils
import io

app = FastAPI(title="Analytics Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_dataset(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        file_obj = io.BytesIO(file_bytes)
        file_obj.name = file.filename

        df = analyzer.load_csv(file_obj)
        
        summary = analyzer.dataset_summary(df)
        cols = analyzer.column_info(df)
        health = analyzer.evaluate_business(summary)
        trends = analyzer.analyze_numeric_trends(df)
        correlations = analyzer.compute_correlations(df)
        
        industry = analyzer.detect_industry(df)
        business_context = analyzer.get_business_context(df, industry)
        critical_variables = analyzer.detect_critical_variables(df)
        anomalies = analyzer.detect_anomalies(df)
        fraud_signals = analyzer.check_fraud_signals(df)
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        forecasts = {}
        for col in numeric_cols[:2]:
            try:
                f = analyzer.simple_forecast(df, col)
                if f:
                    forecasts[col] = f
            except Exception as e:
                pass

        charts = analyzer.get_chart_data(df)
        preview = analyzer.get_preview(df)
        kpis = analyzer.get_kpis(df)

        context = {
            "file_name": file.filename,
            "summary": summary,
            "columns": cols,
            "health": health,
            "trends": trends,
            "correlations": correlations,
            "charts": charts,
            "preview": preview,
            "kpis": kpis,
            "industry": industry,
            "business_context": business_context,
            "critical_variables": critical_variables,
            "anomalies": anomalies,
            "fraud_signals": fraud_signals,
            "forecasts": forecasts
        }

        safe_context = utils.make_json_safe(context)
        return safe_context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
