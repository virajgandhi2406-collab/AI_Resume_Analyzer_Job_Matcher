import sys
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models import user, resume, job, match, application
from app.routers import (
    auth_router,
    resumes_router,
    jobs_router,
    match_router,
    ai_tools_router,
    tracker_router,
    analytics_router,
)
from app.services.sample_data_service import seed_sample_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_resume_analyzer")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database Tables
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Auto seed jobs if database is clean
    try:
        db = SessionLocal()
        seed_sample_jobs(db)
        db.close()
        logger.info("Sample database records initialized successfully.")
    except Exception as e:
        logger.warning(f"Could not auto-seed sample records on startup: {e}")
        
    yield
    # Shutdown logic if any
    logger.info("Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Full-featured AI Resume Analyzer, ATS Score Optimizer, and Intelligent Job Matcher Platform.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Routers
api_v1_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(resumes_router, prefix=api_v1_prefix)
app.include_router(jobs_router, prefix=api_v1_prefix)
app.include_router(match_router, prefix=api_v1_prefix)
app.include_router(ai_tools_router, prefix=api_v1_prefix)
app.include_router(tracker_router, prefix=api_v1_prefix)
app.include_router(analytics_router, prefix=api_v1_prefix)

# Mount Uploads directory for static file access
if settings.UPLOAD_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")

# Frontend static asset serving
frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_path.exists():
    css_path = frontend_path / "css"
    js_path = frontend_path / "js"
    if css_path.exists():
        app.mount("/css", StaticFiles(directory=str(css_path)), name="frontend-css")
    if js_path.exists():
        app.mount("/js", StaticFiles(directory=str(js_path)), name="frontend-js")
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="frontend-static")

    @app.get("/app", tags=["Frontend App"], include_in_schema=False)
    def serve_frontend():
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return JSONResponse(status_code=404, content={"detail": "Frontend index.html not found"})

@app.get("/", tags=["Root"])
def root_endpoint():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "docs_url": "/docs",
        "api_v1_prefix": settings.API_V1_STR,
        "available_endpoints": [
            f"{settings.API_V1_STR}/resumes/upload",
            f"{settings.API_V1_STR}/resumes/analyze-text",
            f"{settings.API_V1_STR}/jobs",
            f"{settings.API_V1_STR}/match/match-single",
            f"{settings.API_V1_STR}/match/batch-match/{{resume_id}}",
            f"{settings.API_V1_STR}/ai-tools/cover-letter",
            f"{settings.API_V1_STR}/ai-tools/interview-prep",
            f"{settings.API_V1_STR}/ai-tools/optimize-bullets",
            f"{settings.API_V1_STR}/ai-tools/career-roadmap",
            f"{settings.API_V1_STR}/tracker",
            f"{settings.API_V1_STR}/analytics/dashboard-summary"
        ]
    }

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_provider_mode": settings.DEFAULT_AI_PROVIDER
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
