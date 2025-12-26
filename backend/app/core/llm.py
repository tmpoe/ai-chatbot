import google.generativeai as genai
from typing import AsyncGenerator, Any
import json

from app.core.config import settings


class GeminiLLM:
    """Gemini LLM integration with tool calling support."""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.google_api_key)
        self.model_cache = {}
    
    def _get_model(self, model_name: str):
        """Get or create Gemini model instance."""
        if model_name not in self.model_cache:
            self.model_cache[model_name] = genai.GenerativeModel(model_name)
        return self.model_cache[model_name]
    
    def _convert_tools_to_gemini_format(self, tools: list[dict[str, Any]]) -> list[dict]:
        """Convert MCP tools to Gemini function calling format."""
        gemini_tools = []
        
        for tool in tools:
            # Get input schema and clean it
            input_schema = tool.get("input_schema", {})
            
            # Remove fields that Gemini doesn't support
            cleaned_schema = self._clean_schema(input_schema)
            
            gemini_tool = {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": cleaned_schema
            }
            gemini_tools.append(gemini_tool)
        
        return gemini_tools
    
    def _clean_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Remove fields from schema that Gemini doesn't support."""
        from google.ai.generativelanguage import Type
        
        if not schema:
            return {"type": Type.OBJECT, "properties": {}}
        
        # Create a copy to avoid modifying original
        cleaned = {}
        
        # Map string types to Gemini Type enum
        type_mapping = {
            "object": Type.OBJECT,
            "string": Type.STRING,
            "number": Type.NUMBER,
            "integer": Type.INTEGER,
            "boolean": Type.BOOLEAN,
            "array": Type.ARRAY,
        }
        
        # Only include fields that Gemini supports
        supported_fields = ["type", "properties", "required", "description", "items", "enum"]
        for field in supported_fields:
            if field in schema:
                if field == "type":
                    # Convert string type to enum
                    type_str = schema[field].lower() if isinstance(schema[field], str) else "object"
                    cleaned[field] = type_mapping.get(type_str, Type.OBJECT)
                else:
                    cleaned[field] = schema[field]
        
        # Ensure type is set (default to OBJECT if not specified)
        if "type" not in cleaned:
            cleaned["type"] = Type.OBJECT
        
        # Recursively clean nested properties
        if "properties" in cleaned and isinstance(cleaned["properties"], dict):
            cleaned["properties"] = {
                key: self._clean_schema(value) if isinstance(value, dict) else value
                for key, value in cleaned["properties"].items()
            }
        
        # Clean items for arrays
        if "items" in cleaned and isinstance(cleaned["items"], dict):
            cleaned["items"] = self._clean_schema(cleaned["items"])
        
        return cleaned
    
    async def generate_stream(
        self,
        messages: list[dict[str, str]],
        model_name: str,
        tools: list[dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Gemini.
        
        Args:
            messages: List of chat messages
            model_name: Gemini model to use
            tools: Optional list of tools for function calling
        
        Yields:
            Chunks of generated text
        """
        model = self._get_model(model_name)
        
        # Convert messages to Gemini format
        # Gemini expects: [{"role": "user", "parts": ["text"]}, ...]
        gemini_messages = []
        for msg in messages:
            gemini_messages.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })
        
        # Prepare generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        # Add tools if provided
        gemini_tools = None
        if tools:
            gemini_tools = self._convert_tools_to_gemini_format(tools)
        
        try:
            # Debug: Print tool schemas
            if gemini_tools:
                print(f"🔧 Sending {len(gemini_tools)} tools to Gemini:")
                for tool in gemini_tools:
                    print(f"  - {tool['name']}: {tool.get('parameters', {}).get('type', 'unknown')}")
            
            # Generate response
            if gemini_tools:
                response = model.generate_content(
                    gemini_messages,
                    generation_config=generation_config,
                    tools=gemini_tools,
                    stream=True
                )
            else:
                response = model.generate_content(
                    gemini_messages,
                    generation_config=generation_config,
                    stream=True
                )
            
            # Stream response chunks
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            import traceback
            print(f"❌ Error generating response: {e}")
            print(f"📋 Full error details:")
            traceback.print_exc()
            
            # Debug: Print the tool schemas that caused the error
            if gemini_tools:
                print(f"🔍 Tool schemas that caused error:")
                import json
                print(json.dumps(gemini_tools, indent=2))
            
            yield f"Error: {str(e)}"


# Global LLM instance
gemini_llm = GeminiLLM()
