export function LoadingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="rounded-2xl bg-white px-4 py-2 dark:bg-zinc-800">
        <div className="flex items-center space-x-2">
          <div className="h-2 w-2 animate-bounce rounded-full bg-zinc-400 [animation-delay:-0.3s]"></div>
          <div className="h-2 w-2 animate-bounce rounded-full bg-zinc-400 [animation-delay:-0.15s]"></div>
          <div className="h-2 w-2 animate-bounce rounded-full bg-zinc-400"></div>
        </div>
      </div>
    </div>
  );
}
