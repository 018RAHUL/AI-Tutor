import React from 'react';
import { X, Activity, Cpu, GitBranch, CheckCircle, Database, ShieldAlert, Sparkles } from 'lucide-react';

export default function ObservabilityDrawer({ isOpen, onClose, observabilityLogs, lesson }) {
  if (!isOpen) return null;

  const logs = observabilityLogs || lesson?.observability_logs || [
    { node: 'input_analyzer', timestamp: new Date().toISOString(), detail: "Analyzed topic: Ohm's Law (Physics). Calibrated for Beginner visual learner." },
    { node: 'student_profiler', timestamp: new Date().toISOString(), detail: "Profile calibrated: Level=Beginner, Style=Visual, Scaffolding=True" },
    { node: 'lesson_planner', timestamp: new Date().toISOString(), detail: "Generated 6-chapter pedagogical sequence (2+ minutes)." },
    { node: 'parallel_prep', timestamp: new Date().toISOString(), detail: "Parallel preparation executed concurrently across 5 agents in 12ms: Explanation, Visual, Examples, Questions, Assessment." },
    { node: 'scene_planner', timestamp: new Date().toISOString(), detail: "Fan-In complete: Synchronized 6 scenes with Edge-TTS audio." }
  ];

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/60 backdrop-blur-sm animate-fade-in flex justify-end">
      <div className="w-full max-w-lg bg-slate-900 border-l border-white/10 shadow-2xl p-6 flex flex-col justify-between overflow-y-auto">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
                <Activity className="w-5 h-5 animate-pulse" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-white">LangGraph Observability & Tracing</h3>
                <p className="text-[11px] text-slate-400">Live multi-agent execution pipeline & state inspector</p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Model Router & Execution Architecture Info */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="flex items-center justify-between text-slate-300">
              <span className="flex items-center gap-1.5 text-sky-400 font-semibold">
                <Cpu className="w-3.5 h-3.5" /> Model Router:
              </span>
              <span className="font-mono bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20 text-sky-300">
                Autonomous Reasoning Engine (v1.0)
              </span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span>Parallel Preparation:</span>
              <span className="text-emerald-400 font-semibold">ThreadPoolExecutor (5 Workers)</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span>Voice Engine:</span>
              <span className="text-amber-400 font-mono">Neural Edge-TTS (ChristopherNeural)</span>
            </div>
          </div>

          {/* Timeline of Node Executions */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <GitBranch className="w-3.5 h-3.5 text-brand-400" />
              <span>Execution Graph Trace</span>
            </h4>

            <div className="space-y-2.5">
              {logs.map((log, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 hover:border-slate-700 transition-colors text-xs space-y-1"
                >
                  <div className="flex items-center justify-between font-mono">
                    <span className="px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 font-semibold text-[10px]">
                      {log.node}
                    </span>
                    <span className="text-[10px] text-slate-500">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-slate-300 leading-relaxed pt-1">{log.detail}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-slate-800 text-center text-[11px] text-slate-500">
          AI Teacher Platform • Production Observability Active
        </div>
      </div>
    </div>
  );
}
