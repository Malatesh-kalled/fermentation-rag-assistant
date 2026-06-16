from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.ingestion import build_vector_store
from app.rag import answer_question

app = FastAPI(
    title="Fermentation RAG Assistant",
    description="RAG API for answering questions from fermentation research papers.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)


class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "papers_dir": str(settings.papers_dir),
        "chroma_dir": str(settings.chroma_dir),
        "model": settings.groq_model,
        "top_k": settings.top_k,
    }


@app.post("/ingest")
def ingest_documents(force_rebuild: bool = True):
    try:
        build_vector_store(force_rebuild=force_rebuild)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"status": "indexed", "papers_dir": str(settings.papers_dir)}


@app.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    try:
        answer = answer_question(payload.question)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AskResponse(question=payload.question, answer=answer)
