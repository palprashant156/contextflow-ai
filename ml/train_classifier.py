import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import os

# Set MLflow tracking URI (assuming it runs via Docker on localhost:5000)
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("document-classification")

def create_sample_dataset():
    """Creates a sample reproducible dataset for document classification."""
    data = {
        "text": [
            "Employees are entitled to 15 days of paid annual leave.",
            "The company's sick leave policy allows for 5 days of paid sick leave.",
            "Invoice #10293 for marketing services rendered in Q3.",
            "Please find attached the Q4 financial report detailing our profits.",
            "The software architecture relies on microservices and Kubernetes.",
            "The new API endpoints require JWT authentication.",
            "Notice of termination of employment contract.",
            "Total amount due for server hosting is $450.00.",
            "Q1 revenue increased by 15% compared to last year.",
            "This document outlines the standard operating procedure for onboarding."
        ],
        "label": [
            "Policy", "Policy", "Invoice", "Financial", "Technical", 
            "Technical", "HR", "Invoice", "Financial", "HR"
        ]
    }
    return pd.DataFrame(data)

def train_model():
    print("Preparing sample dataset...")
    df = create_sample_dataset()
    
    X = df["text"]
    y = df["label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(random_state=42, max_iter=100))
    ])
    
    print("Starting MLflow run...")
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("vectorizer", "TF-IDF")
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        predictions = pipeline.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        
        print(f"Accuracy: {acc:.4f}")
        
        # Log metrics
        mlflow.log_metric("accuracy", acc)
        
        # Save model to MLflow artifact store
        mlflow.sklearn.log_model(
            sk_model=pipeline, 
            artifact_path="document_classifier",
            registered_model_name="DocumentClassifierModel"
        )
        
        print(f"Run {run.info.run_id} completed successfully.")
        print("Model registered as 'DocumentClassifierModel'")

if __name__ == "__main__":
    train_model()
