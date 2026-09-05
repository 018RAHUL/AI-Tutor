import React, { useState } from 'react';
import { Award, CheckCircle2, XCircle, ArrowRight, RotateCcw, Sparkles, BookOpen, Compass } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function AssessmentView({ assessmentData, onRestart, onExploreLearningPath }) {
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const quiz = assessmentData?.assessment_plan || {
    quiz_title: "Ohm's Law Mastery Evaluation",
    questions: [
      {
        id: "quiz_1",
        question: "What is the SI unit of electrical resistance?",
        options: ["Volt (V)", "Ampere (A)", "Ohm (Ω)", "Watt (W)"],
        correct_answer: "Ohm (Ω)",
        explanation: "Resistance is measured in Ohms, denoted by the Greek letter Omega (Ω)."
      },
      {
        id: "quiz_2",
        question: "If a 9V battery is connected across a 3Ω resistor, what current flows?",
        options: ["27 A", "3 A", "0.33 A", "6 A"],
        correct_answer: "3 A",
        explanation: "Using I = V / R: I = 9V / 3Ω = 3 Amperes."
      },
      {
        id: "quiz_3",
        question: "In the water pipe analogy, what represents Voltage?",
        options: ["The width of the pipe", "Water pressure pushing through the pipe", "The total volume of water", "Friction in the pipe"],
        correct_answer: "Water pressure pushing through the pipe",
        explanation: "Voltage is electrical potential difference, analogous to water pressure."
      }
    ]
  };

  const handleSelect = (qId, option) => {
    if (submitted) return;
    setSelectedAnswers({ ...selectedAnswers, [qId]: option });
  };

  const handleSubmitQuiz = () => {
    setSubmitted(true);
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  // Calculate score
  const score = quiz.questions?.reduce((acc, q) => {
    return selectedAnswers[q.id] === q.correct_answer ? acc + 1 : acc;
  }, 0) || 3;
  const percentage = Math.round((score / (quiz.questions?.length || 3)) * 100);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header Banner */}
      <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 mx-auto flex items-center justify-center text-white shadow-xl shadow-emerald-500/25">
          <Award className="w-8 h-8" />
        </div>

        <h2 className="text-3xl font-extrabold text-white tracking-tight">Lesson Assessment & Mastery Report</h2>
        <p className="text-xs text-slate-300 max-w-md mx-auto">
          Validate your conceptual understanding and physical intuition through formative questions.
        </p>

        {submitted && (
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-bold text-sm">
            <Sparkles className="w-4 h-4" />
            <span>Mastery Score: {percentage}% ({score}/{quiz.questions?.length} Correct)</span>
          </div>
        )}
      </div>

      {/* Quiz Questions List */}
      <div className="space-y-4">
        {quiz.questions?.map((q, idx) => {
          const isChosen = selectedAnswers[q.id];
          const isCorrect = isChosen === q.correct_answer;

          return (
            <div key={q.id} className="glass-card p-6 rounded-2xl border border-white/10 space-y-4">
              <div className="flex items-start justify-between">
                <h4 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <span className="w-6 h-6 rounded-lg bg-slate-800 flex items-center justify-center text-xs text-sky-400">
                    {idx + 1}
                  </span>
                  <span>{q.question}</span>
                </h4>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {q.options.map((opt, optIdx) => {
                  const isOptSelected = selectedAnswers[q.id] === opt;
                  const isOptCorrect = opt === q.correct_answer;

                  let btnStyle = 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800';
                  if (submitted) {
                    if (isOptCorrect) btnStyle = 'bg-emerald-500/20 border-emerald-500 text-emerald-300';
                    else if (isOptSelected && !isOptCorrect) btnStyle = 'bg-rose-500/20 border-rose-500 text-rose-300';
                  } else if (isOptSelected) {
                    btnStyle = 'bg-brand-500/20 border-brand-500 text-brand-300';
                  }

                  return (
                    <button
                      key={optIdx}
                      type="button"
                      onClick={() => handleSelect(q.id, opt)}
                      className={`p-3 rounded-xl text-left text-xs font-medium border transition-all ${btnStyle}`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>

              {submitted && (
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-sky-400 shrink-0" />
                  <span>{q.explanation}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onRestart}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl glass-card text-slate-300 hover:text-white border border-slate-800 text-xs font-semibold transition-all"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Replay Lesson</span>
          </button>

          {onOpenSummary && (
            <button
              onClick={onOpenSummary}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-300 border border-sky-500/30 text-xs font-semibold transition-all"
            >
              <BookOpen className="w-4 h-4" />
              <span>Review Summary Hub</span>
            </button>
          )}
        </div>

        {!submitted ? (
          <button
            onClick={handleSubmitQuiz}
            className="flex items-center gap-2 px-8 py-3 rounded-xl bg-gradient-to-r from-brand-500 to-sky-600 text-white font-bold text-xs shadow-lg shadow-brand-500/25 transition-all"
          >
            <span>Submit Quiz & Generate Report</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        ) : (
          <button
            onClick={onExploreLearningPath}
            className="flex items-center gap-2 px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-bold text-xs shadow-lg shadow-emerald-500/25 transition-all"
          >
            <Compass className="w-4 h-4" />
            <span>Next Recommended Topic</span>
          </button>
        )}
      </div>
    </div>
  );
}
