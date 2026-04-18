import { useEffect, useRef, useState } from "react";
import { askAI, fetchSampleQuestions } from "../api/client";
import { Send, Cpu, User } from "lucide-react";
import type { AIResponse } from "../types";

interface Message {
  role: "user" | "assistant";
  content: string;
  meta?: AIResponse;
}

export default function AIChat() {
  const [messages, setMessages]   = useState<Message[]>([]);
  const [input, setInput]         = useState("");
  const [loading, setLoading]     = useState(false);
  const [samples, setSamples]     = useState<string[]>([]);
  const bottomRef                 = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchSampleQuestions().then(r => setSamples(r.data.questions));
    setMessages([{
      role: "assistant",
      content: "Hello. I am the InfraGraph AI assistant. I can answer questions about industrial assets, incidents, maintenance history, and risk analysis — all grounded in the knowledge graph. What would you like to know?"
    }]);
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (question: string) => {
    if (!question.trim() || loading) return;
    setMessages(m => [...m, { role: "user", content: question }]);
    setInput("");
    setLoading(true);
    try {
      const r = await askAI(question);
      setMessages(m => [...m, {
        role: "assistant",
        content: r.data.answer,
        meta: r.data
      }]);
    } catch {
      setMessages(m => [...m, {
        role: "assistant",
        content: "Error contacting the AI service. Please check the backend."
      }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column",
                  height: "calc(100vh - 64px)", gap: 0 }}>

      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ fontSize: 22, fontWeight: 700,
                     color: "#f1f5f9", margin: 0 }}>
          AI Knowledge Assistant
        </h1>
        <p style={{ color: "#64748b", marginTop: 4, fontSize: 14 }}>
          RAG-powered Q&A — answers grounded in Neo4j graph data
        </p>
      </div>

      {/* Sample questions */}
      {messages.length <= 1 && samples.length > 0 && (
        <div style={{ display: "flex", gap: 8,
                      flexWrap: "wrap", marginBottom: 16 }}>
          {samples.slice(0,4).map(q => (
            <button key={q} onClick={() => send(q)}
              style={{
                background: "#1e293b", border: "1px solid #334155",
                borderRadius: 20, padding: "6px 14px",
                color: "#94a3b8", fontSize: 12, cursor: "pointer"
              }}>
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Messages */}
      <div style={{
        flex: 1, overflowY: "auto", display: "flex",
        flexDirection: "column", gap: 16,
        background: "#1e293b", border: "1px solid #334155",
        borderRadius: 12, padding: 20
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: "flex", gap: 12,
            flexDirection: msg.role === "user" ? "row-reverse" : "row"
          }}>
            {/* Avatar */}
            <div style={{
              width: 32, height: 32, borderRadius: "50%", flexShrink: 0,
              background: msg.role === "user" ? "#38bdf822" : "#a78bfa22",
              display: "flex", alignItems: "center", justifyContent: "center",
              color: msg.role === "user" ? "#38bdf8" : "#a78bfa"
            }}>
              {msg.role === "user"
                ? <User size={16} />
                : <Cpu size={16} />}
            </div>

            {/* Bubble */}
            <div style={{ maxWidth: "72%" }}>
              <div style={{
                background: msg.role === "user" ? "#0f172a" : "#0f172a",
                border: `1px solid ${msg.role === "user"
                  ? "#38bdf833" : "#a78bfa33"}`,
                borderRadius: 12, padding: "12px 16px",
                fontSize: 14, color: "#e2e8f0", lineHeight: 1.6,
                whiteSpace: "pre-wrap"
              }}>
                {msg.content}
              </div>

              {/* Metadata for AI responses */}
              {msg.meta && (
                <div style={{
                  marginTop: 6, padding: "8px 12px",
                  background: "#0f172a", borderRadius: 8,
                  border: "1px solid #1e293b", fontSize: 11,
                  color: "#475569"
                }}>
                  <span style={{ color: "#334155" }}>
                    📊 Retrieved: {msg.meta.retrieval_stats.incidents_retrieved} incidents,
                    {" "}{msg.meta.retrieval_stats.assets_retrieved} assets
                    {" "}· {msg.meta.retrieval_stats.retrieval_method}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <div style={{
              width: 32, height: 32, borderRadius: "50%",
              background: "#a78bfa22", display: "flex",
              alignItems: "center", justifyContent: "center",
              color: "#a78bfa"
            }}>
              <Cpu size={16} />
            </div>
            <div style={{ color: "#475569", fontSize: 14 }}>
              Querying knowledge graph...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send(input)}
          placeholder="Ask about assets, incidents, risk, maintenance..."
          style={{
            flex: 1, background: "#1e293b", color: "#e2e8f0",
            border: "1px solid #334155", borderRadius: 10,
            padding: "12px 16px", fontSize: 14, outline: "none"
          }}
        />
        <button onClick={() => send(input)} disabled={loading}
          style={{
            background: loading ? "#1e293b" : "#38bdf8",
            color: loading ? "#475569" : "#0f172a",
            border: "none", borderRadius: 10,
            padding: "12px 18px", cursor: loading ? "not-allowed" : "pointer",
            display: "flex", alignItems: "center", gap: 8,
            fontWeight: 600, fontSize: 14
          }}>
          <Send size={16} />
          Send
        </button>
      </div>
    </div>
  );
}