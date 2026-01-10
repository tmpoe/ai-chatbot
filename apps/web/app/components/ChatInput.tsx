type ChatInputProps = {
  input: string;
  setInput: (value: string) => void;
  isLoading: boolean;
  onSubmit: (e: React.FormEvent) => void;
};

export function ChatInput({ input, setInput, isLoading, onSubmit }: ChatInputProps) {
  return (
    <form onSubmit={onSubmit} className="mx-auto max-w-3xl">
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 rounded-full border border-zinc-300 px-4 py-2 focus:border-blue-600 focus:outline-none dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="rounded-full bg-blue-600 px-6 py-2 font-medium text-white hover:bg-blue-700 disabled:bg-zinc-300 dark:disabled:bg-zinc-700"
        >
          Send
        </button>
      </div>
    </form>
  );
}
