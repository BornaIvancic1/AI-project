from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.qa_service import answer_question
from app.services.ner_service import extract_entities  # Import your NER service
from app.storage.storage_service import get_all_texts

router = APIRouter()

class Entity(BaseModel):
    entity_group: str
    word: str
    start: int
    end: int
    score: float

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    entities: List[Entity]

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    texts = get_all_texts()
    if not texts:
        raise HTTPException(status_code=400, detail="No documents uploaded yet.")
    context = "\n".join(texts)
    answer = answer_question(request.question, context)
    entities_raw = extract_entities(answer)
    entities = [
        Entity(
            entity_group=e.get("entity_group", ""),
            word=e.get("word", ""),
            start=e.get("start", 0),
            end=e.get("end", 0),
            score=float(e.get("score", 0))
        )
        for e in entities_raw
    ]
    return AskResponse(answer=answer, entities=entities)
