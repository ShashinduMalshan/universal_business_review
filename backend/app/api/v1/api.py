from fastapi import APIRouter
from backend.app.api.v1.endpoints import predict, analytics, history, system

api_router = APIRouter()
api_router.include_router(system.router, prefix="", tags=["System Telemetry"])
api_router.include_router(predict.router, prefix="", tags=["Inference"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(history.router, prefix="/history", tags=["Audit History"])
