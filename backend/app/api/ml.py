from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.ml.classification_service import predict_document_category

router = APIRouter()

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    category: str

@router.post("/predict", response_model=PredictionResponse)
def predict_category(request: PredictionRequest, current_user: User = Depends(get_current_user)):
    """
    Endpoint to predict a document's category using the ML model.
    """
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    category = predict_document_category(request.text)
    return PredictionResponse(category=category)

@router.get("/models")
def get_ml_models(current_user: User = Depends(get_current_user)):
    """
    Returns a list of available models for the frontend ML dashboard.
    """
    return [
        {
            "name": "Document Classifier",
            "type": "Logistic Regression + TF-IDF",
            "status": "Active",
            "accuracy": "87.5%",
            "last_trained": "2026-08-15"
        }
    ]
