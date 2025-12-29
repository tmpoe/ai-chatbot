from typing import AsyncGenerator
from app.core.llm import gemini_llm
from app.core.ollama import ollama_llm
from app.services.mcp_service import mcp_service
from app.models.chat import Message


class ChatService:
    """Service for orchestrating chat with MCP tools and LLM."""
    
    def _get_llm_provider(self, model: str):
        """Determine which LLM provider to use based on model name."""
        if model.startswith("ollama:"):
            return ollama_llm, model.replace("ollama:", "")
        else:
            # Default to Gemini
            return gemini_llm, model
    
    async def chat_stream(
        self,
        messages: list[Message],
        model: str
    ) -> AsyncGenerator[str, None]:
        """
        Process chat messages and stream response.
        
        Args:
            messages: List of chat messages
            model: Model identifier (e.g., 'gemini-2.0-flash-exp' or 'ollama:llama3.2:3b')
        
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
        
        # Get the appropriate LLM provider
        llm_provider, actual_model = self._get_llm_provider(model)
        
        # Generate streaming response with tools
        async for chunk in llm_provider.generate_stream(
            messages=message_dicts,
            model_name=actual_model,
            tools=tools if tools else None
        ):
            yield chunk


# Global chat service instance
chat_service = ChatService()
