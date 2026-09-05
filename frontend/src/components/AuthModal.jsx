import React, { useState } from 'react';
import { apiFetch } from '../api';
import {
  X,
  User,
  Mail,
  Lock,
  Sparkles,
  BookOpen,
  Compass,
  Check,
  AlertCircle,
  Eye,
  EyeOff,
  GraduationCap,
  Target
} from 'lucide-react';

const AVATARS = [
  { id: 'avatar_1', name: 'Alex', icon: '🧑‍🔬', label: 'Scholar', bg: 'from-sky-500 to-blue-600' },
  { id: 'avatar_2', name: 'Elena', icon: '⚡', label: 'Physicist', bg: 'from-amber-500 to-orange-600' },
  { id: 'avatar_3', name: 'Kai', icon: '👩‍💻', label: 'Engineer', bg: 'from-emerald-500 to-teal-600' },
  { id: 'avatar_4', name: 'Maya', icon: '📐', label: 'Mathematician', bg: 'from-purple-500 to-indigo-600' },
  { id: 'avatar_5', name: 'Liam', icon: '🚀', label: 'Explorer', bg: 'from-pink-500 to-rose-600' },
  { id: 'avatar_6', name: 'Aria', icon: '🧠', label: 'Thinker', bg: 'from-cyan-500 to-blue-700' }
];

const GRADE_LEVELS = ['Beginner', 'Intermediate', 'Advanced'];
const LEARNING_STYLES = [
  { id: 'Visual', label: 'Visual & Interactive', desc: 'Simulations, circuits, diagrams & animations' },
  { id: 'Practical', label: 'Practical & Applied', desc: 'Real-world problem solving & worked examples' },
  { id: 'Simple', label: 'Simple & Intuitive', desc: 'Analogies, plain language & fundamentals' },
  { id: 'Technical', label: 'Rigorous & Formal', desc: 'Mathematical proofs, formulas & deep derivations' },
  { id: 'Socratic', label: 'Socratic Dialogue', desc: 'Guided inquiry, questions & reflective hints' }
];

