from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from . import llm


app = FastAPI(title="AI Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateReportRequest(BaseModel):
    context: Dict[str, Any]


class ChatWithDataRequest(BaseModel):
    question: str
    context: Dict[str, Any]
    history: str = ""


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate-report")
def generate_report(request: GenerateReportRequest):
    try:
        report = llm.generate_ai_report(request.context)
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
def chat_with_data(request: ChatWithDataRequest):
    try:
        response = llm.chat_with_data(request.question, request.context, request.history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
