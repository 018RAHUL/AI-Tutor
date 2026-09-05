import React, { useState } from 'react';
import { Upload, BookOpen, Clock, Sliders, Sparkles, FileText, CheckCircle2, ArrowRight, Cpu, ChevronDown, ChevronUp } from 'lucide-react';

export default function CreateLesson({ onGenerateLesson, isLoading }) {
  const [mode, setMode] = useState('topic'); // 'topic' or 'upload'
  const [topic, setTopic] = useState("Agentic AI");
  const [studentLevel, setStudentLevel] = useState('Beginner');
  const [teachingStyle, setTeachingStyle] = useState('Visual');
  const [durationTarget, setDurationTarget] = useState('20 min');
  const [learningGoal, setLearningGoal] = useState('Master core principles, visual mechanisms, and real-world application.');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerateLesson({
      topic: mode === 'topic' ? topic : (uploadedFile?.name || 'Uploaded Educational Material'),
      student_level: studentLevel,
      teaching_style: teachingStyle,
      duration_target: durationTarget,
      source_type: mode,
      source_file: uploadedFile,
    });
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl space-y-8">
        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-400 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Curriculum & 1080p Studio Video Generator</span>
          </div>
          <h2 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">Create an Interactive AI Video Lesson</h2>
          <p className="text-sm text-slate-400 mt-1">
            Specify any topic or upload course material to generate a synchronized, high-depth educational video lesson with real formulas, diagrams, and AI voice narration.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Mode Selector: Topic vs Upload */}
          <div className="grid grid-cols-2 gap-3 p-1.5 rounded-2xl bg-slate-900 border border-slate-800">
            <button
              type="button"
              onClick={() => setMode('topic')}
              className={`flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-semibold transition-all ${
                mode === 'topic' ? 'bg-gradient-to-r from-brand-500 to-sky-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Teach Any Topic</span>
            </button>
            <button
              type="button"
              onClick={() => setMode('upload')}
              className={`flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-semibold transition-all ${
                mode === 'upload' ? 'bg-gradient-to-r from-brand-500 to-sky-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Upload className="w-4 h-4" />
              <span>Upload Document (PDF / RAG)</span>
            </button>
          </div>

          {/* Input Area */}
          {mode === 'topic' ? (
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Lesson Topic</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g. Agentic AI, Quantum Computing, Photosynthesis, Ohm's Law, Binary Search..."
                required
                className="w-full px-4 py-3 rounded-xl bg-slate-900/90 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 text-sm"
              />
              <div className="flex flex-wrap gap-2 pt-1">
                <span className="text-[11px] text-slate-400">Quick suggestions:</span>
                {["Agentic AI", "Quantum Superposition", "LangChain & RAG", "Photosynthesis", "Neural Networks", "Ohm's Law"].map(t => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setTopic(t)}
                    className="text-[11px] px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 hover:bg-brand-500/20 hover:text-brand-300 border border-slate-700 transition"
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Upload Course Document (PDF)</label>
              <div className="border-2 border-dashed border-slate-700 hover:border-brand-500/50 rounded-2xl p-6 text-center bg-slate-900/50 cursor-pointer transition-colors">
                <input
                  type="file"
                  accept=".pdf,.txt,.md"
                  onChange={(e) => setUploadedFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="pdf-upload"
                />
                <label htmlFor="pdf-upload" className="cursor-pointer flex flex-col items-center gap-2">
                  <div className="w-12 h-12 rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-400">
                    <FileText className="w-6 h-6" />
                  </div>
                  <span className="text-sm font-semibold text-slate-200">
                    {uploadedFile ? uploadedFile.name : 'Click to select educational document or PDF'}
                  </span>
                  <span className="text-xs text-slate-400">PDF, TXT, or Markdown parsed and indexed for persistent RAG retrieval</span>
                </label>
              </div>
            </div>
          )}

          {/* Learning Goal */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Learning Goal</label>
            <input
              type="text"
              value={learningGoal}
              onChange={(e) => setLearningGoal(e.target.value)}
              placeholder="e.g. Master fundamental mechanisms, mathematical derivations, and physical intuition."
              className="w-full px-4 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-slate-100 text-xs focus:outline-none focus:border-brand-500"
            />
          </div>

          {/* Grid of Settings */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
            {/* Student Level */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Student Level</label>
              <div className="grid grid-cols-3 gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs">
                {['Beginner', 'Intermediate', 'Advanced'].map((lvl) => (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => setStudentLevel(lvl)}
                    className={`py-2 rounded-lg font-medium transition-all ${
                      studentLevel === lvl ? 'bg-brand-500 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
            </div>

            {/* Teaching Style */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Teaching Style</label>
              <select
                value={teachingStyle}
                onChange={(e) => setTeachingStyle(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-200 text-xs focus:outline-none focus:border-brand-500"
              >
                <option value="Visual">Visual & Demonstrative</option>
                <option value="Simple">Simple & Intuitive</option>
                <option value="Practical">Practical & Applied</option>
                <option value="Technical">Technical & Rigorous</option>
                <option value="Socratic">Socratic & Inquisitive</option>
              </select>
            </div>

            {/* Duration Target */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Target Duration</label>
              <div className="grid grid-cols-4 gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs">
                {['5 min', '20 min', '60 min', '7 days'].map((dur) => (
                  <button
                    key={dur}
                    type="button"
                    onClick={() => setDurationTarget(dur)}
                    className={`py-2 rounded-lg font-medium text-[11px] transition-all ${
                      durationTarget === dur ? 'bg-sky-500 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {dur}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* AI Generation Engine Settings */}
          <div className="border border-slate-800 rounded-2xl p-4 bg-slate-900/40">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="w-full flex items-center justify-between text-left text-xs font-semibold text-slate-300 hover:text-white"
            >
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-brand-400" />
                <span>AI Generation Engine</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/25 text-emerald-300 font-mono">
                  Server-managed routing
                </span>
              </div>
              {showAdvanced ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
            </button>
            {showAdvanced && (
              <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-3 text-xs text-slate-400">
                <p>Model credentials stay on the backend. The server selects an available provider and applies safe fallbacks automatically.</p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  <div className="rounded-xl border border-white/5 bg-slate-950/50 p-3"><b className="text-slate-200">Secure</b><br/>No API keys are sent through the browser.</div>
                  <div className="rounded-xl border border-white/5 bg-slate-950/50 p-3"><b className="text-slate-200">Adaptive</b><br/>Lesson depth follows student level and style.</div>
                  <div className="rounded-xl border border-white/5 bg-slate-950/50 p-3"><b className="text-slate-200">Resilient</b><br/>Configured provider failures can fall back safely.</div>
                </div>
              </div>
            )}
          </div>

          {/* Submit Action */}
          <div className="pt-4 border-t border-slate-800 flex items-center justify-end">
            <button
              type="submit"
              disabled={isLoading}
              className="flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-brand-500 via-sky-500 to-indigo-600 hover:from-brand-600 hover:to-indigo-700 text-white font-bold text-sm shadow-xl shadow-brand-500/25 transition-all disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Synthesizing Deep Topic Graphics & Audio...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Generate Educational Lesson Video</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
