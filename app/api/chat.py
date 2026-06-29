from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


from app.services.search_service import search
from app.services.search_service import retrieve_context
from app.services.gemini_service import generate_answer

@router.post("/")
def chat(request: ChatRequest):

    context, sources = retrieve_context(request.question)

    answer = generate_answer(
        context=context,
        question=request.question
    )

    return {
        "answer": answer,
        "sources": sources
    }