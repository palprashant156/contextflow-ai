from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentDetail(DocumentResponse):
    text_content: Optional[str] = None
