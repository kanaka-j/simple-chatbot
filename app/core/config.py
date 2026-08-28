import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

class Settings:
    """
    Central application configuration.
    Reads from environment variables and sets defaults.
    """
    PROJECT_NAME: str = "Enterprise Gemini AI Backend"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-3.6-flash")
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

    def validate(self):
        """Ensures critical configurations are present before booting up."""
        if not self.GEMINI_API_KEY:
            raise ValueError(
                "❌ GEMINI_API_KEY is not set. Please add it to your .env file."
            )

# Create a single instance to be shared across the entire app
settings = Settings()
