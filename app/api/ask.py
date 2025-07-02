from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qa_service import answer_question
from app.storage.storage_service import get_all_texts

router = APIRouter()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    texts = get_all_texts()
    if not texts:
        raise HTTPException(status_code=400, detail="No documents uploaded yet.")
    context = "\n".join(texts)
    answer = answer_question(request.question, context)
    return AskResponse(answer=answer)
