from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

# 1. Initialize the FastAPI Application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade API backend for Google Gemini AI with clean layered architecture.",
    docs_url="/docs",       # Interactive Swagger UI documentation
    redoc_url="/redoc"      # Alternative ReDoc documentation
)

# 2. Configure CORS (Cross-Origin Resource Sharing)
# Allows frontends running on different ports/domains (e.g. React on :3000, Streamlit on :8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount the API v1 Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# 4. Root Welcome Route
@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} 🚀",
        "version": settings.VERSION,
        "docs": "/docs",
        "api_v1": settings.API_V1_PREFIX
    }

# Entrypoint for running with `python app/main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
