import { useState, useCallback, useRef } from 'react';
import type { ModelId } from '@/lib/models';

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isError?: boolean;
};

export function useChatMessages(selectedModel: ModelId) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const lastUserMessageRef = useRef<string>('');

  const sendMessage = useCallback(
    async (content: string, isRetry = false) => {
      if (!content.trim() || isLoading) return;

      // Store the user message for potential retry
      lastUserMessageRef.current = content;

      let userMessage: Message | null = null;

      // If this is a retry, remove the last error message but don't add a new user message
      if (isRetry) {
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg?.isError) {
            return prev.slice(0, -1);
          }
          return prev;
        });
      } else {
        // Only add user message if it's not a retry
        userMessage = {
          id: Date.now().toString(),
          role: 'user',
          content,
        };
        setMessages((prev) => [...prev, userMessage!]);
      }

      setIsLoading(true);

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: isRetry
              ? messages.map((m) => ({
                  role: m.role,
                  content: m.content,
                }))
              : [...messages, userMessage!].map((m) => ({
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
        let hasReceivedContent = false;

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
                
                // Hide loading indicator as soon as we get first content
                if (!hasReceivedContent && assistantMessage.length > 0) {
                  hasReceivedContent = true;
                  setIsLoading(false);
                }
                
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantId ? { ...m, content: assistantMessage } : m
                  )
                );
              }
            }
          }
          
          // Check if the response is an error message
          if (assistantMessage.includes('Something went wrong')) {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId ? { ...m, isError: true } : m
              )
            );
          }
        }
      } catch (error) {
        console.error('Error:', error);
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            role: 'assistant',
            content: 'Something went wrong. Please try again.',
            isError: true,
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, messages, selectedModel]
  );

  const retryLastMessage = useCallback(() => {
    if (lastUserMessageRef.current) {
      sendMessage(lastUserMessageRef.current, true);
    }
  }, [sendMessage]);

  return {
    messages,
    isLoading,
    sendMessage,
    retryLastMessage,
  };
}
