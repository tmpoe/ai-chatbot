from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import chat
from app.services.mcp_service import mcp_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("🚀 Starting AI Chatbot Backend...")
    try:
        await mcp_service.initialize()
        print("✅ Backend ready!")
    except Exception as e:
        print(f"⚠️  Warning: MCP service initialization failed: {e}")
        print("   Continuing without MCP support...")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    await mcp_service.close()


# Create FastAPI app
app = FastAPI(
    title="AI Chatbot Backend",
    description="Python backend with MCP support for AI chatbot",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Chatbot Backend API",
        "version": "0.1.0",
        "docs": "/docs"
    }
