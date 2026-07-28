from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scripts.rag_pipeline import generate_legal_answer


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
        "message":"Ethiopian Legal Assistant API is running"
    }



@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    try:

        result = generate_legal_answer(
            request.question
        )

        return {
            "question": request.question,
            "result": result
        }


    except Exception as e:

        print("API ERROR:", e)

        return {
            "error": str(e)
        }