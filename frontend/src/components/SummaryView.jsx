import { apiFetch } from '../api';
import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Sparkles,
  Copy,
  Check,
  Download,
  RotateCw,
  AlertTriangle,
  HelpCircle,
  Award,
  ArrowRight,
  ArrowLeft,
  Share2,
  Bookmark,
  Layers,
  Sigma,
  Zap,
  Flame,
  CheckCircle2,
  FileText,
  Save
} from 'lucide-react';

export default function SummaryView({
  lessonData,
  currentUser,
  onReturnToClassroom,
  onGoToAssessment
}) {
  const [activeTab, setActiveTab] = useState('executive'); // 'executive', 'formulas', 'flashcards', 'pitfalls', 'notes'
  const [summary, setSummary] = useState(lessonData?.summary || null);
  const [copiedFormulaIdx, setCopiedFormulaIdx] = useState(null);
  const [copiedMd, setCopiedMd] = useState(false);
  
  // Flashcards active recall state
  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [masteredCards, setMasteredCards] = useState({});

  // Student notes editor state
  const [userNote, setUserNote] = useState('');
  const [isSavingNote, setIsSavingNote] = useState(false);
  const [noteSavedToast, setNoteSavedToast] = useState(false);

  const topic = lessonData?.topic || "Ohm's Law";
  const subject = lessonData?.subject || "Physics";

  // Fetch summary if not in props
  useEffect(() => {
    if (lessonData?.summary && Object.keys(lessonData.summary).length > 0) {
      setSummary(lessonData.summary);
    } else if (lessonData?.id) {
      apiFetch(`/api/lesson/${lessonData.id}/summary`)
        .then((res) => res.json())
        .then((data) => setSummary(data))
        .catch(() => {});
    }
  }, [lessonData]);

  // Load existing user notes for topic if available
  useEffect(() => {
    if (currentUser?.id) {
      apiFetch('/api/notes')
        .then((res) => res.json())
        .then((notes) => {
          const match = notes.find((n) => n.topic === topic || n.lesson_id === lessonData?.id);
          if (match) setUserNote(match.content);
        })
        .catch(() => {});
    }
  }, [currentUser, topic, lessonData]);

  const copyFormula = (formulaText, idx) => {
    navigator.clipboard.writeText(formulaText);
    setCopiedFormulaIdx(idx);
    setTimeout(() => setCopiedFormulaIdx(null), 2000);
  };

  const copyFullMarkdown = () => {
    if (!summary) return;
    const md = [
      `# 📚 ${topic} — AI Study Summary`,
      `**Subject:** ${subject}\n`,
      `## 💡 Executive Summary\n${summary.executive_summary || ''}\n`,
      summary.core_intuition ? `> **Core Intuition:** ${summary.core_intuition}\n` : '',
      `## 🔑 Key Takeaways`,
      ...(summary.key_takeaways || []).map((t) => `- ${t}`),
      `\n## 📐 Formulas`,
      ...(summary.formulas || []).map((f) => `### ${f.name}\n- Formula: \`${f.formula_text}\`\n- Description: ${f.description}\n- Units: ${f.units}\n`),
      `## ⚠️ Pitfalls & Misconceptions`,
      ...(summary.common_pitfalls || []).map((p) => `- Misconception: ${p.misconception}\n  Correction: ${p.correction}`)
    ].join('\n');

    navigator.clipboard.writeText(md);
    setCopiedMd(true);
    setTimeout(() => setCopiedMd(false), 2000);
  };

  const handleDownloadMarkdown = async () => {
    if (!lessonData?.id) return copyFullMarkdown();
    try {
      const res = await apiFetch(`/api/lesson/${lessonData.id}/summary/notes.md`);
      if (!res.ok) throw new Error('Could not download notes');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = `${topic.replace(/[^a-z0-9]+/gi, '_').toLowerCase()}_notes.md`;
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err); copyFullMarkdown();
    }
  };

  const handleSaveNote = async () => {
    if (!userNote.trim()) return;
    setIsSavingNote(true);
    try {
      await apiFetch('/api/notes/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson_id: lessonData?.id || 'general',
          topic: topic,
          content: userNote,
          tags: [subject, 'SummaryNotes']
        })
      });
      setNoteSavedToast(true);
      setTimeout(() => setNoteSavedToast(false), 2500);
    } catch (err) {
      console.error('Failed to save note:', err);
    } finally {
      setIsSavingNote(false);
    }
  };

  const flashcards = summary?.flashcards || [];
  const currentCard = flashcards[cardIndex] || null;

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-8 animate-fadeIn">
      {/* Top Breadcrumb & Navigation Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl glass-panel border border-white/10">
        <div className="flex items-center gap-3">
          {onReturnToClassroom && (
            <button
              onClick={onReturnToClassroom}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl glass-card hover:bg-white/10 text-slate-300 text-xs font-semibold border border-white/10 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Classroom</span>
            </button>
          )}

          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/40">
              {subject}
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-300 font-medium">{topic}</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={copyFullMarkdown}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl glass-card hover:bg-white/10 text-slate-300 text-xs font-semibold border border-white/10 transition-colors"
          >
            {copiedMd ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copiedMd ? 'Copied MD' : 'Copy Summary'}</span>
          </button>

          <button
            onClick={handleDownloadMarkdown}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-400 text-xs font-semibold border border-sky-500/30 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download .md</span>
          </button>

          {onGoToAssessment && (
            <button
              onClick={onGoToAssessment}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-brand-500 to-sky-600 hover:from-brand-600 hover:to-sky-700 text-white font-semibold text-xs shadow-lg shadow-brand-500/25 transition-all"
            >
              <span>Take Quiz</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Hero Summary Header */}
      <div className="relative overflow-hidden rounded-3xl p-8 glass-panel border border-brand-500/30 bg-gradient-to-br from-slate-900 via-[#0b1736] to-[#071329] shadow-2xl">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-80 h-80 rounded-full bg-brand-500/15 blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-3 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/20 border border-brand-500/40 text-brand-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Pedagogical Summary & Study Master Hub</span>
          </div>

          <h1 className="text-3xl lg:text-4xl font-extrabold text-white tracking-tight">
            {topic} <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-brand-300">Master Notes</span>
          </h1>

          <p className="text-xs lg:text-sm text-slate-300 leading-relaxed font-normal">
            Autonomous multi-tier executive synthesis, active recall flashcards, formula derivations, and common pitfall remediation generated by the AI Teacher Agent.
          </p>
        </div>
      </div>

      {/* Main Tab Navigation */}
      <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-2xl bg-slate-950/70 border border-white/5">
        {[
          { id: 'executive', label: 'Executive Summary & Takeaways', icon: BookOpen },
          { id: 'formulas', label: 'Formula & Equation Sheet', icon: Sigma },
          { id: 'flashcards', label: `Active Recall Cards (${flashcards.length})`, icon: Layers },
          { id: 'pitfalls', label: 'Misconceptions & Pitfalls', icon: AlertTriangle },
          { id: 'notes', label: 'Personal Notes & Annotations', icon: FileText }
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* ============================================================ */}
      {/* TAB 1: EXECUTIVE SUMMARY & KEY TAKEAWAYS */}
      {/* ============================================================ */}
      {activeTab === 'executive' && (
        <div className="space-y-6">
          {summary?.core_intuition && (
            <div className="p-5 rounded-2xl bg-gradient-to-r from-brand-500/15 via-sky-500/10 to-indigo-500/15 border border-brand-500/30 shadow-lg flex items-start gap-4">
              <div className="p-2.5 rounded-xl bg-brand-500/20 border border-brand-500/40 text-brand-300 shrink-0">
                <Zap className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <div className="text-xs font-bold uppercase tracking-wider text-brand-400">Core Intuition</div>
                <div className="text-sm font-semibold text-white leading-relaxed italic">
                  "{summary.core_intuition}"
                </div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Executive Synthesis */}
            <div className="lg:col-span-2 glass-card p-6 rounded-3xl border border-white/10 space-y-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/30">
                  <BookOpen className="w-4 h-4" />
                </div>
                <h3 className="font-bold text-base text-white">Executive Synthesis</h3>
              </div>

              <p className="text-xs lg:text-sm text-slate-300 leading-relaxed font-normal">
                {summary?.executive_summary || 'Detailed summary is being generated by the autonomous agent.'}
              </p>

              <div className="pt-4 border-t border-white/5 space-y-3">
                <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Key Conceptual Takeaways</h4>
                <div className="space-y-2.5">
                  {(summary?.key_takeaways || []).map((takeaway, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/50 border border-white/5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span className="text-xs text-slate-200 leading-relaxed">{takeaway}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Worked Calculation Problem Card */}
            <div className="glass-card p-6 rounded-3xl border border-white/10 space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30">
                    <Sigma className="w-4 h-4" />
                  </div>
                  <h3 className="font-bold text-base text-white">Worked Problem Recap</h3>
                </div>

                {summary?.worked_example_recap ? (
                  <div className="space-y-3 text-xs">
                    <div className="p-3 rounded-xl bg-slate-950/60 border border-white/5 space-y-1">
                      <div className="font-semibold text-sky-300">{summary.worked_example_recap.title}</div>
                      <div className="text-slate-400">Given: <span className="text-slate-200 font-mono">{summary.worked_example_recap.given}</span></div>
                      <div className="text-slate-400">Target: <span className="text-slate-200 font-mono">{summary.worked_example_recap.target}</span></div>
                    </div>

                    <div className="space-y-1.5">
                      <div className="font-semibold text-slate-300 text-[11px] uppercase tracking-wider">Step-by-Step Solution:</div>
                      {summary.worked_example_recap.steps?.map((st, sidx) => (
                        <div key={sidx} className="p-2 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300 font-mono text-[11px]">
                          {st}
                        </div>
                      ))}
                    </div>

                    {summary.worked_example_recap.verification && (
                      <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-[11px]">
                        ✓ {summary.worked_example_recap.verification}
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-slate-400">Worked calculation examples will appear here.</p>
                )}
              </div>

              <button
                onClick={() => setActiveTab('formulas')}
                className="w-full mt-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-400 text-xs font-semibold border border-sky-500/30 flex items-center justify-center gap-2 transition-colors"
              >
                <span>View Full Formula Sheet</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/* TAB 2: FORMULA & EQUATIONS CHEAT-SHEET */}
      {/* ============================================================ */}
      {activeTab === 'formulas' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {(summary?.formulas || []).map((form, idx) => (
              <div
                key={idx}
                className="p-6 rounded-3xl glass-card border border-white/10 hover:border-brand-500/40 transition-all space-y-4 relative group shadow-xl"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1">
                    <h3 className="font-bold text-base text-white">{form.name}</h3>
                    <div className="text-xs text-slate-400">{form.description}</div>
                  </div>

                  <button
                    onClick={() => copyFormula(form.formula_text, idx)}
                    className="p-2 rounded-xl glass-panel hover:bg-white/10 text-slate-400 hover:text-white transition-colors"
                    title="Copy Formula Text"
                  >
                    {copiedFormulaIdx === idx ? (
                      <Check className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>

                {/* Mathematical Formula Display Box */}
                <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-950 via-[#071329] to-slate-950 border border-brand-500/30 flex items-center justify-center text-center shadow-inner">
                  <div className="text-xl lg:text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-brand-300 to-indigo-300 font-mono tracking-wider">
                    {form.formula_text}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1 text-xs">
                  <span className="text-slate-400 font-medium">Standard SI Units:</span>
                  <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-sky-300 font-mono text-[11px]">
                    {form.units}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ============================================================ */}
      {/* TAB 3: ACTIVE-RECALL FLASHCARDS */}
      {/* ============================================================ */}
      {activeTab === 'flashcards' && (
        <div className="space-y-6 max-w-2xl mx-auto">
          {flashcards.length > 0 && currentCard ? (
            <div className="space-y-4">
              {/* Progress & Card Index */}
              <div className="flex items-center justify-between text-xs text-slate-400 px-2">
                <span>Card {cardIndex + 1} of {flashcards.length}</span>
                <span className="flex items-center gap-1.5 text-brand-300 font-semibold">
                  <Award className="w-4 h-4" />
                  <span>Mastered: {Object.keys(masteredCards).length}/{flashcards.length}</span>
                </span>
              </div>

              {/* 3D Flip Card */}
              <div
                onClick={() => setIsFlipped(!isFlipped)}
                className="cursor-pointer relative min-h-[280px] p-8 rounded-3xl glass-panel border border-white/10 hover:border-brand-500/50 transition-all duration-300 flex flex-col justify-between shadow-2xl bg-gradient-to-br from-slate-900 to-slate-950 group select-none"
              >
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-1 rounded-full text-[11px] font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/40">
                    {currentCard.category || 'Recall Test'}
                  </span>
                  <span className="text-xs text-slate-500 flex items-center gap-1">
                    <RotateCw className="w-3.5 h-3.5" />
                    Click to flip
                  </span>
                </div>

                <div className="py-6 text-center space-y-3">
                  {!isFlipped ? (
                    <>
                      <div className="text-xs uppercase tracking-wider text-slate-400 font-bold">Question</div>
                      <div className="text-lg lg:text-xl font-bold text-white leading-relaxed">
                        {currentCard.question}
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="text-xs uppercase tracking-wider text-emerald-400 font-bold">Answer & Key Insight</div>
                      <div className="text-base lg:text-lg font-semibold text-slate-100 leading-relaxed">
                        {currentCard.answer}
                      </div>
                      {currentCard.hint && (
                        <div className="text-xs text-slate-400 italic pt-2">
                          💡 Hint: {currentCard.hint}
                        </div>
                      )}
                    </>
                  )}
                </div>

                <div className="text-center text-[11px] text-slate-500">
                  {isFlipped ? 'Card Answer Revealed' : 'Think of your answer before flipping'}
                </div>
              </div>

              {/* Navigation Controls */}
              <div className="flex items-center justify-between gap-4 pt-2">
                <button
                  onClick={() => {
                    setIsFlipped(false);
                    setCardIndex((prev) => (prev > 0 ? prev - 1 : flashcards.length - 1));
                  }}
                  className="px-4 py-2.5 rounded-xl glass-card hover:bg-white/10 text-slate-300 text-xs font-semibold border border-white/10 transition-colors"
                >
                  Previous Card
                </button>

                {isFlipped && (
                  <button
                    onClick={() => {
                      setMasteredCards((prev) => ({ ...prev, [currentCard.id]: true }));
                      setIsFlipped(false);
                      setCardIndex((prev) => (prev < flashcards.length - 1 ? prev + 1 : 0));
                    }}
                    className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-lg shadow-emerald-500/20 transition-all"
                  >
                    <Check className="w-4 h-4" />
                    <span>Got It Right!</span>
                  </button>
                )}

                <button
                  onClick={() => {
                    setIsFlipped(false);
                    setCardIndex((prev) => (prev < flashcards.length - 1 ? prev + 1 : 0));
                  }}
                  className="px-4 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white text-xs font-semibold shadow-lg shadow-brand-500/25 transition-all"
                >
                  Next Card
                </button>
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-400 text-center py-8">No flashcards available for this topic.</p>
          )}
        </div>
      )}

      {/* ============================================================ */}
      {/* TAB 4: COMMON PITFALLS & MISCONCEPTIONS RADAR */}
      {/* ============================================================ */}
      {activeTab === 'pitfalls' && (
        <div className="space-y-4">
          {(summary?.common_pitfalls || []).map((pitfall, idx) => (
            <div
              key={idx}
              className="p-6 rounded-3xl glass-card border border-rose-500/20 bg-gradient-to-r from-rose-500/5 via-slate-900 to-slate-900 space-y-3"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-rose-400 font-bold text-sm">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Frequent Misconception #{idx + 1}</span>
                </div>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30">
                  Severity: {pitfall.severity || 'High'}
                </span>
              </div>

              <div className="p-3.5 rounded-2xl bg-rose-950/30 border border-rose-500/20 text-xs text-rose-200 font-medium">
                ❌ <strong>Error:</strong> "{pitfall.misconception}"
              </div>

              <div className="p-3.5 rounded-2xl bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-200 font-medium flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <strong>Pedagogical Correction:</strong> {pitfall.correction}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ============================================================ */}
      {/* TAB 5: AI MASTER STUDY NOTES & PERSONAL NOTEBOOK */}
      {/* ============================================================ */}
      {activeTab === 'notes' && (
        <div className="space-y-6">
          {/* AI Master Revision Sheet Card */}
          <div className="p-6 rounded-3xl glass-panel border border-brand-500/30 bg-slate-900/80 shadow-2xl space-y-5">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-brand-500/20 text-brand-400">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-base text-white">AI-Generated Master Revision Notes</h3>
                  <p className="text-xs text-slate-400">Structured revision guide synthesized by the Autonomous Pedagogical Agent.</p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    const generatedNotes = [
                      `# ${topic} — Comprehensive Study Notes`,
                      `Subject: ${subject}\n`,
                      `## 1. Executive Intuition`,
                      summary?.executive_summary || '',
                      `\n> **Core Principle:** ${summary?.core_intuition || ''}\n`,
                      `## 2. Key Laws & Formulations`,
                      ...(summary?.formulas || []).map(f => `- **${f.name}:** \`${f.formula_text}\` (${f.description})`),
                      `\n## 3. Step-by-Step Problem Solving`,
                      `- **Problem:** ${summary?.worked_example_recap?.title || topic}`,
                      `- **Given:** ${summary?.worked_example_recap?.given || 'Parameters'}`,
                      `- **Steps:**`,
                      ...(summary?.worked_example_recap?.steps || []).map(s => `  - ${s}`),
                      `\n## 4. Common Misconceptions to Avoid`,
                      ...(summary?.common_pitfalls || []).map(p => `- ⚠️ ${p.misconception} -> ${p.correction}`)
                    ].join('\n');

                    setUserNote(prev => prev ? `${prev}\n\n---\n\n${generatedNotes}` : generatedNotes);
                  }}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-brand-500/20 hover:bg-brand-500/30 text-brand-300 text-xs font-semibold border border-brand-500/40 transition"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Import AI Notes to Notebook</span>
                </button>
              </div>
            </div>

            {/* Structured Study Notes Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Concept Overview Box */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-sky-400 flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4" />
                  <span>Conceptual Foundations</span>
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {summary?.executive_summary || `Comprehensive study of ${topic} and its core mechanisms.`}
                </p>
                {summary?.core_intuition && (
                  <div className="pt-2 text-xs italic text-brand-300 border-t border-slate-800">
                    💡 <strong>Intuition:</strong> {summary.core_intuition}
                  </div>
                )}
              </div>

              {/* Problem Solving Recap Box */}
              <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                  <Award className="w-4 h-4" />
                  <span>Worked Example Walkthrough</span>
                </h4>
                {summary?.worked_example_recap ? (
                  <div className="space-y-1 text-xs text-slate-300">
                    <div className="font-semibold text-white">{summary.worked_example_recap.title}</div>
                    <div className="text-slate-400">Given: {summary.worked_example_recap.given}</div>
                    <ul className="list-disc list-inside space-y-0.5 pt-1 text-slate-300">
                      {(summary.worked_example_recap.steps || []).map((st, sIdx) => (
                        <li key={sIdx}>{st}</li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  <p className="text-xs text-slate-400">Step-by-step problem verification recorded.</p>
                )}
              </div>
            </div>
          </div>

          {/* Student Editable Notebook Card */}
          <div className="p-6 rounded-3xl glass-card border border-white/10 space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <h3 className="font-bold text-base text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-emerald-400" />
                  <span>Your Personal Study Notebook & Annotations</span>
                </h3>
                <p className="text-xs text-slate-400">Write custom notes, derivations, or summaries. Stored automatically in your account.</p>
              </div>

              {noteSavedToast && (
                <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1 bg-emerald-500/20 px-3 py-1 rounded-full border border-emerald-500/30 animate-fade-in">
                  <Check className="w-3.5 h-3.5" /> Notes Saved!
                </span>
              )}
            </div>

            <textarea
              rows={9}
              value={userNote}
              onChange={(e) => setUserNote(e.target.value)}
              placeholder="Write your personal reflections, key equations, or click 'Import AI Notes to Notebook' to start with the full AI generated summary..."
              className="w-full p-4 rounded-2xl bg-slate-950/90 border border-slate-700 text-white placeholder-slate-500 text-xs sm:text-sm leading-relaxed focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 font-mono"
            />

            <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
              <span className="text-[11px] text-slate-500 font-mono">
                {userNote ? `${userNote.length} characters • ${userNote.split(/\s+/).filter(Boolean).length} words` : 'Notebook is empty'}
              </span>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(userNote);
                    alert("Notes copied to clipboard!");
                  }}
                  disabled={!userNote.trim()}
                  className="px-4 py-2.5 rounded-xl glass-card hover:bg-white/10 text-slate-300 text-xs font-semibold border border-white/10 transition disabled:opacity-40"
                >
                  <Copy className="w-3.5 h-3.5 inline mr-1.5" />
                  <span>Copy Notes</span>
                </button>

                <button
                  onClick={handleSaveNote}
                  disabled={isSavingNote || !userNote.trim()}
                  className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-semibold text-xs shadow-lg shadow-emerald-500/25 transition-all disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  <span>{isSavingNote ? 'Saving to Profile...' : 'Save Notes to Profile'}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
