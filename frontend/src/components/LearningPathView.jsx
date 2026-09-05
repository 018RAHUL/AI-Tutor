import { apiFetch } from '../api';
import React, { useState, useEffect } from 'react';
import { Compass, CheckCircle2, Lock, Play, ArrowRight, Activity, Sparkles } from 'lucide-react';

export default function LearningPathView({ topic = "Ohm's Law", onSelectTopic }) {
  const [pathData, setPathData] = useState(null);

  useEffect(() => {
    apiFetch(`/api/learning-path/${encodeURIComponent(topic)}`)
      .then((res) => res.json())
      .then((data) => setPathData(data))
      .catch(() => {
        setPathData({
          topic,
          domain: 'Physics',
          nodes: [
            { id: 'node_1', title: 'Electric Charge & Voltage Potential', status: 'completed', duration: '15 min' },
            { id: 'node_2', title: "Ohm's Law & Resistance", status: 'in_progress', duration: '20 min' },
            { id: 'node_3', title: 'Series and Parallel Resistor Circuits', status: 'locked', duration: '30 min' },
            { id: 'node_4', title: "Kirchhoff's Current and Voltage Laws", status: 'locked', duration: '45 min' },
            { id: 'node_5', title: 'Power Dissipation & Energy Transfer (P = I²R)', status: 'locked', duration: '30 min' }
          ]
        });
      });
  }, [topic]);

  const nodes = pathData?.nodes || [];

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-400 text-xs font-semibold mb-2">
            <Compass className="w-3.5 h-3.5" />
            <span>Personalized Learning Curriculum Roadmap</span>
          </div>
          <h2 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Learning Path: <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-brand-400">{topic} & Electronics</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Dynamic prerequisite map calibrated from student mastery and misconception resolution.
          </p>
        </div>
      </div>

      {/* Nodes Roadmap */}
      <div className="relative pl-6 sm:pl-10 space-y-6 before:absolute before:left-3 sm:before:left-5 before:top-4 before:bottom-4 before:w-0.5 before:bg-gradient-to-b before:from-emerald-500 before:via-brand-500 before:to-slate-800">
        {nodes.map((node, idx) => {
          const isCompleted = node.status === 'completed';
          const isInProgress = node.status === 'in_progress';
          const isLocked = node.status === 'locked';

          return (
            <div key={node.id} className="relative flex items-start gap-4">
              {/* Marker Icon */}
              <div
                className={`absolute -left-6 sm:-left-10 mt-1.5 w-6 h-6 sm:w-7 sm:h-7 rounded-full flex items-center justify-center border-2 ${
                  isCompleted
                    ? 'bg-emerald-500 border-emerald-400 text-white shadow-lg shadow-emerald-500/30'
                    : isInProgress
                    ? 'bg-brand-500 border-sky-400 text-white shadow-lg shadow-brand-500/30 animate-pulse'
                    : 'bg-slate-900 border-slate-700 text-slate-500'
                }`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                ) : isInProgress ? (
                  <Play className="w-3 h-3 fill-current ml-0.5" />
                ) : (
                  <Lock className="w-3 h-3" />
                )}
              </div>

              {/* Card */}
              <div
                className={`flex-1 p-5 rounded-2xl glass-card border transition-all ${
                  isInProgress
                    ? 'border-brand-500/50 bg-slate-900/90 shadow-xl shadow-brand-500/10'
                    : isCompleted
                    ? 'border-emerald-500/30 bg-slate-900/60'
                    : 'border-slate-800 opacity-60'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <span
                      className={`text-[10px] font-bold uppercase tracking-wider ${
                        isCompleted ? 'text-emerald-400' : isInProgress ? 'text-brand-400' : 'text-slate-500'
                      }`}
                    >
                      Step {idx + 1} • {node.duration}
                    </span>
                    <h3 className="text-base font-bold text-slate-100 mt-0.5">{node.title}</h3>
                  </div>

                  {!isLocked && (
                    <button
                      onClick={() => onSelectTopic(node.title, 'Beginner')}
                      className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                        isInProgress
                          ? 'bg-brand-500 hover:bg-brand-600 text-white shadow-md'
                          : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                      }`}
                    >
                      <span>{isCompleted ? 'Review' : 'Continue'}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
