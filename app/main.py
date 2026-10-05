"""FastAPI application for the BFSI assistant."""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.agent import process_question
from app.llm import is_configured
from app.rag import FAQ_FILE

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"

app = FastAPI(title="BFSI AI Service Agent", version="2.0.0")


def load_questions() -> list[dict]:
    with QUESTIONS_FILE.open(encoding="utf-8") as file:
        questions = json.load(file)
    if not isinstance(questions, list) or any(
        not isinstance(item, dict) or not all(key in item for key in ("id", "question", "category", "type"))
        for item in questions
    ):
        raise RuntimeError("Question catalog has an invalid format.")
    if len({item["id"] for item in questions}) != len(questions):
        raise RuntimeError("Question catalog contains duplicate IDs.")
    return questions


questions = load_questions()


class HistoryMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    role: str
    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    question_id: str = Field(min_length=1, max_length=100)
    history: list[HistoryMessage] = Field(default_factory=list, max_length=20)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    knowledge_ready = FAQ_FILE.is_file() and FAQ_FILE.stat().st_size > 0
    provider_ready = is_configured()
    return {
        "status": "ok" if knowledge_ready and provider_ready else "degraded",
        "service": "BFSI AI Service Agent",
        "knowledge_base": "ready" if knowledge_ready else "unavailable",
        "answer_provider": "configured" if provider_ready else "unconfigured",
    }


@app.get("/questions")
def get_questions():
    return {"questions": questions}


@app.post("/chat")
def chat(request: ChatRequest):
    selected_question = next(
        (item for item in questions if item["id"] == request.question_id), None
    )
    if selected_question is None:
        raise HTTPException(status_code=400, detail="Invalid BFSI question selected.")

    history = [message.model_dump() for message in request.history]
    return process_question(selected_question, history)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
