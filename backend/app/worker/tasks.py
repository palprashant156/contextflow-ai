from app.worker.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.document import Document, DocumentStatus
from app.models.chunk import DocumentChunk
from app.services.rag.pdf_service import extract_text_from_pdf
from app.services.vision.opencv_service import preprocess_image_for_ocr
from app.services.vision.ocr_service import extract_text_from_image
from app.services.rag.chunking_service import chunk_document_text
from app.services.rag.embedding_service import generate_embeddings

@celery_app.task(bind=True, max_retries=3)
def process_document_task(self, document_id: str, file_bytes: bytes, mime_type: str):
    """
    Celery background task for processing uploaded documents:
    Text extraction, chunking, and pgvector embeddings.
    """
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == document_id).first()
    
    if not doc:
        db.close()
        return "Document not found"

    try:
        extracted_text = ""
        
        # 1. Extraction
        if mime_type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_bytes)
        elif mime_type in ["image/png", "image/jpeg", "image/jpg"]:
            preprocessed_img = preprocess_image_for_ocr(file_bytes)
            extracted_text = extract_text_from_image(preprocessed_img)
            
        doc.text_content = extracted_text
        
        # 2. Chunking & Embedding
        chunks = chunk_document_text(extracted_text)
        if chunks:
            embeddings = generate_embeddings(chunks)
            chunk_objects = []
            for i, chunk_text in enumerate(chunks):
                chunk_objects.append(DocumentChunk(
                    document_id=doc.id,
                    content=chunk_text,
                    embedding=embeddings[i]
                ))
            db.bulk_save_objects(chunk_objects)
        
        # 3. Mark Completed
        doc.status = DocumentStatus.COMPLETED
        db.commit()
        return f"Successfully processed document {document_id}"
        
    except Exception as exc:
        doc.status = DocumentStatus.FAILED
        db.commit()
        # Retry logic for transient failures (e.g., API limits on embeddings)
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()
