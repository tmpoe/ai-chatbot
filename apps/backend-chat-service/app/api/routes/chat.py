from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.chat import ChatRequest
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint with streaming support.
    
    Accepts chat messages and streams back the AI response.
    Supports MCP tool calling for file access and other capabilities.
    """
    try:
        # Stream response
        async def generate():
            async for chunk in chat_service.chat_stream(
                messages=request.messages,
                model=request.model
            ):
                # Format as SSE (Server-Sent Events)
                yield f"0:{chunk}\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-chatbot-backend"}
