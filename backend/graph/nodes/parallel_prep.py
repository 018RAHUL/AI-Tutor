import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
from backend.graph.state import TeachingSessionState
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType
from backend.visuals.engine import VisualEngine

def run_explanation_agent(topic: str, subject: str, level: str, chapters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Retrieve grounded knowledge graph for the specific topic
    kg = LLMProvider.get_topic_knowledge_graph(topic)
    narrations = kg.get("narrations", [])

    explanations = []
    for idx, chap in enumerate(chapters):
        if idx < len(narrations):
            script = narrations[idx]
        else:
            chap_title = chap.get("title", f"Chapter {idx+1}")
            script = (
                f"In this section on {chap_title}, we focus on applying the core principles of {topic}. "
                f"Notice how each governing parameter directly influences the system behavior."
            )

        explanations.append({
            "chapter_id": chap.get("id", f"chap_{idx}"),
            "chapter_title": chap.get("title", f"Chapter {idx+1}"),
            "script": script,
            "target_duration_sec": chap.get("estimated_sec", 30)
        })
    return explanations


def run_visual_agent(topic: str, subject: str, level: str, chapters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    kg = LLMProvider.get_topic_knowledge_graph(topic)
    formula_text = kg.get("formula", f"Principles of {topic}")
    formula_latex = kg.get("formula_latex", "")

    visual_plans = []
    for idx, chap in enumerate(chapters):
        v_payload = VisualEngine.generate_visual_for_scene(
            subject=subject,
            topic=topic,
            concept=chap.get("title", ""),
            narration=chap.get("title", ""),
            chapter_id=chap.get("id", ""),
            student_level=level
        )
        # Augment with topic formula and intuition
        v_payload["formula"] = formula_text
        v_payload["formula_latex"] = formula_latex
        v_payload["core_intuition"] = kg.get("core_intuition", "")

        visual_plans.append({
            "chapter_id": chap.get("id", f"chap_{idx}"),
            "visual_type": v_payload.get("type", "diagram"),
            "visual_payload": v_payload,
            "animation_triggers": ["on_narration_start", "on_variable_highlight", "on_calculation_step"]
        })
    return visual_plans


def run_examples_agent(topic: str, subject: str, level: str) -> List[Dict[str, Any]]:
    kg = LLMProvider.get_topic_knowledge_graph(topic)
    we = kg.get("worked_example", {})
    return [{
        "id": "ex_1",
        "title": we.get("title", f"Applied Demonstration for {topic}"),
        "given": we.get("given", "Initial parameters"),
        "formula": we.get("formula", kg.get("formula", "Governing Principle")),
        "steps": we.get("steps", ["1. Identify inputs", "2. Apply core law", "3. Evaluate output"]),
        "solution": we.get("solution", "Verified Successfully")
    }]


def run_questions_agent(topic: str, subject: str, level: str) -> List[Dict[str, Any]]:
    kg = LLMProvider.get_topic_knowledge_graph(topic)
    chk = kg.get("checkpoint", {})
    return [{
        "id": "q_checkpoint",
        "question": chk.get("question", f"What is the governing principle of {topic}?"),
        "options": chk.get("options", ["Direct cause-and-effect", "Independent random variation", "Static constant", "Non-linear decay"]),
        "expected_answer": chk.get("expected_answer", "Direct cause-and-effect"),
        "common_misconception": chk.get("misconception", "Confusing cause and effect variables"),
        "pedagogical_goal": f"Verify fundamental understanding of {topic}"
    }]


def run_assessment_agent(topic: str, subject: str, level: str) -> Dict[str, Any]:
    kg = LLMProvider.get_topic_knowledge_graph(topic)
    t_clean = kg.get("topic", topic)
    formula = kg.get("formula", f"Governing law of {topic}")

    return {
        "quiz_title": f"{t_clean} Mastery Evaluation",
        "questions": [
            {
                "id": "quiz_1",
                "question": f"What is the central governing principle or formula of {t_clean}?",
                "options": [
                    formula,
                    "Random non-deterministic variation",
                    "Independent static approximation",
                    "Inverse harmonic resonance only"
                ],
                "correct_answer": formula,
                "explanation": f"{t_clean} is defined by: {formula}."
            },
            {
                "id": "quiz_2",
                "question": f"In {t_clean}, what happens when the driving primary variable is increased?",
                "options": [
                    "The system reacts according to its governing mathematical relationship",
                    "No response occurs under any circumstance",
                    "The system instantly resets to zero",
                    "All parameters become undefined"
                ],
                "correct_answer": "The system reacts according to its governing mathematical relationship",
                "explanation": "Variables interact through predictable cause-and-effect mechanisms."
            },
            {
                "id": "quiz_3",
                "question": f"Which of the following is a key real-world application of {t_clean}?",
                "options": [
                    f"Designing, modeling, and analyzing systems involving {t_clean}",
                    "Replacing all experimental observations with pure guesswork",
                    "Ignoring input variables completely",
                    "Assuming all forces and flows are constant"
                ],
                "correct_answer": f"Designing, modeling, and analyzing systems involving {t_clean}",
                "explanation": f"Engineers and scientists apply {t_clean} to predict and optimize practical outcomes."
            }
        ]
    }


def parallel_prep_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Executes independent educational preparation agents concurrently in parallel.
    Uses ThreadPoolExecutor for true non-blocking multi-threaded task execution.
    """
    topic = state.get("topic", "Ohm's Law")
    subject = state.get("subject", "Physics")
    student_level = state.get("student_level", "Beginner")
    lesson_plan = state.get("lesson_plan", {})
    chapters = lesson_plan.get("chapters", [])

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_exp = executor.submit(run_explanation_agent, topic, subject, student_level, chapters)
        future_vis = executor.submit(run_visual_agent, topic, subject, student_level, chapters)
        future_ex = executor.submit(run_examples_agent, topic, subject, student_level)
        future_q = executor.submit(run_questions_agent, topic, subject, student_level)
        future_ass = executor.submit(run_assessment_agent, topic, subject, student_level)

        explanations = future_exp.result()
        visual_plans = future_vis.result()
        examples = future_ex.result()
        questions = future_q.result()
        assessment_plan = future_ass.result()

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    logs = state.get("observability_logs", [])
    logs.append({
        "node": "parallel_prep",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detail": f"Parallel preparation executed concurrently in {elapsed_ms}ms across 5 agents for '{topic}'."
    })

    return {
        "explanations": explanations,
        "visual_plans": visual_plans,
        "examples": examples,
        "questions": questions,
        "assessment_plan": assessment_plan,
        "observability_logs": logs
    }
