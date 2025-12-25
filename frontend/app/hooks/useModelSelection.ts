import { useState, useEffect } from 'react';
import { ModelId, DEFAULT_MODEL } from '@/lib/models';

const STORAGE_KEY = 'ai-chatbot-selected-model';

export function useModelSelection() {
  const [selectedModel, setSelectedModel] = useState<ModelId>(DEFAULT_MODEL);
  const [mounted, setMounted] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setSelectedModel(stored as ModelId);
    }
    setMounted(true);
  }, []);

  // Save to localStorage when model changes
  useEffect(() => {
    if (mounted) {
      localStorage.setItem(STORAGE_KEY, selectedModel);
    }
  }, [selectedModel, mounted]);

  return {
    selectedModel,
    setSelectedModel,
  };
}
