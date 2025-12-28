# Docker Setup

## Quick Start

```bash
# Set your Gemini API key
export GOOGLE_API_KEY=your_key_here

# Start all services
docker-compose up --build

# Or start without frontend
docker-compose up --build backend postgres
```

**Services:**
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Frontend (optional): http://localhost:3000

## Development

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U chatbot -d chatbot_db

# Run SQL queries
docker-compose exec postgres psql -U chatbot -d chatbot_db -c "SELECT * FROM users;"
```

## Troubleshooting

**Backend won't start?**
- Check `GOOGLE_API_KEY` is set
- Verify PostgreSQL is healthy: `docker-compose ps`

**Database connection failed?**
- Wait for PostgreSQL to be ready (check health status)
- Verify `DATABASE_URL` in docker-compose.yml

**MCP server errors?**
- Check Node.js is available in container
- Verify MCP server packages can be installed
