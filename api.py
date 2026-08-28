"""
Main API Entrypoint
To start the server, run:
    uvicorn app.main:app --reload --port 8000
or:
    python api.py
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting Gemini Chatbot API server at http://127.0.0.1:8000")
    print("📖 Interactive API Docs available at http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
