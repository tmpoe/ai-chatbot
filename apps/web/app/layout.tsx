import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Chatbot with Gemini",
  description: "A chatbot powered by Google Gemini with tool calling",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
