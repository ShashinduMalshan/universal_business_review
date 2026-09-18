from fastapi import APIRouter
from backend.app.models.pipeline_manager import PipelineManager
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["System Telemetry"])
def health_check():
    manager = PipelineManager.get_instance()
    return {
        "status": "healthy" if manager.is_loaded else "degraded",
        "model_loaded": manager.is_loaded,
        "version": settings.VERSION,
        "model_name": manager.metadata.get("model_name", "Logistic Regression") if manager.metadata else "Unknown"
    }

@router.get("/ready", tags=["System Telemetry"])
def readiness_check():
    manager = PipelineManager.get_instance()
    return {
        "ready": manager.is_loaded,
        "sample_count": manager.metadata.get("sample_count", 100000) if manager.metadata else 0
    }

@router.get("/info", tags=["System Telemetry"])
def model_info():
    manager = PipelineManager.get_instance()
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "classes": manager.metadata.get("classes", ["Negative", "Neutral", "Positive"]) if manager.metadata else [],
        "metrics": manager.metadata.get("metrics", []) if manager.metadata else [],
        "feature_count": manager.metadata.get("num_features", 0) if manager.metadata else 0
    }
