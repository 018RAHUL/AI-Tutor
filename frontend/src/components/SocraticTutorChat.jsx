import { apiFetch } from '../api';
import React, { useState, useRef, useEffect } from 'react';
import {
  X,
  Send,
  Sparkles,
  Lightbulb,
  HelpCircle,
  Zap,
  Waves,
  Sigma,
  Bot,
  User,
  CheckCircle2,
  RefreshCw
} from 'lucide-react';

export default function SocraticTutorChat({
  isOpen,
  onClose,
  lessonId,
  currentScene,
  topic = "Core Concept",
  learningStyle = "Visual"
}) {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const cleanTopic = topic || "Lesson Topic";
  const sceneTitle = currentScene?.chapter_title || currentScene?.concept || cleanTopic;
  const currentFormula = currentScene?.visual_payload?.formula || currentScene?.formula || `Principles of ${cleanTopic}`;

  // Reset or initialize welcome message when topic or scene opens
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          role: 'assistant',
          content: `👋 Hello! I am your **AI Socratic Tutor**. I'm here to guide your thinking, provide tiered hints, and explore deep conceptual intuition for **${cleanTopic}**.\n\nCurrent Focus: *${sceneTitle}*\n\nWhat would you like to explore or clarify?`,
          avatarState: 'SPEAKING',
          formulaRef: currentFormula
        }
      ]);
    }
  }, [isOpen, cleanTopic, sceneTitle]);

  useEffect(() => {
    if (isOpen) {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  if (!isOpen) return null;

  // Dynamically generate quick prompt chips based on current topic
  const quickPrompts = [
    { label: '💡 Give me a hint', query: `Can you give me a subtle Socratic hint for understanding ${cleanTopic} without spoiling test answers?` },
    { label: '🌊 Real-World Analogy', query: `Can you explain ${cleanTopic} using an intuitive real-world mechanical or physical analogy?` },
    { label: '📐 Formula Breakdown', query: `How do I interpret and apply the governing formula or rule of ${cleanTopic}?` },
    { label: '⚡ Cause & Effect', query: `If the primary input variable in ${cleanTopic} changes, how does the system respond?` }
  ];

  const handleSend = async (queryToSend = null) => {
    const text = (queryToSend || inputQuery).trim();
    if (!text || isLoading) return;

    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const res = await apiFetch(`/api/lesson/${lessonId || 'general'}/tutor-ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_query: text,
          scene_title: sceneTitle,
          scene_narration: currentScene?.narration || '',
          learning_style: learningStyle,
          chat_history: messages.slice(-4)
        })
      });

      const data = await res.json();
      const botMsg = {
        role: 'assistant',
        content: data.response || `Let's analyze ${cleanTopic} step by step from first principles.`,
        avatarState: data.avatar_reaction || 'EXPLAINING',
        formulaRef: data.formula_ref || currentFormula,
        actionableSuggestion: data.actionable_suggestion
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error('Tutor chat failed:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `💡 *Core Intuition on ${cleanTopic}:* Always trace how changing the system inputs influences the resulting output according to the governing principles.`,
          avatarState: 'EXPLAINING'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-slate-900/95 backdrop-blur-xl border-l border-white/10 shadow-2xl flex flex-col animate-slideLeft">
      {/* Header */}
      <div className="p-4 border-b border-white/10 flex items-center justify-between bg-slate-950/40">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-brand-500 to-sky-400 flex items-center justify-center text-white shadow-lg shadow-brand-500/25">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-slate-900" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-sm text-white">Socratic AI Tutor</h3>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/30">
                Live
              </span>
            </div>
            <p className="text-[11px] text-slate-400 truncate max-w-[220px]">
              {cleanTopic} • {sceneTitle}
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages Scroll View */}
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="w-7 h-7 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 shrink-0 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-[85%] rounded-2xl p-3.5 text-xs leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-gradient-to-r from-brand-500 to-sky-600 text-white rounded-br-none shadow-md shadow-brand-500/20'
                  : 'bg-slate-950/80 border border-white/10 text-slate-200 rounded-bl-none shadow-lg'
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content}</div>

              {msg.formulaRef && msg.role === 'assistant' && (
                <div className="mt-2.5 pt-2 border-t border-white/5 flex items-center justify-between text-[11px] text-brand-300 font-mono">
                  <span>📐 Formula: {msg.formulaRef}</span>
                </div>
              )}

              {msg.actionableSuggestion && msg.role === 'assistant' && (
                <div className="mt-2 p-2 rounded-lg bg-brand-500/10 border border-brand-500/20 text-brand-200 text-[11px]">
                  💡 <strong>Suggestion:</strong> {msg.actionableSuggestion}
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-7 h-7 rounded-xl bg-brand-500/20 border border-brand-500/40 flex items-center justify-center text-brand-300 shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center gap-2 p-3 rounded-2xl bg-slate-950/60 border border-white/5 text-xs text-slate-400 w-fit">
            <div className="w-3.5 h-3.5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
            <span>AI Tutor is reasoning pedagogically for {cleanTopic}...</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="p-3 border-t border-white/5 bg-slate-950/40 space-y-2">
        <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider px-1">
          Quick Inquiries on {cleanTopic}
        </div>
        <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-thin">
          {quickPrompts.map((qp, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(qp.query)}
              disabled={isLoading}
              className="px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-white/10 text-slate-300 text-[11px] font-medium border border-white/10 whitespace-nowrap shrink-0 transition-colors"
            >
              {qp.label}
            </button>
          ))}
        </div>
      </div>

      {/* Input Stage */}
      <div className="p-4 border-t border-white/10 bg-slate-950/80">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={`Ask AI Tutor about ${cleanTopic}...`}
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
          />

          <button
            type="submit"
            disabled={!inputQuery.trim() || isLoading}
            className="p-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 disabled:opacity-50 text-white shadow-lg shadow-brand-500/25 transition-all"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
