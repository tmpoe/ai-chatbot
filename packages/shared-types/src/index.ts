// Shared types for AI Chatbot monorepo

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversationId?: string;
  model?: string;
}

export interface ChatResponse {
  message: ChatMessage;
  conversationId: string;
}

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, unknown>;
}

export interface StreamChunk {
  type: 'text' | 'tool_call' | 'tool_result' | 'done';
  content?: string;
  toolCall?: ToolCall;
  toolResult?: unknown;
}

// Model types
export interface ModelInfo {
  id: string;
  name: string;
  provider: 'gemini' | 'ollama';
  description?: string;
}

// API Response types
export interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}

export type ApiResponse<T> = 
  | { success: true; data: T }
  | { success: false; error: ApiError };
