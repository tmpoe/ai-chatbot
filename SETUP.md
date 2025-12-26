# Setup Instructions

## Backend Setup

1. **Copy environment file:**
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Add your Gemini API key to `.env`:**
   ```bash
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

3. **Install dependencies (already done):**
   ```bash
   poetry install
   ```

## Frontend Setup

1. **Copy environment file:**
   ```bash
   cd frontend
   cp env.local.example .env.local
   ```

2. **The frontend is already configured to proxy to Python backend**

## Running the Full Stack

You'll need 3 terminals:

### Terminal 1: MCP Filesystem Server
```bash
npx -y @modelcontextprotocol/server-filesystem /Users/admin/work/ai-chatbot/test-data
```

### Terminal 2: Python Backend
```bash
cd backend
poetry run uvicorn main:app --reload --port 8000
```

### Terminal 3: Next.js Frontend
```bash
cd frontend
npm run dev
```

## Testing

1. Open `http://localhost:3000` in your browser
2. Try these prompts:
   - "Hello!" (basic chat)
   - "What files are in my test folder?" (MCP tool calling)
   - "Read the contents of sample.txt" (file reading)
   - "What's in notes.md?" (markdown file)

## Next Steps

After testing Phase 1, we'll move to Phase 2:
- Build custom MCP servers
- Connect multiple MCP servers simultaneously
- Add more advanced features
