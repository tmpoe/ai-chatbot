import { tool } from 'ai';
import { z } from 'zod';

export const tools = {
  calculator: tool({
    description: 'Perform basic arithmetic operations (add, subtract, multiply, divide)',
    parameters: z.object({
      operation: z.enum(['add', 'subtract', 'multiply', 'divide']).describe('The arithmetic operation to perform'),
      a: z.number().describe('First number'),
      b: z.number().describe('Second number'),
    }),
    execute: async ({ operation, a, b }) => {
      switch (operation) {
        case 'add':
          return { result: a + b };
        case 'subtract':
          return { result: a - b };
        case 'multiply':
          return { result: a * b };
        case 'divide':
          if (b === 0) {
            throw new Error('Cannot divide by zero');
          }
          return { result: a / b };
      }
    },
  }),

  getWeather: tool({
    description: 'Get the current weather for a location (simulated data for demo)',
    parameters: z.object({
      location: z.string().describe('The city name, e.g., "San Francisco" or "London"'),
    }),
    execute: async ({ location }) => {
      // In a real app, you'd call a weather API here
      // For now, we'll simulate it with random data
      const conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Windy'];
      const temp = Math.floor(Math.random() * 30) + 10; // 10-40°C
      const condition = conditions[Math.floor(Math.random() * conditions.length)];

      return {
        location,
        temperature: temp,
        condition,
        humidity: Math.floor(Math.random() * 50) + 30,
        unit: 'celsius',
      };
    },
  }),

  getCurrentTime: tool({
    description: 'Get the current date and time',
    parameters: z.object({}),
    execute: async () => {
      return {
        datetime: new Date().toISOString(),
        formatted: new Date().toLocaleString(),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      };
    },
  }),
};
