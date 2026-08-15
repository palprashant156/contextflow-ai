from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CortexFlow AI"
    
    # Database
    DATABASE_URL: str = "postgresql://cortexflow:cortexflow_password@127.0.0.1:5432/cortexflow_db"
    
    # Security
    JWT_SECRET: str = "supersecret_dev_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours
    # Message Broker
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
