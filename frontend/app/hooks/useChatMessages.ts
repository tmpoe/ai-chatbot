import { useState, useCallback } from 'react';
import type { ModelId } from '@/lib/models';

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

export function useChatMessages(selectedModel: ModelId) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content,
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: [...messages, userMessage].map((m) => ({
              role: m.role,
              content: m.content,
            })),
            model: selectedModel,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to get response');
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let assistantMessage = '';
        const assistantId = (Date.now() + 1).toString();

        if (reader) {
          setMessages((prev) => [
            ...prev,
            { id: assistantId, role: 'assistant', content: '' },
          ]);

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
              if (line.startsWith('0:')) {
                const text = line.slice(2).replace(/^"(.*)"$/, '$1');
                assistantMessage += text;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId ? { ...m, content: assistantMessage } : m
                  )
                );
              }
            }
          }
        }
      } catch (error) {
        console.error('Error:', error);
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: 'Sorry, there was an error processing your request.',
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, messages, selectedModel]
  );

  return {
    messages,
    isLoading,
    sendMessage,
  };
}
