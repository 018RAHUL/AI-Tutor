import React, { useState, useEffect } from 'react';
import { Sparkles, Radio } from 'lucide-react';

export default function TeacherAvatar({
  avatarState = 'SPEAKING',
  isPlaying = true,
  name = 'Prof. Maya (AI Tutor)'
}) {
  const [blink, setBlink] = useState(false);
  const [mouthPhase, setMouthPhase] = useState(0); // 0: gentle smile, 1: open vocalizing, 2: round 'O', 3: wide smile
  const [headTilt, setHeadTilt] = useState(0);
  const [headBob, setHeadBob] = useState(0);
  const [audioBars, setAudioBars] = useState([40, 70, 30, 85, 55]);

  // Periodic natural blinking
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setBlink(true);
      setTimeout(() => setBlink(false), 140);
    }, 3200);
    return () => clearInterval(blinkInterval);
  }, []);

  // Smooth speaking animation, lip sync, breathing
  useEffect(() => {
    let animId;
    let tick = 0;
    const isTalking = isPlaying && ['SPEAKING', 'EXPLAINING', 'RE_EXPLAINING', 'CORRECT', 'QUESTIONING'].includes(avatarState);

    const updateAnim = () => {
      tick++;

      if (isTalking) {
        // Natural phoneme sequence
        const cycle = [1, 2, 3, 1, 0, 3, 2, 1, 0];
        const idx = Math.floor(tick / 5) % cycle.length;
        setMouthPhase(cycle[idx]);

        // Natural rhythmic gestures
        setHeadBob(Math.sin(tick * 0.08) * 2.5);
        setHeadTilt(Math.sin(tick * 0.05) * 2);

        // Sound spectrum equalizer simulation
        setAudioBars([
          20 + Math.abs(Math.sin(tick * 0.18)) * 80,
          30 + Math.abs(Math.cos(tick * 0.22)) * 70,
          15 + Math.abs(Math.sin(tick * 0.15)) * 85,
          40 + Math.abs(Math.cos(tick * 0.28)) * 60,
          25 + Math.abs(Math.sin(tick * 0.20)) * 75,
        ]);
      } else {
        // Idle state: gentle breathing
        setMouthPhase(avatarState === 'CORRECT' ? 3 : 0);
        setHeadBob(Math.sin(tick * 0.04) * 0.8);
        setHeadTilt(avatarState === 'THINKING' ? -3 : 0);
        setAudioBars([8, 12, 8, 10, 8]);
      }

      animId = requestAnimationFrame(updateAnim);
    };

    animId = requestAnimationFrame(updateAnim);
    return () => cancelAnimationFrame(animId);
  }, [isPlaying, avatarState]);

  // Expression Badge Config
  const stateBadgeMap = {
    IDLE: { label: 'Ready', color: 'bg-slate-700 text-slate-300 border-slate-600', aura: 'bg-slate-600' },
    SPEAKING: { label: 'Explaining Live', color: 'bg-sky-500/20 text-sky-300 border-sky-500/40', aura: 'bg-sky-500' },
    EXPLAINING: { label: 'Demonstrating', color: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/40', aura: 'bg-indigo-500' },
    QUESTIONING: { label: 'Interactive Checkpoint', color: 'bg-amber-500/20 text-amber-300 border-amber-500/40', aura: 'bg-amber-500' },
    LISTENING: { label: 'Listening...', color: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40', aura: 'bg-emerald-500' },
    THINKING: { label: 'Evaluating Concept', color: 'bg-purple-500/20 text-purple-300 border-purple-500/40', aura: 'bg-purple-500' },
    CORRECT: { label: 'Brilliant & Correct!', color: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50', aura: 'bg-emerald-400' },
    MISCONCEPTION: { label: 'Misconception Detected', color: 'bg-rose-500/20 text-rose-300 border-rose-500/50', aura: 'bg-rose-500' },
    RE_EXPLAINING: { label: 'Adaptive Re-Teaching', color: 'bg-amber-500/20 text-amber-300 border-amber-500/50', aura: 'bg-amber-500' },
  };

  const badge = stateBadgeMap[avatarState] || stateBadgeMap.SPEAKING;

  return (
    <div className="relative flex flex-col items-center justify-center p-3.5 rounded-3xl glass-card border border-white/20 shadow-2xl overflow-hidden backdrop-blur-2xl group transition-all">
      {/* Background Glowing Aura Ring */}
      <div className={`absolute -inset-2 rounded-3xl blur-2xl opacity-40 transition-all duration-700 ${badge.aura}`} />

      {/* Main Beautiful AI Teacher Vector Canvas */}
      <div 
        className="relative w-48 h-52 sm:w-52 sm:h-56 flex items-center justify-center transition-transform duration-200"
        style={{ transform: `translateY(${headBob}px) rotate(${headTilt * 0.3}deg)` }}
      >
        <svg viewBox="0 0 220 240" className="w-full h-full drop-shadow-2xl">
          <defs>
            {/* Luminous Natural Skin Gradient */}
            <linearGradient id="skinGlow" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#fff1e6" />
              <stop offset="45%" stopColor="#fed7c3" />
              <stop offset="100%" stopColor="#f7ba9e" />
            </linearGradient>

            {/* Luxurious Brunette Hair Gradient */}
            <linearGradient id="hairLux" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3d2314" />
              <stop offset="50%" stopColor="#24140b" />
              <stop offset="100%" stopColor="#140a05" />
            </linearGradient>

            {/* Hair Highlights */}
            <linearGradient id="hairSheen" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#5c3822" stopOpacity="0" />
              <stop offset="50%" stopColor="#8c5838" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#5c3822" stopOpacity="0" />
            </linearGradient>

            {/* Smart Professor Navy Blazer */}
            <linearGradient id="smartBlazer" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#1e293b" />
              <stop offset="60%" stopColor="#0f172a" />
              <stop offset="100%" stopColor="#090d16" />
            </linearGradient>

            {/* Electric Cyan Blouse */}
            <linearGradient id="electricTop" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="100%" stopColor="#0284c7" />
            </linearGradient>

            {/* Laser Stylus Glow */}
            <filter id="stylusGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* 1. LAYER: BACK HAIR (Flowing naturally behind the shoulders) */}
          <path
            d="M 52 90 C 44 40, 176 40, 168 90 C 172 135, 178 185, 164 195 C 150 175, 136 170, 110 170 C 84 170, 70 175, 56 195 C 42 185, 48 135, 52 90 Z"
            fill="url(#hairLux)"
          />

          {/* 2. LAYER: SHOULDERS & SMART BLAZER */}
          <path
            d="M 24 200 C 60 176, 160 176, 196 200 L 210 240 L 10 240 Z"
            fill="url(#smartBlazer)"
            stroke="#334155"
            strokeWidth="2"
          />

          {/* Inner Blouse Collar V-Shape */}
          <polygon points="86,188 110,228 134,188" fill="url(#electricTop)" />
          <polygon points="110,228 104,240 116,240" fill="#ffffff" />
          
          {/* Blazer Lapels */}
          <path d="M 64 186 L 96 230 L 78 240 L 36 210 Z" fill="#1e293b" opacity="0.6" />
          <path d="M 156 186 L 124 230 L 142 240 L 184 210 Z" fill="#1e293b" opacity="0.6" />

          {/* 3. LAYER: SLENDER NECK */}
          <path d="M 94 140 L 126 140 L 122 192 L 98 192 Z" fill="url(#skinGlow)" />
          <ellipse cx="110" cy="188" rx="14" ry="4" fill="#e08a65" opacity="0.3" />

          {/* 4. LAYER: BEAUTIFUL OVAL FACE (Clean contour, never covered by back hair!) */}
          <path
            d="M 66 100 C 66 65, 154 65, 154 100 C 154 138, 136 166, 110 166 C 84 166, 66 138, 66 100 Z"
            fill="url(#skinGlow)"
          />

          {/* Soft Rose Cheek Blush */}
          <ellipse cx="80" cy="124" rx="10" ry="5.5" fill="#f472b6" opacity="0.35" />
          <ellipse cx="140" cy="124" rx="10" ry="5.5" fill="#f472b6" opacity="0.35" />

          {/* 5. LAYER: STYLISH FRONT HAIR & BANGS (Side swept, frames the face elegantly) */}
          <path
            d="M 66 85 C 66 45, 154 45, 154 85 C 154 95, 150 110, 146 122 C 142 100, 134 78, 110 78 C 86 78, 78 100, 74 122 C 70 110, 66 95, 66 85 Z"
            fill="url(#hairLux)"
          />
          {/* Hair Sheen Highlight Band */}
          <path
            d="M 72 65 Q 110 52 148 65 Q 110 58 72 65"
            fill="url(#hairSheen)"
          />

          {/* 6. LAYER: EXPRESSIVE EYEBROWS */}
          {avatarState === 'QUESTIONING' ? (
            <>
              <path d="M 80 88 Q 92 78 102 86" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
              <path d="M 118 86 Q 128 78 140 88" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
            </>
          ) : avatarState === 'THINKING' ? (
            <>
              <path d="M 80 84 Q 92 86 102 88" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
              <path d="M 118 88 Q 128 86 140 84" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
            </>
          ) : (
            <>
              <path d="M 80 86 Q 92 80 102 86" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
              <path d="M 118 86 Q 128 80 140 86" fill="none" stroke="#26140b" strokeWidth="2.8" strokeLinecap="round" />
            </>
          )}

          {/* 7. LAYER: LIVELY EXPRESSIVE EYES */}
          {blink ? (
            <>
              {/* Natural Closed Eyelid Curves */}
              <path d="M 80 106 Q 91 114 102 106" fill="none" stroke="#26140b" strokeWidth="3" strokeLinecap="round" />
              <path d="M 118 106 Q 129 114 140 106" fill="none" stroke="#26140b" strokeWidth="3" strokeLinecap="round" />
            </>
          ) : (
            <>
              {/* Left Eye */}
              <ellipse cx="91" cy="105" rx="11" ry="9" fill="#ffffff" stroke="#26140b" strokeWidth="1.5" />
              {/* Iris (Warm Hazel / Chocolate Brown) */}
              <ellipse cx="92" cy="105" rx="6.5" ry="7.5" fill="#3b2014" />
              <ellipse cx="92" cy="105" rx="4" ry="5" fill="#0f0703" />
              {/* Specular Light Reflection Dots */}
              <circle cx="94" cy="102" r="2.2" fill="#ffffff" />
              <circle cx="89" cy="107" r="1.2" fill="#ffffff" opacity="0.8" />
              {/* Eyelash line */}
              <path d="M 79 104 Q 91 97 103 104" fill="none" stroke="#1a0d07" strokeWidth="2.5" strokeLinecap="round" />

              {/* Right Eye */}
              <ellipse cx="129" cy="105" rx="11" ry="9" fill="#ffffff" stroke="#26140b" strokeWidth="1.5" />
              {/* Iris */}
              <ellipse cx="130" cy="105" rx="6.5" ry="7.5" fill="#3b2014" />
              <ellipse cx="130" cy="105" rx="4" ry="5" fill="#0f0703" />
              {/* Specular Light Reflection Dots */}
              <circle cx="132" cy="102" r="2.2" fill="#ffffff" />
              <circle cx="127" cy="107" r="1.2" fill="#ffffff" opacity="0.8" />
              {/* Eyelash line */}
              <path d="M 117 104 Q 129 97 141 104" fill="none" stroke="#1a0d07" strokeWidth="2.5" strokeLinecap="round" />
            </>
          )}

          {/* 8. LAYER: MODERN STYLISH GLASSES */}
          {/* Left Lens Frame */}
          <rect x="76" y="93" width="30" height="24" rx="7" fill="rgba(56, 189, 248, 0.08)" stroke="#38bdf8" strokeWidth="2" />
          {/* Right Lens Frame */}
          <rect x="114" y="93" width="30" height="24" rx="7" fill="rgba(56, 189, 248, 0.08)" stroke="#38bdf8" strokeWidth="2" />
          {/* Bridge */}
          <path d="M 106 102 Q 110 98 114 102" fill="none" stroke="#38bdf8" strokeWidth="2" />
          {/* Temples */}
          <path d="M 76 100 L 68 98" fill="none" stroke="#38bdf8" strokeWidth="2" />
          <path d="M 144 100 L 152 98" fill="none" stroke="#38bdf8" strokeWidth="2" />
          {/* Lens Specular Glint */}
          <line x1="80" y1="96" x2="88" y2="104" stroke="#ffffff" strokeWidth="1.2" opacity="0.6" strokeLinecap="round" />
          <line x1="118" y1="96" x2="126" y2="104" stroke="#ffffff" strokeWidth="1.2" opacity="0.6" strokeLinecap="round" />

          {/* 9. LAYER: CUTE DELICATE NOSE */}
          <path d="M 110 115 Q 112 124 107 127 Q 111 128 114 127" fill="none" stroke="#d9774d" strokeWidth="1.8" strokeLinecap="round" />

          {/* 10. LAYER: ARTICULATED LIP-SYNC MOUTH */}
          {mouthPhase === 0 && (
            /* Gentle Confident Smile */
            <path d="M 98 142 Q 110 149 122 142" fill="none" stroke="#e11d48" strokeWidth="2.8" strokeLinecap="round" />
          )}

          {mouthPhase === 1 && (
            /* Open Speaking (A/Ah) with subtle teeth & pink interior */
            <g>
              <ellipse cx="110" cy="144" rx="9" ry="6.5" fill="#881337" stroke="#e11d48" strokeWidth="2" />
              <rect x="104" y="139" width="12" height="3" rx="1.5" fill="#ffffff" />
              <ellipse cx="110" cy="147" rx="5" ry="2.5" fill="#f43f5e" />
            </g>
          )}

          {mouthPhase === 2 && (
            /* Round O Speaking (Oh/Oo) */
            <g>
              <ellipse cx="110" cy="144" rx="6.5" ry="7.5" fill="#881337" stroke="#e11d48" strokeWidth="2" />
              <ellipse cx="110" cy="147" rx="3.5" ry="2.5" fill="#f43f5e" />
            </g>
          )}

          {mouthPhase === 3 && (
            /* Wide Joyful / Explaining Smile with teeth */
            <g>
              <path d="M 96 141 Q 110 153 124 141 Z" fill="#881337" stroke="#e11d48" strokeWidth="2" />
              <path d="M 99 142 Q 110 146 121 142 Z" fill="#ffffff" />
            </g>
          )}

          {/* 11. LAYER: HIGH-TECH LASER STYLUS POINTER */}
          {['EXPLAINING', 'SPEAKING', 'RE_EXPLAINING'].includes(avatarState) && (
            <g className="animate-pulse">
              <line x1="168" y1="172" x2="202" y2="136" stroke="#0ea5e9" strokeWidth="3.5" strokeLinecap="round" />
              <circle cx="202" cy="136" r="4.5" fill="#38bdf8" filter="url(#stylusGlow)" />
              <circle cx="202" cy="136" r="2" fill="#ffffff" />
            </g>
          )}
        </svg>
      </div>

      {/* Professor Identity & Sub-label */}
      <div className="mt-1 text-center">
        <h4 className="text-xs sm:text-sm font-bold text-white tracking-wide flex items-center justify-center gap-1.5">
          <span>{name}</span>
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
        </h4>

        {/* Audio Spectrum Equalizer */}
        <div className="flex items-center justify-center gap-1 mt-1.5 h-3.5">
          {audioBars.map((h, i) => (
            <span
              key={i}
              className={`w-1 rounded-full transition-all duration-100 ${
                isPlaying ? 'bg-gradient-to-t from-sky-500 to-cyan-300' : 'bg-slate-700'
              }`}
              style={{ height: `${h}%` }}
            />
          ))}
        </div>
      </div>

      {/* Dynamic Expression Status Pill */}
      <div className="mt-2 flex items-center justify-center">
        <div className={`px-3 py-1 rounded-full text-[10px] font-semibold border flex items-center gap-1.5 shadow-md ${badge.color}`}>
          <span className={`w-1.5 h-1.5 rounded-full animate-ping ${badge.aura}`} />
          <span>{badge.label}</span>
        </div>
      </div>
    </div>
  );
}
