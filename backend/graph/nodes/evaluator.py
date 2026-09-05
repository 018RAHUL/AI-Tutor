import datetime
from typing import Dict, Any
from backend.graph.state import TeachingSessionState
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType

def evaluator_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Evaluates student response for semantic correctness, reasoning depth, and confidence.
    """
    topic = state.get("topic", "Ohm's Law")
    student_response = state.get("student_response", "").strip()
    
    logs = state.get("observability_logs", [])
    logs.append({
        "node": "evaluator",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detail": f"Evaluating student response: '{student_response}'"
    })

    system_prompt = (
        "You are an expert pedagogical evaluator. Evaluate the student's answer for correctness, "
        "identifying if they have mastered the underlying physical or mathematical mechanism."
    )
    user_prompt = f"Topic: {topic}. Student Answer: '{student_response}'. Expected Concept: Ohm's Law (I = V/R, current decreases as resistance increases with constant voltage)."

    eval_result = LLMProvider.generate_json(
        task_type=TaskType.ANSWER_EVALUATION,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        schema_desc="{'is_correct': bool, 'confidence': float, 'feedback': str, 'detected_misconception': str or null, 'adaptation_strategy': str}"
    )

    return {
        "evaluation_result": eval_result,
        "observability_logs": logs
    }


def misconception_detector_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Diagnoses exact cognitive misconceptions and classifies the learning gap.
    """
    eval_res = state.get("evaluation_result", {})
    student_response = state.get("student_response", "")
    is_correct = eval_res.get("is_correct", False)
    
    misconceptions = state.get("detected_misconceptions", [])
    logs = state.get("observability_logs", [])

    if not is_correct:
        detected_name = eval_res.get("detected_misconception", "General Misconception")
        misc_entry = {
            "misconception": detected_name,
            "student_input": student_response,
            "remediation_status": "in_progress",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        misconceptions.append(misc_entry)
        logs.append({
            "node": "misconception_detector",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "detail": f"Misconception identified: '{detected_name}'. Triggering adaptive re-teaching branch."
        })
    else:
        logs.append({
            "node": "misconception_detector",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "detail": "No misconceptions detected. Concept understood accurately."
        })

    return {
        "detected_misconceptions": misconceptions,
        "observability_logs": logs
    }
