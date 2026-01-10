import { useState, useCallback } from 'react';
import { useModelSelection } from './useModelSelection';
import { useChatMessages } from './useChatMessages';

export type { Message } from './useChatMessages';

export function useChat() {
  const [input, setInput] = useState('');
  const { selectedModel, setSelectedModel } = useModelSelection();
  const { messages, isLoading, sendMessage, retryLastMessage } = useChatMessages(selectedModel);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!input.trim()) return;
      
      const messageToSend = input;
      setInput(''); // Clear input immediately
      await sendMessage(messageToSend);
    },
    [input, sendMessage]
  );

  return {
    messages,
    input,
    setInput,
    isLoading,
    handleSubmit,
    selectedModel,
    setSelectedModel,
    retryLastMessage,
  };
}
