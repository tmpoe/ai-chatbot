import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { streamText } from 'ai';
import { tools } from '@/lib/tools';

const google = createGoogleGenerativeAI({
  apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY || '',
});

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: google('gemini-2.0-flash-lite'),
    messages,
    tools,
  });

  return result.toTextStreamResponse();
}
