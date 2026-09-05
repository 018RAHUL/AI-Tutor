import React, { useState, useEffect } from 'react';
import { Sparkles, Cpu, Bot, Film, Mic, BookOpen, CheckCircle2, Layers, ShieldCheck } from 'lucide-react';

export default function LoadingScreen({ topic = "Ohm's Law", studentLevel = "Beginner" }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(5);

  const pipelineStages = [
    { label: "Analyzing Educational Topic & Subject Domain", icon: BookOpen, desc: "Extracting core physical principles and prerequisite concepts." },
    { label: "Calibrating Student Persona & Visual Pacing", icon: ShieldCheck, desc: `Tailoring difficulty for ${studentLevel} level with visual scaffolding.` },
    { label: "Architecting Pedagogical Lesson Plan (2+ Minutes)", icon: Layers, desc: "Structuring 6 pedagogical chapters: Intro, Analogy, Law, Example, Checkpoint, Wrap-up." },
    { label: "Executing LangGraph Multi-Agent Parallel Preparation", icon: Cpu, desc: "Running Explanation, Visual, Examples, Questions, and Assessment agents concurrently." },
    { label: "Synthesizing Neural Spoken Voice & Syllable Timings", icon: Mic, desc: "Generating high-fidelity speech audio via Neural Edge-TTS engine." },
    { label: "Rendering 30 FPS Motion Graphics & MP4 Video Clips", icon: Film, desc: "Composing moving electron particles, water pipe fluid simulations, and formulas." },
    { label: "Synchronizing AI Teacher Avatar & Interactive Checkpoints", icon: Bot, desc: "Configuring lip-sync visemes, laser gestures, and misconception detection router." }
  ];

  // Dynamic progress progression
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 96) return prev;
        const increment = Math.random() * 6 + 4;
        const next = Math.min(96, prev + increment);
        const stageIdx = Math.min(pipelineStages.length - 1, Math.floor((next / 100) * pipelineStages.length));
        setCurrentStep(stageIdx);
        return next;
      });
    }, 900);

    return () => clearInterval(interval);
  }, [pipelineStages.length]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 py-12">
      <div className="glass-panel p-8 sm:p-12 rounded-3xl border border-brand-500/30 max-w-2xl w-full shadow-2xl space-y-8 relative overflow-hidden backdrop-blur-2xl">
        {/* Glowing Background Radial Glow */}
        <div className="absolute -top-24 -right-24 w-72 h-72 rounded-full bg-brand-500/20 blur-3xl pointer-events-none animate-pulse-slow" />
        <div className="absolute -bottom-24 -left-24 w-72 h-72 rounded-full bg-purple-500/20 blur-3xl pointer-events-none animate-pulse-slow" />

        {/* Header with Glowing Animated Spinner */}
        <div className="text-center space-y-3 relative z-10">
          <div className="relative w-20 h-20 mx-auto flex items-center justify-center">
            {/* Spinning Outer Ring */}
            <div className="absolute inset-0 rounded-full border-4 border-brand-500/20 border-t-brand-400 animate-spin" />
            <div className="absolute inset-2 rounded-full border-4 border-purple-500/20 border-b-purple-400 animate-spin-slow" />
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center text-white shadow-lg shadow-brand-500/40">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </div>
          </div>

          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Generating AI Educational Lesson
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            Topic: <span className="text-sky-400 font-semibold font-mono">{topic}</span> • Target: <span className="text-emerald-400 font-semibold">{studentLevel}</span>
          </p>
        </div>

        {/* Dynamic Progress Bar */}
        <div className="space-y-2 relative z-10">
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400 font-medium">Pipeline Orchestration</span>
            <span className="font-mono text-sky-400 font-bold">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-slate-900 rounded-full h-3 p-0.5 border border-slate-800 overflow-hidden">
            <div
              className="bg-gradient-to-r from-brand-500 via-sky-400 to-indigo-500 h-full rounded-full transition-all duration-500 shadow-md shadow-brand-500/30"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Animated Multi-Agent Stage Checklist */}
        <div className="space-y-3 relative z-10 pt-2">
          {pipelineStages.map((stage, idx) => {
            const isDone = idx < currentStep;
            const isCurrent = idx === currentStep;
            const Icon = stage.icon;

            return (
              <div
                key={idx}
                className={`flex items-start gap-3.5 p-3 rounded-2xl transition-all duration-300 border ${
                  isCurrent
                    ? 'bg-slate-900/95 border-brand-500/60 shadow-lg shadow-brand-500/10 scale-[1.02]'
                    : isDone
                    ? 'bg-slate-950/60 border-slate-800/80 opacity-80'
                    : 'bg-slate-950/30 border-slate-900 opacity-40'
                }`}
              >
                <div
                  className={`p-2 rounded-xl border mt-0.5 shrink-0 transition-colors ${
                    isDone
                      ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400'
                      : isCurrent
                      ? 'bg-brand-500/20 border-brand-400 text-brand-300 animate-pulse'
                      : 'bg-slate-800 border-slate-700 text-slate-500'
                  }`}
                >
                  {isDone ? <CheckCircle2 className="w-4 h-4" /> : <Icon className="w-4 h-4" />}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4
                      className={`text-xs font-bold truncate ${
                        isCurrent ? 'text-sky-300' : isDone ? 'text-slate-200' : 'text-slate-500'
                      }`}
                    >
                      {stage.label}
                    </h4>
                    {isCurrent && (
                      <span className="text-[10px] font-semibold text-brand-400 font-mono animate-pulse">
                        RUNNING
                      </span>
                    )}
                    {isDone && (
                      <span className="text-[10px] font-semibold text-emerald-400 font-mono">
                        DONE
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5 line-clamp-1">{stage.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer Note */}
        <div className="text-center text-[11px] text-slate-500 pt-2 relative z-10">
          "The AI does not just talk about the concept — the AI shows the concept."
        </div>
      </div>
    </div>
  );
}
