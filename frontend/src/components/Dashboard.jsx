import React from 'react';
import { Play, Sparkles, BookOpen, Clock, Award, ArrowRight, Zap, Search, Sigma } from 'lucide-react';

export default function Dashboard({ onStartLesson, onSelectTopic }) {
  const quickDemos = [
    {
      topic: "Ohm's Law",
      subject: "Physics",
      level: "Beginner",
      duration: "2–4 min",
      description: "Interactive circuit simulations, water pipe analogy, V = IR formula derivation, and live misconception detection.",
      badge: "Primary Demo Benchmark",
      badgeColor: "bg-brand-500/20 text-brand-300 border-brand-500/40",
      icon: Zap,
      accent: "from-sky-500/20 to-brand-500/10"
    },
    {
      topic: "Binary Search Algorithm",
      subject: "Computer Science",
      level: "Beginner",
      duration: "2–3 min",
      description: "Divide-and-conquer visual pointer animation, array halving steps, and logarithmic O(log n) efficiency.",
      badge: "Algorithms & CS",
      badgeColor: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
      icon: Search,
      accent: "from-emerald-500/20 to-teal-500/10"
    },
    {
      topic: "Quadratic Equations",
      subject: "Mathematics",
      level: "Intermediate",
      duration: "3–4 min",
      description: "Parabolic curves, roots, discriminant calculations, and step-by-step formula substitutions.",
      badge: "Algebra & Math",
      badgeColor: "bg-purple-500/20 text-purple-300 border-purple-500/40",
      icon: Sigma,
      accent: "from-purple-500/20 to-indigo-500/10"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 lg:px-8 py-8 space-y-10">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl p-8 lg:p-12 glass-panel border border-brand-500/30 bg-gradient-to-br from-slate-900 via-[#0b1329] to-[#081b36] shadow-2xl">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-brand-500/15 blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Educational Video Generator & Interactive Teacher</span>
          </div>

          <h1 className="text-3xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Learn Visually with an <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-brand-400 to-indigo-300">Adaptive AI Tutor</span>
          </h1>

          <p className="text-sm lg:text-base text-slate-300 font-normal leading-relaxed">
            Transform any concept into a 2+ minute scene-based educational video complete with animated teacher avatar, synchronized dynamic visuals, equations, worked examples, and real-time misconception remediation.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            <button
              onClick={() => onSelectTopic("Ohm's Law", "Beginner")}
              className="flex items-center gap-2.5 px-6 py-3 rounded-xl bg-gradient-to-r from-brand-500 to-sky-600 hover:from-brand-600 hover:to-sky-700 text-white font-semibold text-sm shadow-lg shadow-brand-500/25 transition-all transform hover:-translate-y-0.5"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Launch Primary Demo (Ohm's Law)</span>
            </button>

            <button
              onClick={onStartLesson}
              className="flex items-center gap-2 px-6 py-3 rounded-xl glass-card hover:bg-white/10 text-slate-200 font-semibold text-sm border border-white/10 transition-all"
            >
              <BookOpen className="w-4 h-4 text-sky-400" />
              <span>Create Custom Lesson</span>
            </button>
          </div>
        </div>
      </div>

      {/* Quick Launch Lessons */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Featured Interactive Lessons</h2>
            <p className="text-xs text-slate-400">Pre-calibrated 2+ minute visual lessons with live simulation stages</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickDemos.map((demo, idx) => {
            const Icon = demo.icon;
            return (
              <div
                key={idx}
                className="group relative flex flex-col justify-between p-6 rounded-2xl glass-card border border-white/10 hover:border-brand-500/40 transition-all duration-300 hover:shadow-xl hover:shadow-brand-500/10"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${demo.badgeColor}`}>
                      {demo.badge}
                    </span>
                    <span className="flex items-center gap-1 text-slate-400 text-xs">
                      <Clock className="w-3.5 h-3.5" />
                      {demo.duration}
                    </span>
                  </div>

                  <div className="flex items-center gap-3 pt-1">
                    <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-sky-400 group-hover:scale-110 transition-transform">
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-slate-100 group-hover:text-sky-300 transition-colors">{demo.topic}</h3>
                      <div className="text-[11px] text-slate-400">{demo.subject} • {demo.level}</div>
                    </div>
                  </div>

                  <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed">
                    {demo.description}
                  </p>
                </div>

                <div className="pt-6">
                  <button
                    onClick={() => onSelectTopic(demo.topic, demo.level)}
                    className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-slate-900 hover:bg-brand-500 hover:text-white text-slate-200 border border-slate-800 hover:border-brand-500 text-xs font-semibold transition-all group-hover:shadow-md"
                  >
                    <span>Start Lesson</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Student Mastery & Analytics Snapshot */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-5 rounded-2xl border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">88%</div>
            <div className="text-xs text-slate-400">Circuit Mastery</div>
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">6</div>
            <div className="text-xs text-slate-400">Lessons Completed</div>
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <Zap className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">100%</div>
            <div className="text-xs text-slate-400">Misconceptions Remedied</div>
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">2.5 min</div>
            <div className="text-xs text-slate-400">Avg Scene Duration</div>
          </div>
        </div>
      </div>
    </div>
  );
}
