# Docker Setup with Ollama

## Quick Start

```bash
# Set your Gemini API key
export GOOGLE_API_KEY=your_key_here

# Start all services (including Ollama)
docker-compose up --build

# In another terminal, pull Ollama models
docker exec -it chatbot-ollama ollama pull llama3.2:3b
docker exec -it chatbot-ollama ollama pull llama3.2:1b
```

**Services:**
- Backend: http://localhost:8000
- Ollama: http://localhost:11434
- PostgreSQL: localhost:5432

---

## Pull Models

```bash
# Recommended models
docker exec -it chatbot-ollama ollama pull llama3.2:3b      # Fast, 3B
docker exec -it chatbot-ollama ollama pull llama3.2:1b      # Very fast, 1B
docker exec -it chatbot-ollama ollama pull qwen2.5:3b       # Alternative

# For better quality (larger)
docker exec -it chatbot-ollama ollama pull llama3.1:8b      # High quality
docker exec -it chatbot-ollama ollama pull mistral:7b       # Alternative
```

---

## Check Models

```bash
# List installed models
docker exec -it chatbot-ollama ollama list

# Test a model
docker exec -it chatbot-ollama ollama run llama3.2:3b "Hello!"
```

---

## Development

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f ollama

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Troubleshooting

**Ollama not responding?**
```bash
# Check if Ollama is running
docker-compose ps

# Restart Ollama
docker-compose restart ollama

# Check Ollama logs
docker-compose logs ollama
```

**Model not found?**
```bash
# Pull the model
docker exec -it chatbot-ollama ollama pull llama3.2:3b

# Verify it's installed
docker exec -it chatbot-ollama ollama list
```

**Backend can't connect to Ollama?**
- Ensure Ollama service is running: `docker-compose ps`
- Check network: `docker network inspect ai-chatbot_chatbot-network`
- Verify `OLLAMA_BASE_URL=http://ollama:11434` in backend environment

---

## GPU Support (Optional)

For faster inference with NVIDIA GPU:

1. Install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
2. Uncomment GPU section in `docker-compose.yml`:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```
3. Restart: `docker-compose up -d`
