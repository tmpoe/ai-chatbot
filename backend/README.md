# AI Chatbot Backend

Python backend with FastAPI, MCP support, and Google Gemini.

## Quick Start

```bash
# Install dependencies
poetry install

# Setup environment
cp env.example .env
# Add your GOOGLE_API_KEY to .env

# Run server
poetry run uvicorn main:app --reload --port 8000
```

**Docs**: http://localhost:8000/docs

---

## Architecture

**Clean architecture** with 4 layers:

- **API** (`app/api/`) - HTTP endpoints, streaming
- **Core** (`app/core/`) - Config, LLM integration
- **Services** (`app/services/`) - MCP client, chat orchestration
- **Models** (`app/models/`) - Pydantic schemas

**Flow**: Frontend → Next.js → Python Backend → MCP Server + Gemini → Stream back

---

## Configuration

`.env` file:
```bash
GOOGLE_API_KEY=your_key_here
MCP_SERVER_ARGS=-y,@modelcontextprotocol/server-filesystem,/path/to/test-data
ALLOWED_ORIGINS=http://localhost:3000
```

---

## API Endpoints

### `POST /api/chat`
Streaming chat with MCP tools.

**Request:**
```json
{
  "messages": [{"role": "user", "content": "Hello"}],
  "model": "gemini-2.0-flash-exp"
}
```

**Response:** SSE stream (`0:chunk\n`)

### `GET /api/health`
Health check.

---

## Development

```bash
# Tests
poetry run pytest

# Format
poetry run black .

# Lint
poetry run ruff check .
```

---

## Troubleshooting

**MCP fails to initialize?**
- Check `MCP_SERVER_ARGS` path in `.env`
- Test manually: `npx -y @modelcontextprotocol/server-filesystem /path`

**Missing API key?**
- Add `GOOGLE_API_KEY` to `.env`
- Get one: https://ai.google.dev/

**CORS errors?**
- Add frontend URL to `ALLOWED_ORIGINS` in `.env`

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MCP Spec](https://modelcontextprotocol.io/)
- [Gemini API](https://ai.google.dev/docs)
