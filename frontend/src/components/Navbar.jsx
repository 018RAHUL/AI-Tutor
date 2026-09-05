import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles,
  Compass,
  PlusCircle,
  Activity,
  Brain,
  User,
  ShieldCheck,
  BookOpen,
  LogOut,
  LogIn,
  Settings,
  Target,
  Award,
  ChevronDown,
  Menu,
  X
} from 'lucide-react';

export default function Navbar({
  activeTab,
  setActiveTab,
  onOpenObservability,
  currentUser,
  onOpenAuthModal,
  onLogout
}) {
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const dropdownRef = useRef(null);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Compass },
    { id: 'create', label: 'Create Lesson', icon: PlusCircle },
    { id: 'classroom', label: 'AI Classroom', icon: Brain },
    { id: 'summary', label: 'Study Notes & Summary', icon: BookOpen },
    { id: 'learning_path', label: 'Learning Path', icon: Activity },
  ];

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setProfileDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getAvatarBadge = (avatarId) => {
    const map = {
      avatar_1: { icon: '🧑‍🔬', bg: 'from-sky-500 to-blue-600' },
      avatar_2: { icon: '⚡', bg: 'from-amber-500 to-orange-600' },
      avatar_3: { icon: '👩‍💻', bg: 'from-emerald-500 to-teal-600' },
      avatar_4: { icon: '📐', bg: 'from-purple-500 to-indigo-600' },
      avatar_5: { icon: '🚀', bg: 'from-pink-500 to-rose-600' },
      avatar_6: { icon: '🧠', bg: 'from-cyan-500 to-blue-700' }
    };
    return map[avatarId] || map.avatar_1;
  };

  const avMeta = getAvatarBadge(currentUser?.avatar_url || 'avatar_1');
  const gradeLevel = currentUser?.profile?.grade_level || 'Beginner';
  const learningStyle = currentUser?.profile?.learning_style || 'Visual';

  return (
    <>
      <header className="sticky top-0 z-40 w-full glass-panel border-b border-white/10 px-3 sm:px-6 lg:px-8 py-2.5 sm:py-3 flex items-center justify-between">
        {/* Brand Logo */}
        <div 
          onClick={() => { setActiveTab('dashboard'); setMobileMenuOpen(false); }}
          className="flex items-center gap-2.5 sm:gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-2xl bg-gradient-to-tr from-brand-600 via-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-all">
            <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-1.5 sm:gap-2">
              <span className="font-bold text-base sm:text-lg tracking-tight text-white font-sans">
                AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-brand-400 to-indigo-300">Teacher</span>
              </span>
              <span className="px-1.5 py-0.2 rounded text-[9px] sm:text-[10px] font-semibold bg-brand-500/20 border border-brand-500/40 text-brand-300">
                v2.0 Pro
              </span>
            </div>
            <p className="hidden sm:block text-[10px] sm:text-[11px] text-slate-400 font-medium">Multi-Agent Visual Educational Tutor</p>
          </div>
        </div>

        {/* Desktop & Tablet Navigation Links */}
        <nav className="hidden lg:flex items-center gap-1 p-1 rounded-2xl bg-slate-900/80 border border-white/10 shadow-inner">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-brand-500 to-sky-600 text-white shadow-md shadow-brand-500/25'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Controls */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* LangGraph Observability Trigger */}
          <button
            onClick={onOpenObservability}
            className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl text-[11px] sm:text-xs font-medium text-amber-300 bg-amber-500/10 border border-amber-500/25 hover:bg-amber-500/20 transition-all shadow-sm"
            title="Inspect Agent Trajectory & State Graph"
          >
            <Activity className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
            <span className="hidden md:inline">LangGraph Trace</span>
          </button>

          {/* User Profile & Auth Trigger */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
              className="flex items-center gap-2 p-1.5 pl-2 sm:pl-2.5 rounded-2xl glass-card hover:bg-white/10 border border-white/10 transition-all group"
            >
              <div className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-br ${avMeta.bg} flex items-center justify-center text-xs sm:text-sm shadow-md`}>
                {avMeta.icon}
              </div>

              <div className="hidden xl:block text-left pr-1">
                <div className="text-xs font-bold text-slate-100 leading-tight group-hover:text-sky-300 transition-colors truncate max-w-[110px]">
                  {currentUser?.full_name || currentUser?.username || 'Student Scholar'}
                </div>
                <div className="text-[10px] text-emerald-400 font-medium flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> {gradeLevel}
                </div>
              </div>

              <ChevronDown className="w-3.5 h-3.5 text-slate-400 group-hover:text-white transition-transform" />
            </button>

            {/* Profile Dropdown Menu */}
            {profileDropdownOpen && (
              <div className="absolute right-0 mt-2 w-64 sm:w-72 rounded-3xl bg-slate-900/95 backdrop-blur-2xl border border-white/10 shadow-2xl p-4 space-y-3 animate-fadeIn z-50">
                {/* Profile Card Header */}
                <div className="flex items-center gap-3 p-2 rounded-2xl bg-slate-950/60 border border-white/5">
                  <div className={`w-10 h-10 rounded-2xl bg-gradient-to-br ${avMeta.bg} flex items-center justify-center text-lg shadow-inner shrink-0`}>
                    {avMeta.icon}
                  </div>
                  <div className="space-y-0.5 truncate">
                    <div className="text-xs font-bold text-white truncate">
                      {currentUser?.full_name || currentUser?.username || 'Student Scholar'}
                    </div>
                    <div className="text-[11px] text-slate-400 truncate">
                      {currentUser?.email || `@${currentUser?.username || 'student'}`}
                    </div>
                  </div>
                </div>

                {/* Learning Stats */}
                <div className="grid grid-cols-2 gap-2 text-center">
                  <div className="p-2.5 rounded-xl bg-slate-950/40 border border-white/5 space-y-0.5">
                    <div className="text-xs font-extrabold text-sky-400">
                      {currentUser?.profile?.total_lessons_completed ?? 0}
                    </div>
                    <div className="text-[10px] text-slate-400">Lessons Finished</div>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-950/40 border border-white/5 space-y-0.5">
                    <div className="text-xs font-extrabold text-emerald-400">
                      {gradeLevel}
                    </div>
                    <div className="text-[10px] text-slate-400">Current Level</div>
                  </div>
                </div>

                {/* Goal Snapshot */}
                {currentUser?.profile?.learning_goal && (
                  <div className="p-2.5 rounded-xl bg-brand-500/10 border border-brand-500/20 text-[11px] text-brand-200 flex items-center gap-2">
                    <Target className="w-4 h-4 text-brand-400 shrink-0" />
                    <span className="truncate">{currentUser.profile.learning_goal}</span>
                  </div>
                )}

                {/* Actions */}
                <div className="pt-2 border-t border-white/5 space-y-1">
                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      onOpenAuthModal('login');
                    }}
                    className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
                  >
                    <User className="w-4 h-4 text-sky-400" />
                    <span>{currentUser ? 'Account' : 'Sign In / Register'}</span>
                  </button>

                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      onOpenAuthModal('register');
                    }}
                    className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
                  >
                    <Settings className="w-4 h-4 text-brand-400" />
                    <span>Edit Learning Profile</span>
                  </button>

                  {onLogout && (
                    <button
                      onClick={() => {
                        setProfileDropdownOpen(false);
                        onLogout();
                      }}
                      className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-rose-300 hover:text-rose-200 hover:bg-rose-500/10 transition-colors"
                    >
                      <LogOut className="w-4 h-4 text-rose-400" />
                      <span>Sign Out</span>
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Mobile Hamburger Toggle */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-2xl glass-card text-slate-300 hover:text-white hover:bg-white/10 transition"
            title="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Mobile Slide-down Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden z-30 fixed top-[56px] left-0 right-0 p-4 bg-slate-950/95 backdrop-blur-2xl border-b border-white/10 shadow-2xl space-y-2 animate-fadeIn">
          <div className="grid grid-cols-1 gap-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-brand-500 to-sky-600 text-white shadow-md'
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <Icon className="w-4 h-4 text-sky-400" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenAuthModal('login');
              }}
              className="px-4 py-2 rounded-xl bg-brand-500/20 text-brand-300 text-xs font-semibold border border-brand-500/40"
            >
              Sign In / Register
            </button>

            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenObservability();
              }}
              className="px-4 py-2 rounded-xl bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/40 flex items-center gap-1.5"
            >
              <Activity className="w-3.5 h-3.5" />
              <span>Trace Graph</span>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
