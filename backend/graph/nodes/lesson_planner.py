import datetime
from typing import Dict, Any
from backend.graph.state import TeachingSessionState
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType

def lesson_planner_node(state: TeachingSessionState) -> Dict[str, Any]:
    topic = state.get("topic", "Ohm's Law")
    subject = state.get("subject", "Physics")
    student_level = state.get("student_level", "Beginner")
    teaching_style = state.get("teaching_style", "Visual")
    duration_target = state.get("duration_target", "20 min")
    
    logs = state.get("observability_logs", [])
    logs.append({
        "node": "lesson_planner",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detail": f"Generating curriculum for '{topic}' ({subject}) targeted at {student_level} student"
    })

    system_prompt = (
        "You are a master educational curriculum architect designing a high-yield, visual lesson. "
        "Every lesson must be structured sequentially into meaningful pedagogical chapters: "
        "1. Introduction & Motivation, 2. The Core Mental Model / Analogy, 3. The Mathematical / Conceptual Law, "
        "4. Step-by-Step Worked Demonstration, 5. Interactive Concept Checkpoint, 6. Real-World Applications & Wrap-up."
    )
    user_prompt = f"Design a {student_level} lesson for Topic: '{topic}', Subject: '{subject}', Style: '{teaching_style}', Target Time: '{duration_target}'."

    lesson_plan = LLMProvider.generate_json(
        task_type=TaskType.LESSON_PLANNING,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        schema_desc="{'subject': str, 'topic': str, 'prerequisites': list, 'learning_objectives': list, 'estimated_duration_sec': float, 'chapters': list}"
    )

    return {
        "lesson_plan": lesson_plan,
        "observability_logs": logs
    }
