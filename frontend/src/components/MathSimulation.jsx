import React from 'react';
import { Sigma, TrendingUp } from 'lucide-react';

export default function MathSimulation({ visualPayload }) {
  const data = visualPayload || {};

  return (
    <div className="w-full h-full flex flex-col justify-between p-4 bg-slate-950/80 rounded-2xl border border-slate-800 text-slate-100">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2 text-purple-400 font-semibold text-sm">
          <Sigma className="w-4 h-4" />
          <span>{data.title || "Mathematical Formulation & Analysis"}</span>
        </div>
      </div>

      <div className="my-auto flex flex-col items-center justify-center p-4">
        {/* Main Equation */}
        <div className="text-3xl sm:text-4xl font-mono font-bold text-slate-100 bg-purple-500/10 border border-purple-500/30 px-6 py-3 rounded-2xl shadow-lg">
          {data.quadratic_formula || "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"}
        </div>

        {/* Worked Breakdown */}
        {data.worked_example && (
          <div className="mt-6 grid grid-cols-2 gap-4 w-full max-w-md text-xs">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-slate-400">Equation:</div>
              <div className="font-mono font-bold text-slate-200 mt-0.5">{data.worked_example.equation}</div>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <div className="text-slate-400">Discriminant:</div>
              <div className="font-mono font-bold text-purple-300 mt-0.5">{data.worked_example.discriminant}</div>
            </div>
            <div className="col-span-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center">
              <div className="text-emerald-400 font-semibold">Roots:</div>
              <div className="font-mono font-bold text-emerald-300 text-sm mt-0.5">{data.worked_example.roots?.join(', ')}</div>
            </div>
          </div>
        )}
      </div>

      <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 text-center font-mono">
        Vertex at (2.5, -0.25) | Two distinct real roots
      </div>
    </div>
  );
}