export default function AuthModal({ isOpen, onClose, onAuthSuccess, initialMode = 'login' }) {
  const [mode, setMode] = useState(initialMode); // 'login' or 'register'
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  
  // Registration specific fields
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [selectedAvatar, setSelectedAvatar] = useState('avatar_1');
  const [gradeLevel, setGradeLevel] = useState('Beginner');
  const [learningStyle, setLearningStyle] = useState('Visual');
  const [learningGoal, setLearningGoal] = useState('Master core STEM concepts');
  
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  React.useEffect(() => {
    setMode(initialMode);
    setErrorMsg('');
  }, [initialMode, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    try {
      if (mode === 'login') {
        if (!usernameOrEmail.trim()) {
          throw new Error('Please enter your username or email address.');
        }

        const res = await apiFetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username_or_email: usernameOrEmail.trim(),
            password: password || undefined
          })
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || 'Login failed. Please verify credentials.');
        }

        localStorage.setItem('ai_teacher_token', data.token);
        localStorage.setItem('ai_teacher_user', JSON.stringify(data.user));
        onAuthSuccess(data.user);
        onClose();
      } else {
        // Register flow
        if (!username.trim()) {
          throw new Error('Please enter a unique username.');
        }

        const res = await apiFetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username.trim(),
            email: email.trim() || undefined,
            password: password || undefined,
            full_name: fullName.trim() || username.trim(),
            grade_level: gradeLevel,
            learning_style: learningStyle,
            learning_goal: learningGoal,
            avatar_url: selectedAvatar
          })
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || 'Registration failed. Please try a different username.');
        }

        localStorage.setItem('ai_teacher_token', data.token);
        localStorage.setItem('ai_teacher_user', JSON.stringify(data.user));
        onAuthSuccess(data.user);
        onClose();
      }
    } catch (err) {
      setErrorMsg(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-lg overflow-hidden rounded-3xl bg-slate-900/95 border border-white/10 shadow-2xl shadow-brand-500/20 max-h-[90vh] flex flex-col">
        {/* Glow accent */}
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-brand-500/20 blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 rounded-full bg-indigo-500/20 blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="relative z-10 flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-gradient-to-tr from-brand-500 to-sky-500 text-white shadow-lg shadow-brand-500/30">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight">
                {mode === 'login' ? 'Welcome Back!' : 'Create Student Profile'}
              </h2>
              <p className="text-xs text-slate-400">
                {mode === 'login'
                  ? 'Sign in to access your saved lessons, scores & summaries'
                  : 'Personalize your visual AI learning journey'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switch */}
        <div className="relative z-10 p-2 mx-6 mt-4 bg-slate-950/60 rounded-2xl border border-white/5 flex gap-1">
          <button
            type="button"
            onClick={() => { setMode('login'); setErrorMsg(''); }}
            className={`flex-1 py-2 text-xs font-semibold rounded-xl transition-all ${
              mode === 'login'
                ? 'bg-brand-500 text-white shadow-md shadow-brand-500/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => { setMode('register'); setErrorMsg(''); }}
            className={`flex-1 py-2 text-xs font-semibold rounded-xl transition-all ${
              mode === 'register'
                ? 'bg-brand-500 text-white shadow-md shadow-brand-500/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            New Student Profile
          </button>
        </div>

        {/* Form Body */}
        <div className="relative z-10 p-6 overflow-y-auto flex-1 space-y-4">
          {errorMsg && (
            <div className="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2.5">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === 'login' ? (
              <>
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-300">Username or Email</label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={usernameOrEmail}
                      onChange={(e) => setUsernameOrEmail(e.target.value)}
                      placeholder="e.g. alex_learner or student@domain.com"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-300">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter password (optional for demo)"
                      className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3 text-slate-400 hover:text-white"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                {/* Avatar Selection */}
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-slate-300">Choose Student Avatar</label>
                  <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                    {AVATARS.map((av) => (
                      <button
                        key={av.id}
                        type="button"
                        onClick={() => setSelectedAvatar(av.id)}
                        className={`p-2 rounded-2xl flex flex-col items-center gap-1 border transition-all ${
                          selectedAvatar === av.id
                            ? 'border-brand-400 bg-brand-500/20 shadow-md shadow-brand-500/20 scale-105'
                            : 'border-white/5 bg-slate-950/40 hover:border-white/20'
                        }`}
                      >
                        <div className={`w-8 h-8 rounded-full bg-gradient-to-br ${av.bg} flex items-center justify-center text-sm shadow-inner`}>
                          {av.icon}
                        </div>
                        <span className="text-[10px] font-medium text-slate-300 truncate w-full text-center">
                          {av.label}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300">Full Name</label>
                    <input
                      type="text"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="e.g. Alex Rivera"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500"
                      required
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300">Username</label>
                    <input
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="e.g. alex_rivera"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-300">Email Address (Optional)</label>
                  <div className="relative">
                    <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="student@domain.com"
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-300">Password (Optional)</label>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Create password"
                      className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-3 text-slate-400 hover:text-white"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Grade Level & Learning Style */}
                <div className="grid grid-cols-2 gap-3 pt-1">
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300">Current Level</label>
                    <select
                      value={gradeLevel}
                      onChange={(e) => setGradeLevel(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white text-xs focus:outline-none focus:border-brand-500"
                    >
                      {GRADE_LEVELS.map((lvl) => (
                        <option key={lvl} value={lvl}>{lvl}</option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-300">Learning Style</label>
                    <select
                      value={learningStyle}
                      onChange={(e) => setLearningStyle(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white text-xs focus:outline-none focus:border-brand-500"
                    >
                      {LEARNING_STYLES.map((st) => (
                        <option key={st.id} value={st.id}>{st.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-300">Learning Goal</label>
                  <div className="relative">
                    <Target className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                    <input
                      type="text"
                      value={learningGoal}
                      onChange={(e) => setLearningGoal(e.target.value)}
                      placeholder="e.g. Master AP Physics, pass interview, etc."
                      className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-white/10 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-brand-500"
                    />
                  </div>
                </div>
              </>
            )}

            <div className="pt-3">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-brand-500 to-sky-600 hover:from-brand-600 hover:to-sky-700 text-white font-semibold text-xs shadow-lg shadow-brand-500/30 transition-all flex items-center justify-center gap-2"
              >
                {loading ? (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    <span>{mode === 'login' ? 'Sign In to Profile' : 'Complete Setup & Save'}</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
