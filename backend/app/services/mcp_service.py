import asyncio
import json
from typing import Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.core.config import settings


class MCPService:
    """Service for managing MCP client connection and tool execution."""
    
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.tools: list[dict[str, Any]] = []
        self._initialized = False
    
    async def initialize(self):
        """Initialize connection to MCP server."""
        if self._initialized:
            return
        
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command=settings.mcp_server_command,
                args=settings.mcp_server_args_list,
                env=None
            )
            
            # Connect to MCP server
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    
                    # Initialize the session
                    await session.initialize()
                    
                    # List available tools
                    tools_result = await session.list_tools()
                    self.tools = [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema
                        }
                        for tool in tools_result.tools
                    ]
                    
                    self._initialized = True
                    print(f"✅ MCP Service initialized with {len(self.tools)} tools")
                    
        except Exception as e:
            print(f"❌ Failed to initialize MCP service: {e}")
            raise
    
    async def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool via MCP."""
        if not self._initialized or not self.session:
            await self.initialize()
        
        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result.content
        except Exception as e:
            print(f"❌ Error executing tool {tool_name}: {e}")
            raise
    
    def get_tools(self) -> list[dict[str, Any]]:
        """Get list of available tools."""
        return self.tools
    
    async def close(self):
        """Close MCP connection."""
        if self.session:
            # MCP session cleanup handled by context manager
            self._initialized = False
            print("✅ MCP Service closed")


# Global MCP service instance
mcp_service = MCPService()
