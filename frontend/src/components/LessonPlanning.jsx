import React from 'react';
import { Play, Layers, Clock, Award, CheckCircle2, ListOrdered, Sparkles, BookOpen } from 'lucide-react';

export default function LessonPlanning({ lessonData, onStartPlayback }) {
  if (!lessonData) return null;

  const plan = lessonData.lesson_plan || {};
  const chapters = plan.chapters || [];
  const objectives = plan.learning_objectives || [];
  const prerequisites = plan.prerequisites || [];

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Header Banner */}
      <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/40">
              {lessonData.subject || 'Physics'}
            </span>
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
              {lessonData.student_level || 'Beginner'} Level
            </span>
            <span className="flex items-center gap-1 text-xs text-slate-400 font-medium">
              <Clock className="w-3.5 h-3.5 text-sky-400" />
              {Math.round(lessonData.estimated_duration_sec / 60)} min ({Math.round(lessonData.estimated_duration_sec)}s)
            </span>
          </div>

          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Lesson Plan: <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-brand-400">{lessonData.topic}</span>
          </h2>
          <p className="text-xs text-slate-400">
            Engineered through LangGraph parallel multi-agent preparation: Explanation, Visuals, Examples, and Questions.
          </p>
        </div>

        <button
          onClick={onStartPlayback}
          className="flex items-center gap-3 px-8 py-4 rounded-2xl bg-gradient-to-r from-brand-500 via-sky-500 to-indigo-600 hover:from-brand-600 hover:to-indigo-700 text-white font-bold text-sm shadow-xl shadow-brand-500/30 transition-all transform hover:-translate-y-0.5"
        >
          <Play className="w-5 h-5 fill-current" />
          <span>Enter AI Classroom</span>
        </button>
      </div>

      {/* Grid: Objectives & Prerequisites */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Learning Objectives */}
        <div className="glass-card p-6 rounded-2xl border border-white/10 space-y-4">
          <div className="flex items-center gap-2 text-sky-400 font-bold text-sm">
            <Award className="w-5 h-5" />
            <span>Target Learning Objectives</span>
          </div>
          <ul className="space-y-2.5">
            {objectives.map((obj, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{obj}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Prerequisites & Teaching Method */}
        <div className="glass-card p-6 rounded-2xl border border-white/10 space-y-4">
          <div className="flex items-center gap-2 text-purple-400 font-bold text-sm">
            <BookOpen className="w-5 h-5" />
            <span>Prerequisites & Method</span>
          </div>
          <div className="space-y-3 text-xs text-slate-300">
            <div>
              <span className="font-semibold text-slate-200">Recommended Prerequisites:</span>
              <ul className="mt-1.5 list-disc list-inside text-slate-400 space-y-1">
                {prerequisites.map((req, idx) => (
                  <li key={idx}>{req}</li>
                ))}
              </ul>
            </div>
            <div className="pt-2 border-t border-slate-800">
              <span className="font-semibold text-slate-200">Teaching Methodology:</span>
              <p className="mt-1 text-slate-400">
                Dynamic visual demonstrations, physical analogies, step-by-step mathematical calculations, and active checkpoint evaluation.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Chapter Breakdown Roadmap */}
      <div className="glass-card p-6 rounded-2xl border border-white/10 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-200 font-bold text-base">
            <ListOrdered className="w-5 h-5 text-sky-400" />
            <span>Curriculum Chapters & Visual Timeline</span>
          </div>
          <span className="text-xs text-slate-400">{chapters.length} Scenes Prepared</span>
        </div>

        <div className="space-y-3">
          {chapters.map((chap, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-sky-500/30 transition-all"
            >
              <div className="flex items-center gap-3.5">
                <div className="w-8 h-8 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center font-bold text-xs text-sky-400">
                  {idx + 1}
                </div>
                <div>
                  <h4 className="font-semibold text-sm text-slate-200">{chap.title}</h4>
                  <div className="text-xs text-slate-400">Synchronized visual simulation and spoken script</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-slate-400">~{chap.estimated_sec}s</span>
                <span className="px-2.5 py-1 rounded-md bg-slate-800 text-[11px] font-medium text-slate-300 border border-slate-700">
                  {idx === 4 ? 'Interactive Checkpoint' : 'Visual Lesson'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
