#!/bin/bash
set -e

# Start Ollama in the background
/bin/ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 5

# Pull only the smallest, fastest model
echo "Pulling Ollama model (this may take a few minutes)..."
ollama pull llama3.2:1b

echo "Model ready!"

# Keep the container running
wait
