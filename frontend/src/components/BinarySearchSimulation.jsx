import React, { useState } from 'react';
import { Code, Search, CheckCircle, ArrowRight } from 'lucide-react';

export default function BinarySearchSimulation({ visualPayload }) {
  const [activeStep, setActiveStep] = useState(0);
  const data = visualPayload || {
    target: 23,
    initial_array: [2, 5, 8, 12, 16, 23, 38],
    iterations: [
      { step: 1, low: 0, high: 6, mid: 3, mid_val: 12, comparison: '23 > 12', action: 'Target > 12: Discard left half [2, 5, 8, 12]', eliminated: [0, 1, 2, 3] },
      { step: 2, low: 4, high: 6, mid: 5, mid_val: 23, comparison: '23 == 23', action: 'Target == 23: Direct match discovered at index 5!', eliminated: [0, 1, 2, 3, 4, 6], found: true }
    ]
  };

  const currentIter = data.iterations[activeStep] || data.iterations[0];

  return (
    <div className="w-full h-full flex flex-col justify-between p-4 bg-slate-950/80 rounded-2xl border border-slate-800 text-slate-100">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2 text-sky-400 font-semibold text-sm">
          <Search className="w-4 h-4" />
          <span>Binary Search Divide & Conquer: Target = {data.target || 23}</span>
        </div>
        <div className="flex gap-2">
          {data.iterations.map((it, idx) => (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                activeStep === idx ? 'bg-sky-500 text-white shadow-md' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              Step {idx + 1}
            </button>
          ))}
        </div>
      </div>

      {/* Array Element Boxes with Pointers */}
      <div className="my-auto flex flex-col items-center py-4">
        <div className="flex items-center gap-2 sm:gap-3">
          {(data.initial_array || [2, 5, 8, 12, 16, 23, 38]).map((val, idx) => {
            const isMid = idx === currentIter.mid;
            const isEliminated = currentIter.eliminated?.includes(idx);
            const isFound = isMid && currentIter.found;

            return (
              <div key={idx} className="flex flex-col items-center">
                {/* Pointer Label Top */}
                <div className="h-5 text-[10px] font-mono font-bold">
                  {idx === currentIter.low && <span className="text-amber-400">L</span>}
                  {idx === currentIter.high && <span className="text-purple-400 ml-1">H</span>}
                </div>

                {/* Box */}
                <div
                  className={`w-10 h-12 sm:w-12 sm:h-14 rounded-xl flex items-center justify-center font-mono font-bold text-base transition-all duration-300 border ${
                    isFound
                      ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300 shadow-lg shadow-emerald-500/30 scale-110'
                      : isMid
                      ? 'bg-sky-500/20 border-sky-400 text-sky-300 shadow-lg shadow-sky-500/30 scale-105'
                      : isEliminated
                      ? 'bg-slate-900/50 border-slate-800 text-slate-600 opacity-40 line-through'
                      : 'bg-slate-900 border-slate-700 text-slate-200'
                  }`}
                >
                  {val}
                </div>

                {/* Index & Mid Label */}
                <div className="mt-1.5 text-[10px] text-slate-500 font-mono">[{idx}]</div>
                {isMid && (
                  <span className="text-[10px] font-bold text-sky-400 uppercase tracking-tighter">MID</span>
                )}
              </div>
            );
          })}
        </div>

        {/* Step Explanation Banner */}
        <div className="mt-6 p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-center max-w-md w-full">
          <div className="text-xs font-mono text-sky-300 font-semibold mb-1">
            Comparison: <span className="text-amber-300">{currentIter.comparison}</span>
          </div>
          <div className="text-xs text-slate-300">{currentIter.action}</div>
        </div>
      </div>

      {/* Code Snippet Trace */}
      <div className="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800/80 font-mono text-[11px] text-slate-400 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Code className="w-3.5 h-3.5 text-sky-400" />
          <span>Time Complexity: <strong className="text-emerald-400">O(log n)</strong></span>
        </div>
        <div className="text-slate-400">
          Search space halved each comparison: 7 → 3 → 1
        </div>
      </div>
    </div>
  );
}
