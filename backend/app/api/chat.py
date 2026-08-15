from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.rag.retrieval_service import retrieve_similar_chunks, generate_rag_answer

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/rag", response_model=ChatResponse)
def rag_chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Temporary standalone RAG endpoint. 
    Will be replaced by the AI Orchestrator in Phase 6.
    """
    try:
        # 1. Retrieve
        chunks = retrieve_similar_chunks(db, query=request.message, user_id=str(current_user.id), top_k=5)
        
        if not chunks:
            return ChatResponse(
                answer="I couldn't find any relevant information in your uploaded documents to answer this question.",
                sources=[]
            )
            
        # 2. Generate
        result = generate_rag_answer(request.message, chunks)
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")
