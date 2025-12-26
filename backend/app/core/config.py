from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Keys
    google_api_key: str
    
    # MCP Server Configuration
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


# Global settings instance
settings = Settings()
