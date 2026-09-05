from enum import Enum
from typing import Optional, Dict, Any
from backend.config import GROQ_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY

class TaskType(str, Enum):
    LESSON_PLANNING = "LESSON_PLANNING"
    CONCEPT_EXPLANATION = "CONCEPT_EXPLANATION"
    TEACHER_SCRIPT = "TEACHER_SCRIPT"
    VISUAL_PLANNING = "VISUAL_PLANNING"
    EXAMPLE_GENERATION = "EXAMPLE_GENERATION"
    QUESTION_GENERATION = "QUESTION_GENERATION"
    ANSWER_EVALUATION = "ANSWER_EVALUATION"
    MISCONCEPTION_DETECTION = "MISCONCEPTION_DETECTION"
    ADAPTATION = "ADAPTATION"
    ASSESSMENT = "ASSESSMENT"
    LEARNING_PATH = "LEARNING_PATH"
    MATH_REASONING = "MATH_REASONING"
    CODE_EXPLANATION = "CODE_EXPLANATION"
    RAG_QA = "RAG_QA"
    SOCRATIC_TUTOR = "SOCRATIC_TUTOR"

class ModelRouter:
    """
    Intelligent Model Router that selects the optimal LLM provider and model
    based on task type, reasoning demands, speed, structured output needs,
    and available credentials.
    """

    @classmethod
    def get_route(cls, task_type: TaskType) -> Dict[str, Any]:
        has_groq = bool(GROQ_API_KEY)
        has_openai = bool(OPENAI_API_KEY)
        has_anthropic = bool(ANTHROPIC_API_KEY)
        has_gemini = bool(GEMINI_API_KEY)

        # High reasoning tasks
        deep_reasoning_tasks = {
            TaskType.LESSON_PLANNING,
            TaskType.MISCONCEPTION_DETECTION,
            TaskType.ADAPTATION,
            TaskType.MATH_REASONING,
            TaskType.ANSWER_EVALUATION
        }

        # Fast structured generation tasks
        fast_tasks = {
            TaskType.VISUAL_PLANNING,
            TaskType.QUESTION_GENERATION,
            TaskType.EXAMPLE_GENERATION,
            TaskType.ASSESSMENT,
            TaskType.LEARNING_PATH
        }

        if task_type in deep_reasoning_tasks:
            if has_openai:
                return {"provider": "openai", "model": "gpt-4o", "temperature": 0.3, "reasoning": "High-fidelity pedagogical evaluation"}
            elif has_groq:
                return {"provider": "groq", "model": "llama-3.3-70b-versatile", "temperature": 0.3, "reasoning": "Fast deep reasoning"}
            elif has_gemini:
                return {"provider": "gemini", "model": "gemini-2.0-flash", "temperature": 0.3, "reasoning": "Multimodal reasoning"}
            elif has_anthropic:
                return {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022", "temperature": 0.3, "reasoning": "Nuanced pedagogical analysis"}
            else:
                return {"provider": "local_expert", "model": "autonomous_curriculum_engine", "temperature": 0.2, "reasoning": "Offline deterministic reasoning"}

        else:
            if has_groq:
                return {"provider": "groq", "model": "llama-3.1-8b-instant", "temperature": 0.5, "reasoning": "Ultra-fast low-latency generation"}
            elif has_openai:
                return {"provider": "openai", "model": "gpt-4o-mini", "temperature": 0.4, "reasoning": "Fast lightweight synthesis"}
            elif has_gemini:
                return {"provider": "gemini", "model": "gemini-2.0-flash", "temperature": 0.4, "reasoning": "Fast structured synthesis"}
            elif has_anthropic:
                return {"provider": "anthropic", "model": "claude-3-5-haiku-20241022", "temperature": 0.4, "reasoning": "Fast synthesis"}
            else:
                return {"provider": "local_expert", "model": "autonomous_curriculum_engine", "temperature": 0.2, "reasoning": "Offline deterministic generation"}
