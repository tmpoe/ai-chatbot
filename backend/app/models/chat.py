from pydantic import BaseModel


class Message(BaseModel):
    """Chat message model."""
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    messages: list[Message]
    model: str = "gemini-2.0-flash-exp"


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str
    model: str
