from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    """Represents a single message in a conversation."""
    role: Literal["user", "model", "assistant"] = Field(
        ..., 
        description="The role of the speaker. Use 'user' for human, 'model' or 'assistant' for AI."
    )
    content: str = Field(
        ..., 
        min_length=1, 
        description="The text content of the message."
    )

class ChatRequest(BaseModel):
    """Request payload sent by client frontends."""
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=10000, 
        description="The latest user message to send to the AI."
    )
    history: Optional[List[ChatMessage]] = Field(
        default=[], 
        description="Optional previous chat history for multi-turn conversation memory."
    )
    system_instruction: Optional[str] = Field(
        default=None, 
        description="Optional custom persona or behavioral rules for the AI."
    )
    temperature: Optional[float] = Field(
        default=0.7, 
        ge=0.0, 
        le=2.0, 
        description="Creativity parameter: 0.0 (precise) to 2.0 (creative)."
    )
    model: Optional[str] = Field(
        default="gemini-3.6-flash",
        description="Gemini model name to use for generation."
    )

class ChatResponse(BaseModel):
    """Structured response returned back to the client."""
    reply: str = Field(..., description="The AI's generated text answer.")
    model_used: str = Field(..., description="The specific model that generated the answer.")
    status: str = Field(default="success", description="Status of the request.")
