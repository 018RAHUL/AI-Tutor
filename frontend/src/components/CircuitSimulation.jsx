import React, { useState, useEffect, useRef } from 'react';
import { Zap, Activity, Gauge, Flame, AlertCircle, Waves, Cpu, Sparkles } from 'lucide-react';

export default function CircuitSimulation({ visualPayload, sceneIndex = 0, isPlaying = true }) {
  const circuitCanvasRef = useRef(null);
  const fluidCanvasRef = useRef(null);
  const oscilloCanvasRef = useRef(null);

  const [voltage, setVoltage] = useState(12);
  const [resistance, setResistance] = useState(4);
  const current = (voltage / resistance).toFixed(2);
  const vType = visualPayload?.type || 'circuit_intro';

  // 1. Continuous 60 FPS Animated Circuit Simulation with moving charges & glowing wires
  useEffect(() => {
    const canvas = circuitCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let particles = [];
    const numParticles = 32;

    const padX = 40;
    const padY = 35;
    const w = canvas.width - padX * 2;
    const h = canvas.height - padY * 2;
    const perimeter = 2 * (w + h);

    for (let i = 0; i < numParticles; i++) {
      particles.push({
        progress: (i / numParticles) * perimeter,
        size: 3.5 + Math.random() * 1.5
      });
    }

    let waveOffset = 0;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      waveOffset += 0.05;

      // Glow background field
      const glowGrad = ctx.createRadialGradient(canvas.width / 2, canvas.height / 2, 20, canvas.width / 2, canvas.height / 2, 160);
      glowGrad.addColorStop(0, 'rgba(14, 165, 233, 0.08)');
      glowGrad.addColorStop(1, 'rgba(15, 23, 42, 0)');
      ctx.fillStyle = glowGrad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Base copper wire loop
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 10;
      ctx.lineJoin = 'round';
      ctx.strokeRect(padX, padY, w, h);

      // Glowing current conduit
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 3;
      ctx.shadowColor = '#38bdf8';
      ctx.shadowBlur = 10;
      ctx.strokeRect(padX, padY, w, h);
      ctx.shadowBlur = 0;

      // Speed of electrons proportional to current I
      const speed = isPlaying ? Math.max(0.6, parseFloat(current) * 0.9) : 0;

      // Draw flowing electron charges with light trails
      particles.forEach((p) => {
        p.progress = (p.progress + speed) % perimeter;
        let x = padX;
        let y = padY;
        let d = p.progress;

        if (d < w) {
          x = padX + d;
          y = padY;
        } else if (d < w + h) {
          x = padX + w;
          y = padY + (d - w);
        } else if (d < 2 * w + h) {
          x = padX + w - (d - (w + h));
          y = padY + h;
        } else {
          x = padX;
          y = padY + h - (d - (2 * w + h));
        }

        // Particle Core
        ctx.beginPath();
        ctx.arc(x, y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = '#38bdf8';
        ctx.shadowColor = '#38bdf8';
        ctx.shadowBlur = 12;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      // Battery on Left Side
      const batY = padY + h / 2;
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(padX - 22, batY - 35, 44, 70);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2.5;
      ctx.strokeRect(padX - 22, batY - 35, 44, 70);

      // Battery Positive (+) & Negative (-) Plates
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(padX - 16, batY - 22, 32, 7);
      ctx.fillStyle = '#38bdf8';
      ctx.fillRect(padX - 10, batY + 15, 20, 7);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(`+${voltage}V`, padX - 15, batY - 26);
      ctx.fillText('-GND', padX - 14, batY + 36);

      // Resistor on Right Side (with thermal dissipation aura)
      const resY = padY + h / 2;
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(padX + w - 22, resY - 35, 44, 70);
      ctx.strokeStyle = '#f87171';
      ctx.lineWidth = 2.5;
      ctx.strokeRect(padX + w - 22, resY - 35, 44, 70);

      // Resistor Zigzag Coil
      ctx.strokeStyle = '#f87171';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(padX + w - 12, resY - 24);
      ctx.lineTo(padX + w + 12, resY - 12);
      ctx.lineTo(padX + w - 12, resY);
      ctx.lineTo(padX + w + 12, resY + 12);
      ctx.lineTo(padX + w - 12, resY + 24);
      ctx.stroke();

      ctx.fillStyle = '#fca5a5';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(`${resistance}Ω`, padX + w - 10, resY + 46);

      // Top Ammeter Gauge (Moving Analog Meter)
      const meterX = padX + w / 2;
      const meterY = padY;
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.arc(meterX, meterY, 26, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Needle deflecting proportional to Current
      const needleAngle = -Math.PI / 4 + (parseFloat(current) / 6) * (Math.PI / 2);
      ctx.strokeStyle = '#34d399';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(meterX, meterY);
      ctx.lineTo(meterX + Math.cos(needleAngle) * 18, meterY + Math.sin(needleAngle) * 18);
      ctx.stroke();

      ctx.fillStyle = '#6ee7b7';
      ctx.font = 'bold 10px monospace';
      ctx.fillText(`${current}A`, meterX - 12, meterY - 10);

      animId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animId);
  }, [voltage, resistance, current, isPlaying]);

  // 2. Animated Fluid Hydrodynamics Simulation for Water Analogy
  useEffect(() => {
    const canvas = fluidCanvasRef.current;
    if (!canvas || vType !== 'water_analogy') return;
    const ctx = canvas.getContext('2d');
    let animId;
    let waterParticles = [];
    const numFluid = 45;

    for (let i = 0; i < numFluid; i++) {
      waterParticles.push({
        x: Math.random() * canvas.width,
        y: 20 + Math.random() * (canvas.height - 40),
        speed: 1.5 + Math.random() * 2,
        radius: 2 + Math.random() * 3
      });
    }

    let impellerRot = 0;

    const renderFluid = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      impellerRot += isPlaying ? 0.08 : 0;

      // Draw Water Pipe Outline
      ctx.fillStyle = '#0b1329';
      ctx.fillRect(10, 20, canvas.width - 20, canvas.height - 40);

      // Pipe Borders
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(10, 20);
      ctx.lineTo(canvas.width - 10, 20);
      ctx.moveTo(10, canvas.height - 20);
      ctx.lineTo(canvas.width - 10, canvas.height - 20);
      ctx.stroke();

      // Constriction in middle (Narrow nozzle)
      ctx.fillStyle = '#f87171';
      ctx.beginPath();
      ctx.moveTo(canvas.width / 2 - 30, 20);
      ctx.lineTo(canvas.width / 2, 45);
      ctx.lineTo(canvas.width / 2 + 30, 20);
      ctx.fill();

      ctx.beginPath();
      ctx.moveTo(canvas.width / 2 - 30, canvas.height - 20);
      ctx.lineTo(canvas.width / 2, canvas.height - 45);
      ctx.lineTo(canvas.width / 2 + 30, canvas.height - 20);
      ctx.fill();

      // Water Particles Flow
      waterParticles.forEach((wp) => {
        // Accelerate when passing through constriction
        const inConstriction = Math.abs(wp.x - canvas.width / 2) < 40;
        const speedMult = inConstriction ? 2.2 : 1.0;
        wp.x += isPlaying ? wp.speed * speedMult : 0;

        if (wp.x > canvas.width - 10) wp.x = 15;

        ctx.beginPath();
        ctx.arc(wp.x, wp.y, wp.radius, 0, Math.PI * 2);
        ctx.fillStyle = inConstriction ? '#38bdf8' : '#0284c7';
        ctx.fill();
      });

      // Rotating Pump Impeller on Left
      ctx.save();
      ctx.translate(50, canvas.height / 2);
      ctx.rotate(impellerRot);
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (let i = 0; i < 4; i++) {
        ctx.rotate(Math.PI / 2);
        ctx.moveTo(0, 0);
        ctx.lineTo(0, -18);
      }
      ctx.stroke();
      ctx.restore();

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText('Water Pump (Voltage Push)', 15, canvas.height - 6);
      ctx.fillStyle = '#f87171';
      ctx.fillText('Constriction (Resistance R)', canvas.width / 2 - 60, canvas.height - 6);

      animId = requestAnimationFrame(renderFluid);
    };

    renderFluid();
    return () => cancelAnimationFrame(animId);
  }, [vType, isPlaying]);

  // 3. Live Oscilloscope Waveform Animation
  useEffect(() => {
    const canvas = oscilloCanvasRef.current;
    if (!canvas || vType !== 'worked_example') return;
    const ctx = canvas.getContext('2d');
    let animId;
    let waveT = 0;

    const renderWave = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      waveT += 0.04;

      // Oscilloscope Grid Lines
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Live Current Waveform Line (Steady DC with slight pulse)
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2.5;
      ctx.shadowColor = '#10b981';
      ctx.shadowBlur = 8;
      ctx.beginPath();

      const centerY = canvas.height - 30 - parseFloat(current) * 12;
      for (let x = 0; x < canvas.width; x++) {
        const y = centerY + Math.sin(x * 0.05 + waveT) * 2;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      ctx.fillStyle = '#34d399';
      ctx.font = 'bold 10px monospace';
      ctx.fillText(`DC CURRENT: ${current} A (STABLE)`, 8, 16);

      animId = requestAnimationFrame(renderWave);
    };

    renderWave();
    return () => cancelAnimationFrame(animId);
  }, [vType, current, isPlaying]);

  return (
    <div className="w-full h-full flex flex-col justify-between p-4 bg-slate-950/90 rounded-2xl border border-slate-800 text-slate-100 overflow-hidden relative">
      {/* Background Animated Floating Grid Aura */}
      <div className="absolute inset-0 bg-[radial-gradient(#0284c7_1px,transparent_1px)] [background-size:20px_20px] opacity-10 pointer-events-none" />

      {/* Header Bar with Live Circuit Gauges */}
      <div className="w-full flex items-center justify-between pb-3 border-b border-slate-800/80 z-10">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400 animate-pulse">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-base text-slate-100 flex items-center gap-2">
              <span>{visualPayload?.title || "Ohm's Law Live Interactive Stage"}</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-brand-500/20 text-brand-300 border border-brand-500/40">
                60 FPS Simulation
              </span>
            </h3>
            <p className="text-xs text-slate-400">Dynamic physics model & charge flow visualization</p>
          </div>
        </div>

        {/* Live Gauges */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono">
            <span className="text-sky-400 font-bold">V:</span> {voltage}V
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono">
            <span className="text-rose-400 font-bold">R:</span> {resistance}Ω
          </div>
          <div className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-xs font-mono text-emerald-300 font-bold shadow-lg shadow-emerald-500/10">
            <Activity className="w-3.5 h-3.5 animate-pulse text-emerald-400" />
            <span>I = {current} A</span>
          </div>
        </div>
      </div>

      {/* Main Dynamic Stage Selector */}
      {vType === 'water_analogy' ? (
        <div className="w-full my-auto py-2 z-10 space-y-4">
          <div className="w-full flex justify-center">
            <canvas ref={fluidCanvasRef} width={520} height={120} className="rounded-2xl border border-sky-500/30 shadow-2xl bg-slate-900/80 max-w-full" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="glass-card p-3 rounded-xl border border-sky-500/30 text-center">
              <h4 className="font-bold text-sky-300 text-xs">Water Pump = Voltage (V)</h4>
              <p className="text-[11px] text-slate-300 mt-1">Drives pressure that pushes charges forward.</p>
            </div>
            <div className="glass-card p-3 rounded-xl border border-emerald-500/30 text-center">
              <h4 className="font-bold text-emerald-300 text-xs">Water Flow = Current (I)</h4>
              <p className="text-[11px] text-slate-300 mt-1">Volume of charge passing per second.</p>
            </div>
            <div className="glass-card p-3 rounded-xl border border-rose-500/30 text-center">
              <h4 className="font-bold text-rose-300 text-xs">Pipe Narrowing = Resistance (R)</h4>
              <p className="text-[11px] text-slate-300 mt-1">Restricts flow rate and causes friction.</p>
            </div>
          </div>
        </div>
      ) : vType === 'math_formula_interactive' ? (
        <div className="w-full flex flex-col items-center justify-center my-auto p-6 glass-card rounded-2xl border border-brand-500/30 z-10 space-y-6">
          <div className="text-4xl md:text-6xl font-extrabold tracking-wider font-mono text-center text-white drop-shadow-2xl">
            <span className="text-sky-400 px-3 py-1 rounded-xl bg-sky-500/15 border border-sky-500/40 inline-block animate-pulse">V</span>
            <span className="text-slate-400 mx-3">=</span>
            <span className="text-emerald-400 px-3 py-1 rounded-xl bg-emerald-500/15 border border-emerald-500/40 inline-block">I</span>
            <span className="text-slate-400 mx-3">×</span>
            <span className="text-rose-400 px-3 py-1 rounded-xl bg-rose-500/15 border border-rose-500/40 inline-block">R</span>
          </div>

          <div className="grid grid-cols-3 gap-4 w-full text-center">
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-sky-500/30">
              <div className="text-xs text-sky-400 font-bold uppercase">Voltage (V)</div>
              <div className="text-sm font-extrabold text-slate-100 mt-0.5">{voltage} Volts</div>
              <div className="text-[11px] text-slate-400">Potential Difference</div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/30">
              <div className="text-xs text-emerald-400 font-bold uppercase">Current (I)</div>
              <div className="text-sm font-extrabold text-emerald-300 mt-0.5">{current} Amperes</div>
              <div className="text-[11px] text-slate-400">I = V / R</div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-rose-500/30">
              <div className="text-xs text-rose-400 font-bold uppercase">Resistance (R)</div>
              <div className="text-sm font-extrabold text-rose-300 mt-0.5">{resistance} Ohms (Ω)</div>
              <div className="text-[11px] text-slate-400">Opposition to Flow</div>
            </div>
          </div>
        </div>
      ) : vType === 'worked_example' ? (
        <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-4 my-auto p-4 glass-card rounded-2xl border border-slate-800 z-10">
          <div className="space-y-3">
            <div className="text-xs font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-4 h-4" />
              <span>Step-by-Step Calculation</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/95 border border-slate-800 font-mono text-xs space-y-2">
              <div className="text-slate-400">Given: Voltage V = 12V, Resistance R = 4Ω</div>
              <div className="text-sky-300 font-bold">1. Apply Formula: I = V / R</div>
              <div className="text-slate-200">2. Substitute Values: I = 12 / 4</div>
              <div className="p-2.5 rounded-lg bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 font-extrabold text-sm">
                3. Calculated Current: I = 3.00 Amperes (A)
              </div>
            </div>
          </div>

          <div className="flex flex-col items-center justify-center space-y-2">
            <canvas ref={oscilloCanvasRef} width={260} height={140} className="w-full rounded-xl bg-slate-900 border border-slate-800 shadow-inner" />
            <span className="text-[10px] text-slate-400 font-mono">Live Current Oscilloscope Waveform</span>
          </div>
        </div>
      ) : vType === 'circuit_remediation' ? (
        <div className="w-full my-auto p-4 rounded-2xl glass-card border border-amber-500/40 space-y-3 z-10">
          <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
            <AlertCircle className="w-5 h-5 animate-pulse" />
            <span>Misconception Visualized: Bottleneck Effect</span>
          </div>
          <div className="grid grid-cols-2 gap-4 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/30">
              <div className="font-bold text-slate-100">Standard Resistor (R = 4Ω)</div>
              <div className="text-slate-400 mt-1">V = 12V ÷ 4Ω</div>
              <div className="text-emerald-400 font-extrabold text-sm mt-1">Current = 3.0 A (Wide Flow)</div>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900/90 border border-rose-500/30">
              <div className="font-bold text-slate-100">Higher Resistor (R = 8Ω)</div>
              <div className="text-slate-400 mt-1">V = 12V ÷ 8Ω (Narrow Bottleneck)</div>
              <div className="text-rose-400 font-extrabold text-sm mt-1">Current = 1.5 A (Restricted)</div>
            </div>
          </div>
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs text-amber-200 text-center font-semibold">
            Increasing the denominator (Resistance) ALWAYS reduces the resulting Current!
          </div>
        </div>
      ) : (
        <div className="relative w-full h-56 flex items-center justify-center my-auto z-10">
          <canvas ref={circuitCanvasRef} width={500} height={210} className="w-full max-w-xl h-full rounded-2xl bg-slate-900/80 border border-slate-800 shadow-2xl" />
        </div>
      )}

      {/* Interactive Controls Bar for Live Experimentation */}
      <div className="w-full grid grid-cols-2 gap-4 pt-3 border-t border-slate-800/80 text-xs z-10">
        <div>
          <div className="flex justify-between text-slate-200 font-semibold mb-1">
            <span>Voltage Push (V):</span>
            <span className="font-mono text-sky-400">{voltage} V</span>
          </div>
          <input
            type="range"
            min="2"
            max="24"
            step="1"
            value={voltage}
            onChange={(e) => setVoltage(Number(e.target.value))}
            className="w-full accent-sky-400 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
        </div>
        <div>
          <div className="flex justify-between text-slate-200 font-semibold mb-1">
            <span>Resistance Brake (R):</span>
            <span className="font-mono text-rose-400">{resistance} Ω</span>
          </div>
          <input
            type="range"
            min="1"
            max="12"
            step="1"
            value={resistance}
            onChange={(e) => setResistance(Number(e.target.value))}
            className="w-full accent-rose-400 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
        </div>
      </div>
    </div>
  );
}
