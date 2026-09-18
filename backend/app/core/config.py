import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "Universal Business Review Analyzer & Sentiment Intelligence System"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Absolute Paths
    BASE_DIR: Path = BASE_DIR
    ROOT_DIR: Path = ROOT_DIR
    MODEL_PATH: str = str(ROOT_DIR / "models" / "business_sentiment_pipeline.joblib")
    METADATA_PATH: str = str(ROOT_DIR / "models" / "model_metadata.json")
    DATABASE_PATH: str = str(ROOT_DIR / "backend" / "app" / "db" / "history.db")
    FRONTEND_DIR: str = str(ROOT_DIR / "frontend")
    
    # Security & CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    # Critical Severity Triggers
    CRITICAL_SEVERITY_KEYWORDS: list[str] = [
        "food poisoning", "scam", "fraud", "illegal", "threatened",
        "blisters", "injury", "dangerous", "unhygienic", "terrible hygiene",
        "damaged my property", "broke immediately", "emergency clinic", "hazard"
    ]

settings = Settings()
