from fastapi import APIRouter
from app.api.v1.endpoints import health, chat, vision 


api_router = APIRouter()

# Register endpoint routers
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(chat.router, prefix="/ai", tags=["Gemini AI"])
api_router.include_router(vision.router, prefix="/ai", tags=["Multimodal Vision"])

