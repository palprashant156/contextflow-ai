from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import magic

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse
from app.worker.tasks import process_document_task

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Read bytes
    file_bytes = await file.read()
    
    # Validate MIME type safely
    mime_type = magic.from_buffer(file_bytes, mime=True)
    allowed_types = ["application/pdf", "image/png", "image/jpeg", "image/jpg"]
    
    if mime_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {mime_type}")
        
    # Save to database initially
    doc = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_type=mime_type,
        status=DocumentStatus.PROCESSING
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Hand off to Celery Worker
    process_document_task.delay(str(doc.id), file_bytes, mime_type)
    
    return doc

@router.get("/", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()
