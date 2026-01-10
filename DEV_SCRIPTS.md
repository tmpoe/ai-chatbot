# Development Scripts

This directory contains scripts to help with local development.

## dev.sh

**Purpose**: Start all services needed for local development in one command.

**Usage**:
```bash
# From the root directory
./dev.sh

# Or using pnpm
pnpm dev:all
```

**What it does**:
1. ✅ Checks if Docker is running
2. ✅ Starts PostgreSQL and Ollama (via Docker Compose)
3. ✅ Waits for PostgreSQL to be ready
4. ✅ Starts Python backend (FastAPI) on port 8000
5. ✅ Starts Next.js frontend (via Turborepo) on port 3000
6. ✅ Handles graceful shutdown with Ctrl+C

**Services Started**:
- PostgreSQL: `localhost:5432`
- Ollama: `localhost:11434`
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

**Logs**:
- Backend logs: `logs/backend.log`
- Frontend logs: Terminal output

**Requirements**:
- Docker Desktop running
- Poetry installed (for Python backend)
- pnpm installed (for frontend)

**Stopping**:
Press `Ctrl+C` to stop all services gracefully.

## Individual Services

If you prefer to run services separately:

**Docker services only**:
```bash
cd docker
docker-compose up postgres ollama
```

**Frontend only**:
```bash
pnpm dev
```

**Backend only**:
```bash
cd apps/backend-chat-service
poetry run uvicorn main:app --reload
```
