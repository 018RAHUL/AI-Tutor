import React, { useState, useEffect } from 'react';
import { apiFetch } from './api';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import CreateLesson from './components/CreateLesson';
import LessonPlanning from './components/LessonPlanning';
import AIClassroom from './components/AIClassroom';
import SummaryView from './components/SummaryView';
import AssessmentView from './components/AssessmentView';
import LearningPathView from './components/LearningPathView';
import ObservabilityDrawer from './components/ObservabilityDrawer';
import LoadingScreen from './components/LoadingScreen';
import AuthModal from './components/AuthModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentLesson, setCurrentLesson] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatingTopic, setGeneratingTopic] = useState("Ohm's Law");
  const [generatingLevel, setGeneratingLevel] = useState("Beginner");
  const [observabilityOpen, setObservabilityOpen] = useState(false);
  const [observabilityLogs, setObservabilityLogs] = useState([]);
  
  // User Authentication & Profile State
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState('login');

  const handleOpenAuthModal = (mode = 'login') => {
    setAuthModalMode(mode);
    setAuthModalOpen(true);
  };
  const [currentUser, setCurrentUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);

  // Verify session on mount if token exists
  useEffect(() => {
    const token = localStorage.getItem('ai_teacher_token');
    if (token) {
      apiFetch('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => {
          if (data?.user) {
            setCurrentUser(data.user);
            localStorage.setItem('ai_teacher_user', JSON.stringify(data.user));
          }
        })
        .catch(() => {}).finally(() => setAuthChecked(true));
    } else { setAuthChecked(true); }
  }, []);

  const handleAuthSuccess = (userData) => {
    setCurrentUser(userData);
    localStorage.setItem('ai_teacher_user', JSON.stringify(userData));
  };

  const handleLogout = async () => {
    try { await apiFetch('/api/auth/logout', { method: 'POST' }); } catch {}
    localStorage.removeItem('ai_teacher_token');
    localStorage.removeItem('ai_teacher_user');
    setCurrentUser(null);
    setActiveTab('dashboard');
  };

  // Generate lesson handler
  const handleGenerateLesson = async (params) => {
    if (!localStorage.getItem('ai_teacher_token')) {
      setAuthModalMode('login');
      setAuthModalOpen(true);
      return;
    }
    setIsGenerating(true);
    setGeneratingTopic(params.topic || "Ohm's Law");
    setGeneratingLevel(params.student_level || currentUser?.profile?.grade_level || "Beginner");
    try {
      if (params.source_type === 'upload' && params.source_file) {
        const formData = new FormData();
        formData.append('file', params.source_file);
        await apiFetch('/api/rag/upload', {
          method: 'POST',
          body: formData
        });
      }

      const res = await apiFetch('/api/lesson/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: params.topic || "Agentic AI",
          student_level: params.student_level || currentUser?.profile?.grade_level || 'Beginner',
          teaching_style: params.teaching_style || currentUser?.profile?.learning_style || 'Visual',
          duration_target: params.duration_target || '20 min',
          source_type: params.source_type || 'topic',
          model_provider: params.model_provider || 'autonomous',
        })
      });

      const data = await res.json();
      setCurrentLesson(data);
      setObservabilityLogs(data.observability_logs || []);
      setActiveTab('planning');
    } catch (err) {
      console.error('Lesson creation failed:', err);
      alert(err.message || 'Unable to create the lesson. Please check that the backend is running.');
    } finally {
      setIsGenerating(false);
    }
  };

  // Launch primary benchmark demo directly
  const handleSelectTopic = (topicName, level = 'Beginner') => {
    handleGenerateLesson({
      topic: topicName,
      student_level: level,
      teaching_style: currentUser?.profile?.learning_style || 'Visual',
      duration_target: '20 min',
      source_type: 'topic'
    });
  };

  if (!authChecked) return <LoadingScreen topic="Preparing your classroom" studentLevel="Beginner" />;

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col justify-between selection:bg-brand-500 selection:text-white">
      {/* Top Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenObservability={() => setObservabilityOpen(true)}
        currentUser={currentUser}
        onOpenAuthModal={handleOpenAuthModal}
        onLogout={handleLogout}
      />

      {/* Main Content Stage */}
      <main className="flex-1">
        {isGenerating ? (
          <LoadingScreen topic={generatingTopic} studentLevel={generatingLevel} />
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <Dashboard
                onStartLesson={() => setActiveTab('create')}
                onSelectTopic={handleSelectTopic}
                currentUser={currentUser}
              />
            )}

            {activeTab === 'create' && (
              <CreateLesson
                onGenerateLesson={handleGenerateLesson}
                isLoading={isGenerating}
                currentUser={currentUser}
              />
            )}

            {activeTab === 'planning' && (
              <LessonPlanning
                lessonData={currentLesson}
                onStartPlayback={() => setActiveTab('classroom')}
              />
            )}

            {activeTab === 'classroom' && (
              <AIClassroom
                lesson={currentLesson}
                currentUser={currentUser}
                onCompleteLesson={() => setActiveTab('assessment')}
                onOpenObservability={() => setObservabilityOpen(true)}
                onOpenSummary={() => setActiveTab('summary')}
              />
            )}

            {activeTab === 'summary' && (
              <SummaryView
                lessonData={currentLesson}
                currentUser={currentUser}
                onReturnToClassroom={() => setActiveTab('classroom')}
                onGoToAssessment={() => setActiveTab('assessment')}
              />
            )}

            {activeTab === 'assessment' && (
              <AssessmentView
                assessmentData={currentLesson}
                currentUser={currentUser}
                onRestart={() => setActiveTab('classroom')}
                onExploreLearningPath={() => setActiveTab('learning_path')}
                onOpenSummary={() => setActiveTab('summary')}
              />
            )}

            {activeTab === 'learning_path' && (
              <LearningPathView
                topic={currentLesson?.topic || "Ohm's Law"}
                onSelectTopic={handleSelectTopic}
              />
            )}
          </>
        )}
      </main>

      {/* User Authentication & Profile Modal */}
      <AuthModal
        isOpen={authModalOpen}
        initialMode={authModalMode}
        onClose={() => setAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      {/* Observability & Tracing Drawer */}
      <ObservabilityDrawer
        isOpen={observabilityOpen}
        onClose={() => setObservabilityOpen(false)}
        observabilityLogs={observabilityLogs}
        lesson={currentLesson}
      />

      {/* Footer */}
      <footer className="w-full border-t border-white/5 py-4 px-8 text-center text-xs text-slate-500 flex flex-wrap items-center justify-between gap-2">
        <span>AI Teacher — AI-Generated Visual Educational Tutor • Powered by LangGraph & Multi-Agent Architecture</span>
        <span className="text-slate-600">v2.0 Advanced Edition</span>
      </footer>
    </div>
  );
}
