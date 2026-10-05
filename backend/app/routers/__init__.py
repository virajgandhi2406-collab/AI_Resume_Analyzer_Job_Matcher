from app.routers.auth_router import router as auth_router
from app.routers.resumes_router import router as resumes_router
from app.routers.jobs_router import router as jobs_router
from app.routers.match_router import router as match_router
from app.routers.ai_tools_router import router as ai_tools_router
from app.routers.tracker_router import router as tracker_router
from app.routers.analytics_router import router as analytics_router

__all__ = [
    "auth_router",
    "resumes_router",
    "jobs_router",
    "match_router",
    "ai_tools_router",
    "tracker_router",
    "analytics_router"
]
