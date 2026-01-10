#!/bin/bash

# AI Chatbot - Development Environment Startup Script
# This script starts all services needed for local development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AI Chatbot Development Environment${NC}\n"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop first.${NC}"
    exit 1
fi

# Check if Poetry is installed (for Python backend)
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}⚠️  Poetry not found. Python backend will not start.${NC}"
    echo -e "${YELLOW}   Install with: curl -sSL https://install.python-poetry.org | python3 -${NC}\n"
    SKIP_BACKEND=true
fi

# Start Docker services (PostgreSQL + Ollama)
echo -e "${GREEN}📦 Starting Docker services (PostgreSQL + Ollama)...${NC}"
cd docker

# Stop any existing containers first
docker-compose down > /dev/null 2>&1 || true

# Start fresh
docker-compose up -d postgres ollama
cd ..

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}⏳ Waiting for PostgreSQL to be ready...${NC}"
sleep 3

# Start Python backend in background
if [ "$SKIP_BACKEND" != true ]; then
    echo -e "${GREEN}🐍 Starting Python backend...${NC}"
    cd apps/backend-chat-service
    
    # Install dependencies if needed
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}   Installing Python dependencies...${NC}"
        poetry install
    fi
    
    # Start backend in background with nohup
    nohup poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}   ✓ Backend starting (PID: $BACKEND_PID)${NC}"
    echo -e "${YELLOW}   ⏳ Waiting for backend to initialize...${NC}"
    sleep 5  # Give backend time to start
    cd ../..
fi

# Start frontend with Turborepo
echo -e "${GREEN}⚛️  Starting Next.js frontend...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Create logs directory if it doesn't exist
mkdir -p logs

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down services...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo -e "${YELLOW}   Stopping Python backend...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    echo -e "${YELLOW}   Stopping Docker services...${NC}"
    cd docker
    docker-compose down
    cd ..
    
    echo -e "${GREEN}✓ All services stopped${NC}"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup INT TERM

# Start frontend (this will block)
pnpm dev

# If we get here, cleanup
cleanup
