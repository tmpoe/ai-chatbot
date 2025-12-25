export type ModelId = 
  | 'gemini-2.0-flash-exp'
  | 'gemini-2.0-flash-lite';

export const DEFAULT_MODEL: ModelId = 'gemini-2.0-flash-exp';

export const AVAILABLE_MODELS: { id: ModelId; name: string; description: string }[] = [
  { id: 'gemini-2.0-flash-exp', name: 'Gemini 2.0 Flash', description: 'Experimental' },
  { id: 'gemini-2.0-flash-lite', name: 'Gemini 2.0 Flash Lite', description: 'Lite' },
];

export function isValidModel(model: string): model is ModelId {
  return AVAILABLE_MODELS.some(m => m.id === model);
}
