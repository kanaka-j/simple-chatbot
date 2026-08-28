from typing import AsyncGenerator, List
from google.genai import types
from app.core.client import gemini_client
from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessage

class GeminiService:
    """
    Business & AI Orchestration layer for Google Gemini.
    Handles prompt assembly, history formatting, and SDK invocation.
    """

    @staticmethod
    def _build_contents(message: str, history: List[ChatMessage]) -> List[types.Content]:
        """Converts chat history + new message into Google GenAI SDK Content objects."""
        contents: List[types.Content] = []
        
        # Add past history if provided
        for msg in history:
            role = "user" if msg.role == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.content)]
                )
            )
            
        # Add current user prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)]
            )
        )
        return contents

    @classmethod
    def analyze_image(cls, image_bytes:bytes, mime_type:str, prompt:str="Describe this image in detail.") -> str:
           """
            Processes an image with a text prompt using Gemini's multimodal capabilities.
            """
           image_part= types.Part.from_bytes(
               data=image_bytes,
               mime_type=mime_type
           )
           #Text prompt part
           text_part = types.Part.from_text(text=prompt)

           #Call gemini model with both parts
           response = gemini_client.models.generate_content(
                model=settings.DEFAULT_MODEL,
                contents=[image_part, text_part]
           )
           return response.text or "No description could be generated."




    @classmethod
    def generate_chat(cls, request: ChatRequest) -> ChatResponse:
        """
        Synchronous / Standard Generation endpoint.
        Returns the complete response once generated.
        """
        contents = cls._build_contents(request.message, request.history or [])
        
        # Configure system instructions and temperature
        config = types.GenerateContentConfig(
            system_instruction=request.system_instruction,
            temperature=request.temperature or settings.DEFAULT_TEMPERATURE
        )
        
        model_name = request.model or settings.DEFAULT_MODEL

        # Call Gemini SDK
        response = gemini_client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config
        )

        return ChatResponse(
            reply=response.text or "",
            model_used=model_name,
            status="success"
        )

    @classmethod
    def generate_chat_stream(cls, request: ChatRequest):
        """
        Generator for Server-Sent Events (SSE) streaming token-by-token.
        """
        contents = cls._build_contents(request.message, request.history or [])
        
        config = types.GenerateContentConfig(
            system_instruction=request.system_instruction,
            temperature=request.temperature or settings.DEFAULT_TEMPERATURE
        )
        
        model_name = request.model or settings.DEFAULT_MODEL

        response_stream = gemini_client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config
        )

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

# Export a single service instance
gemini_service = GeminiService()
