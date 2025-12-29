export type ModelId = 
  | 'gemini-2.0-flash-exp'
  | 'gemini-2.0-flash-lite'
  | 'ollama:llama3.2:3b'
  | 'ollama:llama3.2:1b'
  | 'ollama:qwen2.5:3b';

export const DEFAULT_MODEL: ModelId = 'ollama:llama3.2:3b';

export const AVAILABLE_MODELS: { id: ModelId; name: string; description: string; provider: string }[] = [
  { id: 'gemini-2.0-flash-exp', name: 'Gemini 2.0 Flash', description: 'Experimental', provider: 'Google' },
  { id: 'gemini-2.0-flash-lite', name: 'Gemini 2.0 Flash Lite', description: 'Lite', provider: 'Google' },
  { id: 'ollama:llama3.2:3b', name: 'Llama 3.2 3B', description: 'Local, Fast', provider: 'Ollama' },
  { id: 'ollama:llama3.2:1b', name: 'Llama 3.2 1B', description: 'Local, Very Fast', provider: 'Ollama' },
  { id: 'ollama:qwen2.5:3b', name: 'Qwen 2.5 3B', description: 'Local, Alternative', provider: 'Ollama' },
];

export function isValidModel(model: string): model is ModelId {
  return AVAILABLE_MODELS.some(m => m.id === model);
}
