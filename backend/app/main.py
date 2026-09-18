import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.exceptions import (
    ModelNotLoadedException, InvalidInputException,
    model_not_loaded_handler, invalid_input_handler
)
from backend.app.api.v1.api import api_router
from backend.app.db.database import init_db
from backend.app.models.pipeline_manager import PipelineManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing SQLite database...")
    init_db()
    logger.info("Loading Machine Learning Pipeline...")
    PipelineManager.get_instance()
    logger.info("Universal Business Review Analyzer Backend is READY.")
    yield

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Industrial-grade domain-agnostic customer sentiment intelligence API.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception Handlers
    app.add_exception_handler(ModelNotLoadedException, model_not_loaded_handler)
    app.add_exception_handler(InvalidInputException, invalid_input_handler)
    
    # Include API Routers (/api/v1/... and legacy /api/...)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(api_router, prefix="/api")  # Backward compatibility
    
    # System root routes
    @app.get("/health", tags=["System Telemetry"])
    def root_health():
        manager = PipelineManager.get_instance()
        return {
            "status": "healthy" if manager.is_loaded else "degraded",
            "model_name": manager.metadata.get("model_name", "Logistic Regression") if manager.metadata else "Unknown",
            "classes": manager.metadata.get("classes", ["Negative", "Neutral", "Positive"]) if manager.metadata else []
        }
        
    @app.get("/ready", tags=["System Telemetry"])
    def root_ready():
        manager = PipelineManager.get_instance()
        return {"ready": manager.is_loaded}
        
    # Mount Frontend Static Assets
    if os.path.exists(settings.FRONTEND_DIR):
        app.mount("/static", StaticFiles(directory=settings.FRONTEND_DIR), name="static")
        
        @app.get("/", include_in_schema=False)
        def serve_dashboard():
            return FileResponse(os.path.join(settings.FRONTEND_DIR, "index.html"))
            
    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
