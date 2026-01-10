import { Message } from '../hooks/useChat';

type ChatMessageProps = {
  message: Message;
  onRetry?: () => void;
};

export function ChatMessage({ message, onRetry }: ChatMessageProps) {
  return (
    <div
      className={`flex ${
        message.role === 'user' ? 'justify-end' : 'justify-start'
      }`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 ${
          message.role === 'user'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>
        {message.isError && onRetry && (
          <button
            onClick={onRetry}
            className="mt-2 px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        )}
      </div>
    </div>
  );
}
