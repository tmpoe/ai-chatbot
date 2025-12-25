import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { streamText } from 'ai';
import { tools } from '@/lib/tools';
import { DEFAULT_MODEL } from '@/lib/models';

const google = createGoogleGenerativeAI({
  apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY || '',
});

export async function POST(req: Request) {
  const { messages, model = DEFAULT_MODEL } = await req.json();

  const result = streamText({
    model: google(model),
    messages,
    tools,
  });

  return result.toTextStreamResponse();
}
