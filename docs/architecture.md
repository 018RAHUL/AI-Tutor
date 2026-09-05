# AI Teacher — System Architecture & Technical Specifications

## 1. Executive Summary
**AI Teacher** is a full-stack, scene-based AI Educational Video Generator and Interactive AI Teacher. It transforms any topic or uploaded educational material (PDF/TXT) into a synchronized 2+ minute educational explainer video complete with a living animated teacher avatar, subject-aware dynamic visual simulations, audio narration (Neural Edge-TTS), interactive question checkpoints, real-time misconception detection, and adaptive pedagogical re-teaching.

---

## 2. Core Architecture

```
[Student Topic / PDF Material]
             ↓
[Input & Subject Analyzer] → [RAG Vector Retriever]
             ↓
     [Student Profiler]
             ↓
     [Lesson Planner]
             ↓
 ┌─────────────────────────────────────────────────────────┐
 │   LangGraph Real Parallel Multi-Agent Preparation       │
 │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
 │ │ Explanation │ │   Visual    │ │  Examples & Checks  │ │
 │ │    Agent    │ │    Agent    │ │        Agent        │ │
 │ └─────────────┘ └─────────────┘ └─────────────────────┘ │
 └─────────────────────────────────────────────────────────┘
             ↓
     [Scene Planner (Fan-In)]
             ↓
 ┌─────────────────────────────────────────────────────────┐
 │                  Synchronized Scenes                    │
 │  • Subject Visuals (Circuits, Formulas, Code, Graphs)   │
 │  • Edge-TTS Neural Audio + Visemes                      │
 │  • Teacher Avatar (Expressions & Lip Movement)          │
 └─────────────────────────────────────────────────────────┘
             ↓
    [Interactive Checkpoint]
             ↓
      [Student Response]
             ↓
   [Semantic Evaluator] → [Misconception Detector]
             ↓
      [Adaptive Router]
      ├── Understood → Proceed to next concept
      └── Misconception → Inject Adaptive Scene (Remediation)
             ↓
      [Final Assessment & Personalized Learning Path]
```

---

## 3. Key Components

### A. LangGraph Orchestration & Real Parallelism
- Structured state machine managing session metadata, RAG context, student profile, scene queues, and remediation logs.
- Independent preparation agents (Explanation, Visual, Examples, Questions, Assessment) execute concurrently via multi-threaded asynchronous workers.

### B. Subject-Aware Visual Reasoning Engine
- **Physics**: Circuit simulations with live animated electron particles, water pipe physical analogy, Ohm's law formula derivations ($V=IR$), and worked calculations ($V=12\text{V}, R=4\Omega \implies I=3\text{A}$).
- **Computer Science**: Binary search divide-and-conquer steps with dynamic pointers (`low`, `mid`, `high`), array eliminations, and code execution tracing.
- **Mathematics**: Quadratic equations, parabolic curve plots, and step-by-step discriminant calculations.

### C. Animated Teacher Avatar & Speech
- Real-time animated avatar with eye blinking, continuous breathing/head bobbing, and phoneme-driven mouth animations.
- Expressive states: `IDLE`, `SPEAKING`, `EXPLAINING`, `QUESTIONING`, `LISTENING`, `THINKING`, `CORRECT`, `MISCONCEPTION`, `RE_EXPLAINING`.
- Spoken voice powered by Neural Edge-TTS (`en-US-ChristopherNeural`) with local asset caching.

### D. Misconception Detection & Adaptive Remediation
- Semantic diagnosis of student responses.
- Catches inverse vs direct proportionality misconceptions (e.g., student asserting current increases when resistance increases).
- Dynamically synthesizes and injects targeted remediation scenes with simplified physical analogies (pipe narrowing) before resuming the lesson.

---

## 4. Hardware Modes & Performance
- **Offline / Autonomous Mode**: Built-in curriculum engines and visual generators operate with 0 external API dependencies.
- **Enhanced LLM Mode**: Seamlessly routes tasks to Groq, OpenAI, Anthropic, Gemini, or Ollama when keys are configured.
- **Lightweight Composition**: Uses HTML5 Canvas / SVG 60 FPS client rendering and optional FFmpeg standalone MP4 exporter.
