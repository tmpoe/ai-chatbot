# Quick Start Guide

## 1. Start Everything

```bash
# Just run this - models will auto-download!
docker-compose up --build
```

That's it! The first startup will take a few minutes to download models (llama3.2:3b and llama3.2:1b).

## 2. Use the Chatbot

- Frontend: http://localhost:3000 (if running locally)
- Backend: http://localhost:8000
- Select "Llama 3.2 3B" from the model dropdown
- Start chatting!

## What Happens Automatically

1. ✅ PostgreSQL starts with sample data
2. ✅ Ollama starts and pulls models (llama3.2:3b, llama3.2:1b)
3. ✅ Backend starts with MCP servers
4. ✅ Everything is ready to use!

## Troubleshooting

**First startup taking long?**
- Normal! Ollama is downloading models (~2GB each)
- Watch logs: `docker-compose logs -f ollama`

**"Could not connect to Ollama"?**
- Wait for models to finish downloading
- Check: `docker-compose logs ollama`

**Want to add more models?**
```bash
docker exec -it chatbot-ollama ollama pull mistral:7b
```
