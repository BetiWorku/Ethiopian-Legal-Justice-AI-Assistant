from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scripts.chatbot import chat


app = FastAPI(
    title="Ethiopian Legal Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Ethiopian Legal Assistant API is running"
    }


@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    answer = chat(request.question)

    return {
        "question": request.question,
        "answer": answer
    }