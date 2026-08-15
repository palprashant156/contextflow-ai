import mlflow.sklearn
import os

# We will cache the model in memory to avoid reloading it from MLflow on every request
_classifier_model = None

def get_classifier_model():
    global _classifier_model
    if _classifier_model is None:
        try:
            # Assuming MLflow tracking server is running at localhost:5000
            mlflow.set_tracking_uri("http://localhost:5000")
            
            # Load the latest version of the registered model
            model_uri = "models:/DocumentClassifierModel/latest"
            _classifier_model = mlflow.sklearn.load_model(model_uri)
        except Exception as e:
            print(f"Warning: Could not load MLflow model: {e}")
            return None
            
    return _classifier_model

def predict_document_category(text: str) -> str:
    """
    Predicts the category of a document text using the MLflow registered model.
    Falls back to 'Unknown' if model cannot be loaded.
    """
    model = get_classifier_model()
    if not model:
        return "Unknown"
        
    try:
        prediction = model.predict([text])
        return prediction[0]
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Unknown"
