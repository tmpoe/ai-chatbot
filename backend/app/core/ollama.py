import httpx
from typing import AsyncGenerator, Any
import json
import os


class OllamaLLM:
    """Ollama LLM integration with streaming support."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    async def generate_stream(
        self,
        messages: list[dict[str, str]],
        model_name: str,
        tools: list[dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Ollama.
        
        Args:
            messages: List of chat messages
            model_name: Ollama model to use (e.g., 'llama3.2:3b')
            tools: Optional list of tools (Ollama supports function calling)
        
        Yields:
            Chunks of generated text
        """
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Prepare request payload
        payload = {
            "model": model_name,
            "messages": ollama_messages,
            "stream": True
        }
        
        # Add tools if provided (Ollama supports function calling)
        if tools:
            payload["tools"] = self._convert_tools_to_ollama_format(tools)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                chunk_data = json.loads(line)
                                if "message" in chunk_data:
                                    content = chunk_data["message"].get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.ConnectError as e:
            print(f"❌ Error connecting to Ollama at {self.base_url}: {e}")
            yield f"Error: Could not connect to Ollama at {self.base_url}. Make sure Ollama is running and accessible."
        except httpx.HTTPError as e:
            print(f"❌ HTTP error from Ollama: {e}")
            yield f"Error: Ollama returned an error. The model may not be installed. Try: docker exec -it chatbot-ollama ollama pull {model_name}"
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            yield "Something went wrong. Please try again later."
    
    def _convert_tools_to_ollama_format(self, tools: list[dict[str, Any]]) -> list[dict]:
        """Convert MCP tools to Ollama function calling format."""
        ollama_tools = []
        
        for tool in tools:
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool.get("input_schema", {})
                }
            }
            ollama_tools.append(ollama_tool)
        
        return ollama_tools


# Global Ollama instance
ollama_llm = OllamaLLM()
