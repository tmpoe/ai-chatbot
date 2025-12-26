from typing import AsyncGenerator
from app.core.llm import gemini_llm
from app.services.mcp_service import mcp_service
from app.models.chat import Message


class ChatService:
    """Service for orchestrating chat with MCP tools and LLM."""
    
    async def chat_stream(
        self,
        messages: list[Message],
        model: str
    ) -> AsyncGenerator[str, None]:
        """
        Process chat messages and stream response.
        
        Args:
            messages: List of chat messages
            model: Gemini model to use
        
        Yields:
            Chunks of generated text
        """
        # Initialize MCP service if needed
        if not mcp_service._initialized:
            await mcp_service.initialize()
        
        # Get available tools from MCP
        tools = mcp_service.get_tools()
        
        # Convert messages to dict format
        message_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Generate streaming response with tools
        async for chunk in gemini_llm.generate_stream(
            messages=message_dicts,
            model_name=model,
            tools=tools if tools else None
        ):
            yield chunk


# Global chat service instance
chat_service = ChatService()
