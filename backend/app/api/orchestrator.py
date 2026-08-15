from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.orchestrator.workflow import orchestrate_query

router = APIRouter()

class OrchestratorRequest(BaseModel):
    message: str

class OrchestratorResponse(BaseModel):
    answer: str
    sources: List[str]
    analysis_steps: List[str]
    engine: str

@router.post("/query", response_model=OrchestratorResponse)
def unified_query_endpoint(request: OrchestratorRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Unified entry point for CortexFlow AI.
    It automatically routes the request to RAG, SQL, ML, or a Complex Workflow.
    """
    try:
        result = orchestrate_query(db, request.message, str(current_user.id))
        
        return OrchestratorResponse(
            answer=result["answer"],
            sources=result["sources"],
            analysis_steps=result["analysis_steps"],
            engine=result["engine"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator Error: {str(e)}")
