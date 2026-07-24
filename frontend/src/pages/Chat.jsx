import React, { useEffect, useRef, useState } from "react";
import Layout from "../components/Layout";
import { chatApi } from "../services/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    chatApi.history().then((res) => {
      const loaded = res.data.map((m) => ({
        role: m.role,
        content: m.content,
        citations: m.citations || [],
      }));
      setMessages(loaded);
    });
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim() || asking) return;

    const q = question;
    setQuestion("");
    setMessages((prev) => [...prev, { role: "user", content: q, citations: [] }]);
    setAsking(true);

    try {
      const res = await chatApi.ask(q);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.data.answer, citations: res.data.citations },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            err.response?.data?.detail ||
            "Something went wrong answering that question. Please try again.",
          citations: [],
        },
      ]);
    } finally {
      setAsking(false);
    }
  };

  const handleClear = async () => {
    await chatApi.clearHistory();
    setMessages([]);
  };

  return (
    <Layout>
      <div className="flex h-screen flex-col">
        <div className="flex items-center justify-between border-b border-ink/10 px-8 py-4">
          <div>
            <h1 className="text-lg font-semibold tracking-tight">Ask your documents</h1>
            <p className="text-xs text-ink/40">
              Answers are grounded only in what you've uploaded, with sources cited.
            </p>
          </div>
          {messages.length > 0 && (
            <button
              onClick={handleClear}
              className="text-xs font-medium text-ink/40 hover:text-red-600"
            >
              Clear history
            </button>
          )}
        </div>

        <div className="flex-1 overflow-y-auto px-8 py-6">
          {messages.length === 0 && (
            <div className="mx-auto mt-24 max-w-md text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-ink/5 text-2xl">
                💬
              </div>
              <h2 className="text-base font-medium">Ask anything about your documents</h2>
              <p className="mt-1 text-sm text-ink/40">
                Try: "How many vacation days do interns get?"
              </p>
            </div>
          )}

          <div className="mx-auto max-w-2xl space-y-6">
            {messages.map((m, i) => (
              <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
                <div
                  className={`inline-block max-w-[85%] rounded-2xl px-4 py-3 text-left text-sm ${
                    m.role === "user"
                      ? "bg-ink text-paper"
                      : "card"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{m.content}</p>

                  {m.citations?.length > 0 && (
                    <div className="mt-3 space-y-1.5 border-t border-ink/10 pt-3">
                      <p className="text-xs font-medium text-ink/50">Sources</p>
                      {m.citations.map((c, ci) => (
                        <div
                          key={ci}
                          className="rounded-lg bg-ink/5 px-2.5 py-1.5 text-xs text-ink/60"
                          title={c.snippet}
                        >
                          📄 {c.filename} · chunk {c.chunk_index}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {asking && (
              <div className="text-left">
                <div className="card inline-block px-4 py-3 text-sm text-ink/40">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
        </div>

        <form
          onSubmit={handleAsk}
          className="border-t border-ink/10 px-8 py-4"
        >
          <div className="mx-auto flex max-w-2xl items-center gap-3">
            <input
              type="text"
              className="input-field"
              placeholder="Ask a question about your documents..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            <button type="submit" disabled={asking} className="btn-primary shrink-0">
              Send
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
