import { apiFetch } from '../api';
import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Volume2,
  VolumeX,
  Maximize,
  HelpCircle,
  Sparkles,
  Send,
  Mic,
  MicOff,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Activity,
  Layers,
  Tv,
  SlidersHorizontal,
  Compass,
  Lightbulb,
  Clock,
  ArrowRight
} from 'lucide-react';
import TeacherAvatar from './TeacherAvatar';
import VisualStage from './VisualStage';
import SocraticTutorChat from './SocraticTutorChat';

export default function AIClassroom({
  lesson,
  onCompleteLesson,
  onOpenObservability,
  onOpenSummary,
  currentUser
}) {
  const [scenes, setScenes] = useState(lesson?.scenes || []);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [viewMode, setViewMode] = useState('video'); // 'video' or 'interactive_sim'
  const [socraticTutorOpen, setSocraticTutorOpen] = useState(false);
  
  // Interactive Checkpoint State
  const [showQuestionModal, setShowQuestionModal] = useState(false);
  const [studentAnswer, setStudentAnswer] = useState('');
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [isListeningVoice, setIsListeningVoice] = useState(false);

  // Audio & Video player refs
  const audioRef = useRef(null);
  const videoRef = useRef(null);
  const stageContainerRef = useRef(null);

  const currentScene = scenes[currentIdx] || null;

  // Determine if this topic / scene actually needs / supports simulation
  const hasSimulation = Boolean(
    currentScene?.has_simulation ||
    currentScene?.visual_payload?.has_simulation ||
    ['circuit_intro', 'water_analogy', 'binary_search_animation', 'math_quadratic_visual', 'circuit_remediation'].includes(currentScene?.visual_type)
  );

  // Default to video mode if simulation is not supported for this topic
  useEffect(() => {
    if (!hasSimulation && viewMode === 'interactive_sim') {
      setViewMode('video');
    }
  }, [hasSimulation, viewMode]);

  // Sync scenes when lesson prop changes
  useEffect(() => {
    if (lesson?.scenes) {
      setScenes(lesson.scenes);
      setCurrentIdx(0);
    }
  }, [lesson]);

  // Keyboard shortcuts (Space for Play/Pause, Arrow keys for scenes)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return;
      if (e.code === 'Space') {
        e.preventDefault();
        setIsPlaying((prev) => !prev);
      } else if (e.code === 'ArrowRight') {
        handleNext();
      } else if (e.code === 'ArrowLeft') {
        handlePrev();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIdx, scenes]);

  // Playback & Audio/Video Synchronization
  useEffect(() => {
    if (!currentScene) return;

    const hasVideo = Boolean(currentScene.video_url) && viewMode === 'video';

    if (hasVideo) {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      if (videoRef.current) {
        videoRef.current.playbackRate = playbackSpeed;
        videoRef.current.muted = isMuted;
        if (isPlaying) {
          videoRef.current.play().catch(() => {});
        } else {
          videoRef.current.pause();
        }
      }
    } else {
      if (videoRef.current) {
        videoRef.current.pause();
      }
      if (audioRef.current && currentScene.audio_url) {
        audioRef.current.src = currentScene.audio_url;
        audioRef.current.playbackRate = playbackSpeed;
        audioRef.current.muted = isMuted;

        if (isPlaying) {
          audioRef.current.play().catch(() => {});
        } else {
          audioRef.current.pause();
        }
      }
    }
  }, [currentIdx, currentScene, isPlaying, playbackSpeed, isMuted, viewMode]);

  const handleMediaEnded = () => {
    if (currentScene?.is_interactive && !evaluationResult) {
      setIsPlaying(false);
      setShowQuestionModal(true);
    } else if (currentIdx < scenes.length - 1) {
      setCurrentIdx((prev) => prev + 1);
      setCurrentTime(0);
    } else {
      setIsPlaying(false);
      onCompleteLesson();
    }
  };

  const handleNext = () => {
    if (currentIdx < scenes.length - 1) {
      setCurrentIdx((prev) => prev + 1);
      setShowQuestionModal(false);
      setEvaluationResult(null);
      setCurrentTime(0);
    } else {
      onCompleteLesson();
    }
  };

  const handlePrev = () => {
    if (currentIdx > 0) {
      setCurrentIdx((prev) => prev - 1);
      setShowQuestionModal(false);
      setEvaluationResult(null);
      setCurrentTime(0);
    }
  };

  const toggleFullScreen = () => {
    if (!document.fullscreenElement) {
      stageContainerRef.current?.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  };

  const formatTime = (secs) => {
    if (!secs || isNaN(secs)) return '0:00';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  // Web Speech API for voice answer
  const toggleSpeechRecognition = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Speech Recognition is not supported in this browser. Please type your answer.');
      return;
    }

    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    if (!isListeningVoice) {
      setIsListeningVoice(true);
      recognition.start();

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setStudentAnswer(transcript);
        setIsListeningVoice(false);
      };

      recognition.onerror = () => {
        setIsListeningVoice(false);
      };

      recognition.onend = () => {
        setIsListeningVoice(false);
      };
    } else {
      setIsListeningVoice(false);
    }
  };

  // Submit Answer to Backend Evaluator & Adaptive Router
  const handleAnswerSubmit = async (e) => {
    e?.preventDefault();
    if (!studentAnswer.trim()) return;

    setIsEvaluating(true);
    const lessonId = lesson?.id || lesson?.lesson_id;
    try {
      const res = await apiFetch(`/api/lesson/${lessonId}/interact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scene_id: currentScene.id,
          question_text: currentScene.question_text || `Checkpoint for ${lesson?.topic || "Lesson"}`,
          student_response: studentAnswer
        })
      });

      const data = await res.json();
      setEvaluationResult(data);

      if (data.adaptive_scene) {
        const newScenes = [...scenes];
        newScenes.splice(currentIdx + 1, 0, data.adaptive_scene);
        setScenes(newScenes);
      }
    } catch (err) {
      console.error('Evaluation error:', err);
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleContinueAfterEval = () => {
    setShowQuestionModal(false);
    setStudentAnswer('');
    setIsPlaying(true);
    handleNext();
  };

  const totalLessonDurationSec = scenes.reduce((acc, sc) => acc + (sc.duration_sec || 28), 0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 animate-fade-in">
      <audio
        ref={audioRef}
        onEnded={handleMediaEnded}
        onTimeUpdate={() => setCurrentTime(audioRef.current?.currentTime || 0)}
        onLoadedMetadata={() => setDuration(audioRef.current?.duration || currentScene?.duration_sec || 25)}
      />

      {/* Top Header Navigation & Utility Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/70 border border-white/10 backdrop-blur-md shadow-lg">
        <div className="flex items-center gap-3">
          <span className="px-3.5 py-1.5 rounded-full text-xs font-bold bg-gradient-to-r from-sky-500 to-blue-600 text-white shadow-md shadow-sky-500/20">
            {lesson?.topic || "Core Topic"}
          </span>
          <div className="hidden sm:block text-slate-400 text-xs">/</div>
          <span className="text-xs sm:text-sm text-slate-200 font-semibold tracking-wide">
            {currentScene?.chapter_title || `Chapter ${currentIdx + 1}`}
          </span>
        </div>

        <div className="flex items-center gap-2.5">
          {/* Conditional View Mode Switcher: Only display if topic supports/needs simulation */}
          {hasSimulation && (
            <div className="flex items-center bg-slate-950/80 border border-slate-700/80 rounded-xl p-0.5 shadow-inner">
              <button
                onClick={() => setViewMode('video')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  viewMode === 'video'
                    ? 'bg-sky-500 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="AI Video Animation"
              >
                <Tv className="w-3.5 h-3.5" />
                <span>AI Video</span>
              </button>
              <button
                onClick={() => setViewMode('interactive_sim')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  viewMode === 'interactive_sim'
                    ? 'bg-sky-500 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
                title="Interactive Simulation & Sandbox"
              >
                <SlidersHorizontal className="w-3.5 h-3.5" />
                <span>Live Sim</span>
              </button>
            </div>
          )}

          {/* Socratic AI Tutor Action Button */}
          <button
            onClick={() => setSocraticTutorOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-brand-500/20 via-sky-500/20 to-indigo-500/20 border border-brand-500/40 text-brand-300 hover:text-white hover:bg-brand-500/30 text-xs font-semibold transition-all shadow-sm"
            title="Open Live Socratic AI Tutor"
          >
            <Sparkles className="w-3.5 h-3.5 text-brand-400 animate-pulse" />
            <span>Ask AI Tutor</span>
          </button>

          {/* Study Notes & Summary Hub Trigger */}
          {onOpenSummary && (
            <button
              onClick={onOpenSummary}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-brand-500/20 hover:bg-brand-500/30 border border-brand-500/50 text-brand-300 text-xs font-semibold shadow-sm transition-all"
              title="View Comprehensive Lesson Study Notes, Formulas & Flashcards"
            >
              <BookOpen className="w-3.5 h-3.5 text-brand-400" />
              <span>Study Notes & Summary</span>
            </button>
          )}

          {/* Observability Multi-Agent Graph Trigger */}
          {onOpenObservability && (
            <button
              onClick={onOpenObservability}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 hover:text-sky-300 hover:border-sky-500/50 text-xs font-semibold transition-all"
              title="View Multi-Agent Reasoning Graph"
            >
              <Activity className="w-3.5 h-3.5 text-sky-400" />
              <span className="hidden md:inline">Multi-Agent Graph</span>
            </button>
          )}

          {/* Fullscreen Trigger */}
          <button
            onClick={toggleFullScreen}
            className="p-1.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition-colors"
            title="Toggle Fullscreen Theater"
          >
            <Maximize className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Spacious Stage & Dedicated Teacher Companion Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start">
        
        {/* Left Column: Expansive 16:9 Educational Video & Stage (Spacious, Unobstructed) */}
        <div className="lg:col-span-8 xl:col-span-8 flex flex-col space-y-4">
          <div 
            ref={stageContainerRef}
            className="relative w-full aspect-video min-h-[220px] sm:min-h-[340px] md:min-h-[420px] bg-slate-950 rounded-3xl border border-sky-500/20 overflow-hidden shadow-2xl flex flex-col justify-between group"
          >
            {/* Top Stage Sub-Header Badge */}
            <div className="absolute top-3 sm:top-4 left-3 sm:left-4 z-20 flex items-center gap-2 pointer-events-none">
              <span className="px-2.5 sm:px-3 py-1 rounded-xl bg-slate-950/80 backdrop-blur-md border border-white/10 text-[11px] sm:text-xs font-semibold text-slate-200 shadow-md">
                Chapter {currentIdx + 1} of {scenes.length}
              </span>
              {viewMode === 'video' && currentScene?.video_url && (
                <span className="px-2.5 py-1 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-[10px] font-bold text-emerald-300 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  HD Video
                </span>
              )}
            </div>

            {/* Central Visual & Video Playback Area: 100% Free of Overlapping Avatars */}
            <div className="relative w-full h-full flex items-center justify-center p-2 sm:p-4">
              {viewMode === 'video' && currentScene?.video_url ? (
                <video
                  ref={videoRef}
                  key={currentScene.video_url}
                  src={currentScene.video_url}
                  autoPlay={false}
                  loop={false}
                  muted={isMuted}
                  playsInline
                  onEnded={handleMediaEnded}
                  onTimeUpdate={() => setCurrentTime(videoRef.current?.currentTime || 0)}
                  onLoadedMetadata={() => setDuration(videoRef.current?.duration || currentScene?.duration_sec || 25)}
                  className="w-full h-full object-contain rounded-2xl bg-black shadow-inner"
                />
              ) : (
                <VisualStage scene={currentScene} isPlaying={isPlaying} sceneIndex={currentIdx} />
              )}
            </div>

            {/* Interactive Checkpoint Pause Modal Overlay */}
            {showQuestionModal && (
              <div className="absolute inset-0 z-40 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 animate-fade-in">
                <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-amber-500/40 max-w-xl w-full shadow-2xl space-y-5">
                  {!evaluationResult ? (
                    <>
                      <div className="flex items-center gap-2.5 text-amber-400 font-bold text-sm">
                        <HelpCircle className="w-5 h-5 animate-pulse" />
                        <span>Teacher Concept Checkpoint</span>
                      </div>

                      <p className="text-sm sm:text-base text-white font-semibold leading-relaxed">
                        {currentScene?.question_text || `Checkpoint for ${lesson?.topic || "this topic"}`}
                      </p>

                      {/* Multiple Choice Options */}
                      {currentScene?.question_options && currentScene.question_options.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                          {currentScene.question_options.map((opt, idx) => (
                            <button
                              key={idx}
                              type="button"
                              onClick={() => setStudentAnswer(opt)}
                              className={`p-3 rounded-xl text-left text-xs font-medium border transition-all ${
                                studentAnswer === opt
                                  ? 'bg-sky-500/20 border-sky-500 text-sky-300 shadow-md'
                                  : 'bg-slate-900/80 border-slate-800 text-slate-300 hover:bg-slate-800 hover:text-white'
                              }`}
                            >
                              {opt}
                            </button>
                          ))}
                        </div>
                      )}

                      <form onSubmit={handleAnswerSubmit} className="space-y-3.5">
                        <div className="relative">
                          <input
                            type="text"
                            value={studentAnswer}
                            onChange={(e) => setStudentAnswer(e.target.value)}
                            placeholder="Type your answer or speak with the microphone..."
                            className="w-full px-4 py-3 pr-12 rounded-xl bg-slate-900 border border-slate-700 text-slate-100 text-xs sm:text-sm focus:outline-none focus:border-sky-500 shadow-inner"
                          />
                          <button
                            type="button"
                            onClick={toggleSpeechRecognition}
                            className={`absolute right-2 top-2 p-2 rounded-lg transition-colors ${
                              isListeningVoice ? 'bg-rose-500 text-white animate-pulse' : 'text-slate-400 hover:text-white'
                            }`}
                            title="Speech Recognition"
                          >
                            {isListeningVoice ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                          </button>
                        </div>

                        <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
                          <span className="text-[11px] text-slate-400">
                            Evaluated for deep conceptual intuition & misconception detection.
                          </span>
                          <button
                            type="submit"
                            disabled={isEvaluating || !studentAnswer.trim()}
                            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white font-semibold text-xs transition-all disabled:opacity-50 shadow-lg shadow-sky-500/25"
                          >
                            {isEvaluating ? (
                              <>
                                <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                <span>Evaluating...</span>
                              </>
                            ) : (
                              <>
                                <Send className="w-3.5 h-3.5" />
                                <span>Submit Answer</span>
                              </>
                            )}
                          </button>
                        </div>
                      </form>
                    </>
                  ) : (
                    /* Evaluation & Remediation Result */
                    <div className="space-y-4">
                      <div className="flex items-center gap-3">
                        {evaluationResult.has_misconception ? (
                          <div className="p-2.5 rounded-xl bg-rose-500/20 border border-rose-500/50 text-rose-400">
                            <AlertTriangle className="w-6 h-6" />
                          </div>
                        ) : (
                          <div className="p-2.5 rounded-xl bg-emerald-500/20 border border-emerald-500/50 text-emerald-400">
                            <CheckCircle2 className="w-6 h-6" />
                          </div>
                        )}
                        <div>
                          <h4 className="font-bold text-sm sm:text-base text-white">
                            {evaluationResult.has_misconception ? 'Misconception Diagnosed' : 'Outstanding Understanding!'}
                          </h4>
                          <p className="text-xs text-slate-400">
                            {evaluationResult.evaluation?.detected_misconception || 'Physical mechanism verified accurately'}
                          </p>
                        </div>
                      </div>

                      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                        {evaluationResult.evaluation?.feedback || 'Your explanation matches the physical laws governing this concept.'}
                      </div>

                      {evaluationResult.adaptive_scene && (
                        <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-xs text-amber-300 flex items-center gap-2">
                          <Sparkles className="w-4 h-4 shrink-0 text-amber-400" />
                          <span>Adaptive Scene Injected: Teacher will re-explain with an intuitive comparison.</span>
                        </div>
                      )}

                      <div className="flex justify-end pt-2">
                        <button
                          onClick={handleContinueAfterEval}
                          className="px-6 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-600 text-white font-semibold text-xs shadow-lg transition-all"
                        >
                          Continue Lesson Video →
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Spacious External Playback Control Bar (Never overlaps stage content!) */}
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-white/10 backdrop-blur-md shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
            {/* Left Transport Controls */}
            <div className="flex items-center gap-2.5">
              <button
                onClick={handlePrev}
                disabled={currentIdx === 0}
                className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-30"
                title="Previous Scene (Left Arrow)"
              >
                <SkipBack className="w-4 h-4" />
              </button>

              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-3 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-600 hover:to-blue-700 text-white shadow-lg shadow-sky-500/25 transition-all"
                title={isPlaying ? 'Pause (Space)' : 'Play (Space)'}
              >
                {isPlaying ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current" />}
              </button>

              <button
                onClick={handleNext}
                disabled={currentIdx === scenes.length - 1}
                className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors disabled:opacity-30"
                title="Next Scene (Right Arrow)"
              >
                <SkipForward className="w-4 h-4" />
              </button>

              <div className="h-4 w-px bg-slate-700 mx-1" />

              <button
                onClick={() => setIsMuted(!isMuted)}
                className="p-2.5 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
                title={isMuted ? 'Unmute' : 'Mute'}
              >
                {isMuted ? <VolumeX className="w-4 h-4 text-rose-400" /> : <Volume2 className="w-4 h-4" />}
              </button>

              <span className="text-xs font-mono text-slate-400">
                {formatTime(currentTime)} / {formatTime(duration || currentScene?.duration_sec || 25)}
              </span>
            </div>

            {/* Center Chapter Scrubber Pills */}
            <div className="flex items-center gap-2 overflow-x-auto py-1">
              {scenes.map((sc, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setCurrentIdx(idx);
                    setShowQuestionModal(false);
                    setCurrentTime(0);
                  }}
                  className={`h-2.5 rounded-full transition-all duration-300 ${
                    idx === currentIdx
                      ? 'w-10 bg-gradient-to-r from-sky-400 to-blue-500 shadow-sm shadow-sky-400'
                      : idx < currentIdx
                      ? 'w-3.5 bg-sky-800 hover:bg-sky-600'
                      : 'w-3.5 bg-slate-800 hover:bg-slate-700'
                  }`}
                  title={`Scene ${idx + 1}: ${sc.chapter_title}`}
                />
              ))}
            </div>

            {/* Right Speed & Progress Stats */}
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-slate-400">
                Ch. {currentIdx + 1}/{scenes.length}
              </span>

              <select
                value={playbackSpeed}
                onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
                className="bg-slate-950 border border-slate-700 text-slate-300 text-xs rounded-xl px-2.5 py-1.5 focus:outline-none focus:border-sky-500"
              >
                <option value="0.75">0.75x</option>
                <option value="1">1.0x</option>
                <option value="1.25">1.25x</option>
                <option value="1.5">1.5x</option>
              </select>
            </div>
          </div>

          {/* Clean Dedicated Narration Transcript Card (Placed BELOW Video Player, 0% Video Overlap) */}
          {(currentScene?.narration || currentScene?.subtitle) && (
            <div className="p-4 rounded-2xl bg-slate-900/90 border border-sky-500/20 shadow-xl space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
                  <Volume2 className="w-3.5 h-3.5 text-sky-400" />
                  <span>Teacher Voice Narration & Transcript</span>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-300 font-mono">
                  Scene {currentIdx + 1} of {scenes.length}
                </span>
              </div>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-normal">
                {currentScene?.narration || currentScene?.subtitle}
              </p>
            </div>
          )}
        </div>

        {/* Right Column: Dedicated AI Teacher Companion Pod (Completely separate from stage!) */}
        <div className="lg:col-span-4 xl:col-span-4 flex flex-col space-y-4">
          
          {/* AI Teacher Avatar Pod Card */}
          <div className="glass-card p-4 rounded-3xl border border-white/10 shadow-xl flex flex-col items-center justify-center space-y-2 relative overflow-hidden bg-slate-900/60">
            <TeacherAvatar
              avatarState={currentScene?.avatar_state || (isPlaying ? 'SPEAKING' : 'IDLE')}
              isPlaying={isPlaying}
              name="Prof. Maya"
            />
          </div>

          {/* Socratic Hint & Prompt Launchpad */}
          <div className="glass-card p-4 rounded-3xl border border-white/10 shadow-xl space-y-3 bg-slate-900/60">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-200 flex items-center gap-1.5">
                <Lightbulb className="w-4 h-4 text-amber-400" />
                <span>AI Socratic Guidance</span>
              </span>
              <button
                onClick={() => setSocraticTutorOpen(true)}
                className="text-[11px] font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1"
              >
                <Sparkles className="w-3 h-3" /> Full Chat
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setSocraticTutorOpen(true)}
                className="p-2 rounded-xl bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/30 text-left text-[11px] text-slate-300 transition-all flex flex-col gap-1"
              >
                <span className="font-semibold text-amber-300">💡 Tiered Hint</span>
                <span className="text-[10px] text-slate-400">Step-by-step intuition</span>
              </button>

              <button
                onClick={() => setSocraticTutorOpen(true)}
                className="p-2 rounded-xl bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/30 text-left text-[11px] text-slate-300 transition-all flex flex-col gap-1"
              >
                <span className="font-semibold text-sky-300">🌊 Analogy</span>
                <span className="text-[10px] text-slate-400">Mechanical model</span>
              </button>
            </div>
          </div>

          {/* Current Chapter Takeaways */}
          <div className="glass-card p-4 rounded-3xl border border-white/10 shadow-xl space-y-2.5 bg-slate-900/60">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-200">
              <Compass className="w-4 h-4 text-emerald-400" />
              <span>Chapter Objective</span>
            </div>
            
            <p className="text-xs text-slate-300 leading-relaxed">
              {currentScene?.learning_objective || `Master foundational mechanisms and relationships of ${lesson?.topic || "this concept"}.`}
            </p>

            {/* Formula pills if present */}
            {(lesson?.summary?.formulas?.length > 0 || currentScene?.formula) && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {(
                  lesson?.summary?.formulas?.map((f) => f.formula_text || f.name) ||
                  (currentScene?.formula ? [currentScene.formula] : [])
                ).slice(0, 2).map((formText, fIdx) => (
                  <span
                    key={fIdx}
                    className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-semibold bg-sky-500/20 text-sky-300 border border-sky-500/30 truncate max-w-full"
                    title={formText}
                  >
                    📐 {formText}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Curriculum Sequence Section: Spacious, Clear, Elegantly Structured */}
      <div className="glass-card p-5 sm:p-6 rounded-3xl border border-white/10 shadow-xl space-y-4 bg-slate-900/40">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-sky-400" />
            <h3 className="font-bold text-sm text-slate-100">Curriculum Chapter Sequence</h3>
          </div>
          <div className="flex items-center gap-2 text-slate-400 font-mono text-xs">
            <Clock className="w-3.5 h-3.5" />
            <span>Total Duration: ~{Math.max(1, Math.round(totalLessonDurationSec / 60))} min</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {scenes.map((sc, idx) => (
            <button
              key={idx}
              onClick={() => {
                setCurrentIdx(idx);
                setShowQuestionModal(false);
                setCurrentTime(0);
              }}
              className={`p-3.5 rounded-2xl text-left text-xs transition-all border flex flex-col justify-between space-y-2 ${
                idx === currentIdx
                  ? 'bg-sky-500/20 border-sky-500 text-sky-200 shadow-lg shadow-sky-500/10 scale-[1.02]'
                  : idx < currentIdx
                  ? 'bg-slate-900/80 border-slate-800 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-950/60 border-slate-900 text-slate-400 hover:bg-slate-900'
              }`}
            >
              <div className="flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>CH. {idx + 1}</span>
                {idx === currentIdx && <span className="w-2 h-2 rounded-full bg-sky-400 animate-pulse" />}
                {idx < currentIdx && <CheckCircle2 className="w-3 h-3 text-emerald-400" />}
              </div>
              <div className="font-semibold text-slate-200 line-clamp-2 leading-snug">
                {sc.chapter_title}
              </div>
              <div className="text-[10px] text-slate-500 font-mono">
                ~{Math.round(sc.duration_sec || 28)}s
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Live Socratic AI Tutor Drawer */}
      <SocraticTutorChat
        isOpen={socraticTutorOpen}
        onClose={() => setSocraticTutorOpen(false)}
        lessonId={lesson?.id}
        currentScene={currentScene}
        topic={lesson?.topic || "Core Topic"}
        learningStyle={currentUser?.profile?.learning_style || "Visual"}
      />
    </div>
  );
}
