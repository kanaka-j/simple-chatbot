from google import genai
from app.core.config import settings

# Validate settings before creating client
settings.validate()

# Initialize a single Gemini Client instance (Singleton Pattern)
# This prevents creating multiple connections across different requests
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
