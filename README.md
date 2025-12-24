# AI Chatbot with Gemini & MCP

A modern AI chatbot built with Next.js and Google Gemini, featuring tool calling and Model Context Protocol (MCP) integration.

## Project Structure

```
ai-chatbot/
├── frontend/          # Next.js frontend application
│   ├── app/          # Next.js app directory
│   ├── lib/          # Utilities and tools
│   └── ...
├── backend/          # MCP servers and backend services (coming soon)
└── README.md
```

## Features

- 🤖 Powered by Google Gemini 2.0 Flash Lite
- 🛠️ Tool calling support (calculator, weather, time)
- 💬 Streaming chat responses
- 🎨 Modern UI with Tailwind CSS
- 🔌 MCP (Model Context Protocol) ready

## Getting Started

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your Gemini API key:
   ```
   GOOGLE_GENERATIVE_AI_API_KEY=your-key-here
   ```
   Get your API key from https://aistudio.google.com/app/apikey

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Backend (Coming Soon)

MCP server integration will be added here.

## Tech Stack

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **AI SDK**: Vercel AI SDK, @ai-sdk/google
- **LLM**: Google Gemini 2.0 Flash Lite
- **Future**: MCP servers for extended functionality
