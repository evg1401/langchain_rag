import threading
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from chunker.pdf import chunk_pdf
import uuid
from app.entry import ask

app = FastAPI()

def rag_ask(question: str) -> str:
    return ask(question)

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = None


@app.post("/v1/chunker/chunk_pdf")
def start_chunk_pdf():
    thread = threading.Thread(target=chunk_pdf)
    thread.start()

    return "ok"

@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {
                "id": "my-rag",
                "object": "model",
                "owned_by": "my-company"
            }
        ]
    }

@app.post("/v1/chat/completions")
def chat_completions(request: ChatRequest):
    # последнее сообщение пользователя
    user_message = next(
        (
            m.content
            for m in reversed(request.messages)
            if m.role == "user"
        ),
        ""
    )

    answer = rag_ask(user_message)

    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer
                },
                "finish_reason": "stop"
            }
        ]
    }