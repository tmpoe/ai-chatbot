from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Keys
    google_api_key: str
    
    # Database
    database_url: Optional[str] = None
    
    # MCP Server Configuration (legacy single server)
    mcp_server_command: str = "npx"
    mcp_server_args: str = "-y,@modelcontextprotocol/server-filesystem,/Users/admin/work/ai-chatbot/test-data"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # CORS
    allowed_origins: str = "http://localhost:3000"
    
    @property
    def mcp_server_args_list(self) -> list[str]:
        """Convert comma-separated MCP args to list."""
        return self.mcp_server_args.split(",")
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Convert comma-separated origins to list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    def get_mcp_servers_config(self) -> list[dict]:
        """Get list of MCP servers to initialize."""
        servers = [
            {
                "name": "filesystem",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/admin/work/ai-chatbot/test-data"],
                "env": None
            }
        ]
        
        # Add PostgreSQL server if database URL is configured
        if self.database_url:
            servers.append({
                "name": "postgres",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres"],
                "env": {"DATABASE_URL": self.database_url}
            })
        
        return servers


# Global settings instance
settings = Settings()
