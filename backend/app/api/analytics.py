from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.chunk import DocumentChunk

router = APIRouter()

class AnalyticsResponse(BaseModel):
    total_documents: int
    documents_processed: int
    total_chunks: int
    rag_queries: int
    sql_queries: int
    ml_predictions: int

@router.get("/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Provides aggregated analytics for the frontend dashboard.
    """
    total_docs = db.query(Document).filter(Document.user_id == current_user.id).count()
    docs_processed = db.query(Document).filter(
        Document.user_id == current_user.id, 
        Document.status == "COMPLETED"
    ).count()
    
    # Total chunks across all user's documents
    total_chunks = db.query(DocumentChunk).join(Document).filter(Document.user_id == current_user.id).count()
    
    # In a real app, these query counts would come from a `retrieval_logs` or `workflow_runs` table.
    # For MVP, we simulate the metrics based on document activity.
    return AnalyticsResponse(
        total_documents=total_docs,
        documents_processed=docs_processed,
        total_chunks=total_chunks,
        rag_queries=532, # Simulated
        sql_queries=187, # Simulated
        ml_predictions=123 # Simulated
    )
