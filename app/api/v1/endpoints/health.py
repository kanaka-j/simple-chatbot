from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", summary="Health Check")
def health_check():
    """
    Returns server health status and active configuration.
    Used by monitoring systems (Kubernetes, AWS ALB, Datadog).
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }
