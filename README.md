# AI Chatbot Monorepo

A modern AI chatbot built with Next.js and Google Gemini, featuring tool calling and Model Context Protocol (MCP) integration. Organized as a monorepo using Turborepo and pnpm workspaces.

## 🏗️ Monorepo Structure

```
ai-chatbot/
├── apps/
│   ├── web/                      # Next.js frontend
│   └── backend-chat-service/     # Python FastAPI backend
├── packages/
│   └── shared-types/             # Shared TypeScript types
├── docker/
│   ├── docker-compose.yml        # Docker orchestration
│   └── ollama-entrypoint.sh      # Ollama setup script
└── test-data/                    # Shared test data
```

## ✨ Features

- 🤖 Powered by Google Gemini 2.0 Flash & Ollama
- 🛠️ Tool calling support (calculator, weather, time)
- 💬 Streaming chat responses
- 🎨 Modern UI with Tailwind CSS
- 🔌 MCP (Model Context Protocol) integration
- 📦 Monorepo with Turborepo for efficient builds
- 🐳 Docker support with PostgreSQL & Ollama

## 🚀 Quick Start

### Prerequisites

- **Node.js** >= 16.0.0
- **npm** >= 7.0.0 (comes with Node.js)
- **Python** 3.11+ (for backend development)
- **Docker** (optional, for containerized setup)

### Development Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   
   For the web app (`apps/web/.env.local`):
   ```bash
   GOOGLE_GENERATIVE_AI_API_KEY=your-key-here
   ```
   Get your API key from https://aistudio.google.com/app/apikey

   For the backend (`apps/backend-chat-service/.env`):
   ```bash
   GOOGLE_API_KEY=your-key-here
   DATABASE_URL=postgresql://chatbot:chatbot_password@localhost:5432/chatbot_db
   ```

3. **Run all services**:
   ```bash
   # Start everything (Docker + Backend + Frontend)
   pnpm dev:all
   
   # Or just the frontend
   pnpm dev
   ```

   **`pnpm dev:all` starts**:
   - PostgreSQL (Docker)
   - Ollama (Docker)
   - Python backend (port 8000)
   - Next.js frontend (port 3000)

### Docker Setup

1. **Start all services with Docker**:
   ```bash
   cd docker
   docker-compose up -d
   ```

   This starts:
   - PostgreSQL database
   - Ollama (local LLM server)
   - Python backend
   - Frontend (with `--profile full-stack`)

2. **View logs**:
   ```bash
   docker-compose logs -f
   ```

See [DOCKER.md](./DOCKER.md) for detailed Docker instructions.

## 📦 Workspace Packages

### Apps

- **[@ai-chatbot/web](./apps/web)** - Next.js 16 frontend with React 19
- **[@ai-chatbot/backend-chat-service](./apps/backend-chat-service)** - Python FastAPI backend with MCP

### Packages

- **[@ai-chatbot/shared-types](./packages/shared-types)** - Shared TypeScript types

## 🛠️ Development

### Available Scripts

```bash
# Run all dev servers
npm run dev

# Build all apps
npm run build

# Lint all packages
npm run lint

# Run tests
npm run test

# Clean all build artifacts
npm run clean
```

### Adding a New Service

1. Create a new directory in `apps/`:
   ```bash
   mkdir apps/backend-auth-service
   ```

2. Add a `package.json` with a workspace name:
   ```json
   {
     "name": "@ai-chatbot/backend-auth-service",
     "version": "0.1.0"
   }
   ```

3. The workspace will be automatically detected by npm.

### Using Shared Types

In any TypeScript app:

```typescript
import { ChatMessage, ModelInfo } from '@ai-chatbot/shared-types';
```

## 🏛️ Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: Python 3.11, FastAPI, Poetry
- **AI SDK**: Vercel AI SDK, @ai-sdk/google
- **LLM**: Google Gemini 2.0 Flash, Ollama
- **Database**: PostgreSQL 16
- **Monorepo**: Turborepo, npm workspaces
- **DevOps**: Docker, Docker Compose

## 📚 Documentation

- [Quick Start Guide](./QUICKSTART.md)
- [Setup Instructions](./SETUP.md)
- [Docker Guide](./DOCKER.md)

## 🤝 Contributing

This is a monorepo project. When contributing:

1. Make changes in the appropriate workspace (`apps/*` or `packages/*`)
2. Run `npm run lint` before committing
3. Ensure all builds pass with `npm run build`
4. Update shared types in `packages/shared-types` when adding new APIs

## 📝 License

MIT
