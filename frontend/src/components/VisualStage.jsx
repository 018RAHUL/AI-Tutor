import React from 'react';
import CircuitSimulation from './CircuitSimulation';
import BinarySearchSimulation from './BinarySearchSimulation';
import MathSimulation from './MathSimulation';
import { Sparkles, Layers, BookOpen, Sun, Leaf, Zap, Activity, Atom, ArrowRight } from 'lucide-react';

export default function VisualStage({ scene, isPlaying = true, sceneIndex = 0 }) {
  if (!scene) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-slate-950/80 rounded-2xl border border-slate-800 text-slate-500">
        <Sparkles className="w-8 h-8 animate-pulse text-brand-400 mr-2" />
        <span>Preparing high-yield visual explanation...</span>
      </div>
    );
  }

  const vType = (scene.visual_type || '').toLowerCase();
  const vPayload = scene.visual_payload || {};
  const concept = scene.concept || '';
  const topic = scene.topic || '';
  const combined = (vType + ' ' + concept + ' ' + topic).toLowerCase();

  // 1. Ohm's Law & Circuit Interactive Simulator
  if (
    combined.includes('circuit') ||
    combined.includes('ohm') ||
    (combined.includes('water_analogy') && !combined.includes('photo'))
  ) {
    return <CircuitSimulation visualPayload={vPayload} sceneIndex={sceneIndex} isPlaying={isPlaying} />;
  }

  // 2. Computer Science & Binary Search Simulator
  if (combined.includes('binary_search') || combined.includes('search') || combined.includes('algorithm') || combined.includes('code')) {
    return <BinarySearchSimulation visualPayload={vPayload} />;
  }

  // 3. Mathematics & Quadratic Simulator
  if (combined.includes('quadratic') || combined.includes('parabola') || combined.includes('algebra')) {
    return <MathSimulation visualPayload={vPayload} />;
  }

  // 4. Biology & Photosynthesis Visual Stage
  if (combined.includes('photosynthesis') || combined.includes('biology') || combined.includes('chloroplast') || combined.includes('plant')) {
    return (
      <div className="w-full h-full flex flex-col justify-between p-6 bg-slate-950/90 rounded-2xl border border-emerald-500/30 text-slate-100 shadow-2xl">
        <div className="flex items-center justify-between border-b border-emerald-500/20 pb-3">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
            <Leaf className="w-5 h-5" />
            <span>{vPayload.title || 'Photosynthesis Biochemical Architecture'}</span>
          </div>
          <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            Chloroplast Stage
          </span>
        </div>

        {/* Master Chemical Formula Box */}
        <div className="my-2 p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/40 text-center shadow-lg">
          <div className="text-[11px] font-mono text-emerald-300 uppercase tracking-wider mb-1">
            Governing Reaction
          </div>
          <div className="text-sm sm:text-base font-bold text-emerald-200 font-mono">
            6CO₂ + 6H₂O + Light Energy ⟶ C₆H₁₂O₆ (Glucose) + 6O₂
          </div>
        </div>

        {/* Key Stages Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-auto">
          <div className="glass-card p-4 rounded-xl border border-sky-500/30 bg-sky-950/20">
            <div className="flex items-center gap-2 text-xs font-bold text-sky-400 uppercase tracking-wider mb-2">
              <Sun className="w-4 h-4 text-amber-400" />
              <span>1. Light-Dependent Reactions</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-2">
              Inside the <strong>Thylakoid membranes</strong>, chlorophyll absorbs solar photons to split water (photolysis):
            </p>
            <div className="p-2 rounded bg-slate-900 font-mono text-[11px] text-sky-300">
              2H₂O ⟶ 4H⁺ + 4e⁻ + O₂ ↑ (Releases Oxygen)
            </div>
          </div>

          <div className="glass-card p-4 rounded-xl border border-emerald-500/30 bg-emerald-950/20">
            <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">
              <Leaf className="w-4 h-4 text-emerald-400" />
              <span>2. Calvin Cycle (Carbon Fixation)</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-2">
              Inside the <strong>Stroma</strong>, ATP & NADPH energy carriers drive CO₂ fixation into organic sugar:
            </p>
            <div className="p-2 rounded bg-slate-900 font-mono text-[11px] text-emerald-300">
              CO₂ + Energy Carriers ⟶ C₆H₁₂O₆ (Glucose)
            </div>
          </div>
        </div>

        {/* Footer Objective */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-emerald-400" />
            <span>Objective: {scene.learning_objective || 'Master photosynthesis chemical pathways'}</span>
          </div>
          <span className="text-slate-400">Chapter {scene.order_index}</span>
        </div>
      </div>
    );
  }

  // 5. Physics Mechanics & Newton's Laws Visual Stage
  if (combined.includes('newton') || combined.includes('force') || combined.includes('motion') || combined.includes('gravity') || combined.includes('acceleration')) {
    return (
      <div className="w-full h-full flex flex-col justify-between p-6 bg-slate-950/90 rounded-2xl border border-sky-500/30 text-slate-100 shadow-2xl">
        <div className="flex items-center justify-between border-b border-sky-500/20 pb-3">
          <div className="flex items-center gap-2 text-sky-400 font-bold text-sm">
            <Activity className="w-5 h-5" />
            <span>{vPayload.title || "Newton's Laws of Classical Dynamics"}</span>
          </div>
          <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30">
            Classical Mechanics
          </span>
        </div>

        {/* Formula HUD */}
        <div className="my-2 p-3.5 rounded-xl bg-slate-900/90 border border-sky-500/40 text-center shadow-lg">
          <div className="text-[11px] font-mono text-sky-300 uppercase tracking-wider mb-1">
            Governing Dynamics Formula
          </div>
          <div className="text-base sm:text-lg font-bold text-white font-mono">
            F_net = m × a  ⟹  Acceleration: a = F_net / m
          </div>
        </div>

        {/* 3 Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 my-auto">
          <div className="glass-card p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
            <div className="text-xs font-bold text-sky-400 mb-1">1st Law (Inertia)</div>
            <div className="text-[11px] text-slate-300 leading-relaxed">
              Objects resist velocity changes. Uniform velocity persists unless unbalanced net force acts.
            </div>
          </div>

          <div className="glass-card p-3.5 rounded-xl border border-sky-500/40 bg-sky-950/30 shadow-md">
            <div className="text-xs font-bold text-sky-300 mb-1">2nd Law (F = ma)</div>
            <div className="text-[11px] text-slate-300 leading-relaxed">
              Net force causes proportional acceleration. Doubling mass cuts acceleration by 50%.
            </div>
          </div>

          <div className="glass-card p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
            <div className="text-xs font-bold text-amber-400 mb-1">3rd Law (Action-Reaction)</div>
            <div className="text-[11px] text-slate-300 leading-relaxed">
              Every applied force produces an equal, opposite reaction on the interacting body.
            </div>
          </div>
        </div>

        {/* Footer Objective */}
        <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-sky-400" />
            <span>Objective: {scene.learning_objective || 'Master classical force and dynamic motion'}</span>
          </div>
          <span className="text-slate-400">Chapter {scene.order_index}</span>
        </div>
      </div>
    );
  }

  // 6. Universal Dynamic Topic Visual Stage
  const keyPoints = vPayload.key_points || [
    { label: 'Fundamental Principle', detail: `Core mechanism governing ${concept || topic}.` },
    { label: 'Underlying Interaction', detail: 'Observed cause and effect relationship across driving parameters.' },
    { label: 'Practical Application', detail: 'Direct mathematical, scientific, and engineering application.' }
  ];

  return (
    <div className="w-full h-full flex flex-col justify-between p-6 bg-slate-950/80 rounded-2xl border border-slate-800 text-slate-100 shadow-2xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2 text-sky-400 font-semibold text-sm">
          <Layers className="w-4 h-4" />
          <span>{vPayload.title || scene.concept || `Core Tenets: ${topic}`}</span>
        </div>
        <span className="px-2.5 py-1 rounded-full text-[10px] font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30">
          {topic || 'Concept Study'}
        </span>
      </div>

      {vPayload.formula && (
        <div className="my-2 p-3 rounded-xl bg-slate-900/90 border border-sky-500/30 text-center">
          <div className="text-[10px] font-mono text-sky-400 uppercase tracking-wider mb-0.5">Core Relationship</div>
          <div className="text-sm font-bold text-white font-mono">{vPayload.formula}</div>
        </div>
      )}

      <div className="my-auto grid grid-cols-1 md:grid-cols-3 gap-4">
        {keyPoints.map((pt, idx) => (
          <div key={idx} className="glass-card p-4 rounded-xl border border-slate-800 hover:border-sky-500/40 transition-all bg-slate-900/40">
            <div className="text-xs font-semibold text-sky-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
              <span>{pt.label}</span>
            </div>
            <div className="text-xs text-slate-300 leading-relaxed">{pt.detail}</div>
          </div>
        ))}
      </div>

      <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-sky-400" />
          <span>Objective: {scene.learning_objective || `Master the principles of ${topic}`}</span>
        </div>
        <span className="text-slate-400">Chapter {scene.order_index}</span>
      </div>
    </div>
  );
}
