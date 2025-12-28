import asyncio
import json
from typing import Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.core.config import settings


class MCPService:
    """Service for managing multiple MCP client connections and tool execution."""
    
    def __init__(self):
        self.servers: dict[str, dict] = {}  # server_name -> {session, tools, process}
        self.tools: list[dict[str, Any]] = []
        self._initialized = False
    
    async def initialize(self):
        """Initialize connections to all configured MCP servers."""
        if self._initialized:
            return
        
        try:
            servers_config = settings.get_mcp_servers_config()
            print(f"🔧 Initializing {len(servers_config)} MCP server(s)...")
            
            for server_config in servers_config:
                await self._initialize_server(server_config)
            
            self._initialized = True
            print(f"✅ MCP Service initialized with {len(self.tools)} total tools from {len(self.servers)} server(s)")
                    
        except Exception as e:
            print(f"❌ Failed to initialize MCP service: {e}")
            raise
    
    async def _initialize_server(self, config: dict):
        """Initialize a single MCP server."""
        server_name = config["name"]
        
        try:
            # Create server parameters
            server_params = StdioServerParameters(
                command=config["command"],
                args=config["args"],
                env=config.get("env")
            )
            
            # Note: This is a simplified version. In production, you'd want to
            # keep the connection alive, not use context managers
            print(f"  📡 Connecting to {server_name} MCP server...")
            
            # For now, we'll initialize and get tools, but note that
            # the session will close after this block
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the session
                    await session.initialize()
                    
                    # List available tools
                    tools_result = await session.list_tools()
                    server_tools = [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema,
                            "server": server_name  # Track which server owns this tool
                        }
                        for tool in tools_result.tools
                    ]
                    
                    # Store server info (session will be recreated on demand)
                    self.servers[server_name] = {
                        "config": config,
                        "tools": server_tools,
                        "session": None  # Will be created on-demand
                    }
                    
                    # Add to global tools list
                    self.tools.extend(server_tools)
                    
                    print(f"  ✅ {server_name}: {len(server_tools)} tools available")
                    
        except Exception as e:
            print(f"  ⚠️  Failed to initialize {server_name} server: {e}")
            # Continue with other servers
    
    async def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool via the appropriate MCP server."""
        if not self._initialized:
            await self.initialize()
        
        # Find which server owns this tool
        server_name = None
        for tool in self.tools:
            if tool["name"] == tool_name:
                server_name = tool["server"]
                break
        
        if not server_name:
            raise ValueError(f"Tool {tool_name} not found in any server")
        
        server_info = self.servers.get(server_name)
        if not server_info:
            raise ValueError(f"Server {server_name} not initialized")
        
        try:
            # Create a new session for this execution
            config = server_info["config"]
            server_params = StdioServerParameters(
                command=config["command"],
                args=config["args"],
                env=config.get("env")
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    return result.content
                    
        except Exception as e:
            print(f"❌ Error executing tool {tool_name} on {server_name}: {e}")
            raise
    
    def get_tools(self) -> list[dict[str, Any]]:
        """Get list of all available tools from all servers."""
        return self.tools
    
    async def close(self):
        """Close all MCP connections."""
        self.servers.clear()
        self.tools.clear()
        self._initialized = False
        print("✅ MCP Service closed")


# Global MCP service instance
mcp_service = MCPService()
