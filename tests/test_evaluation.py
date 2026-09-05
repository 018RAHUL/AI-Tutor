import pytest
from backend.graph.workflow import interaction_pipeline

def test_misconception_detection_and_adaptive_remediation():
    # Student states misconception: "Current increases when resistance increases"
    state = {
        "lesson_id": "test_lesson_123",
        "user_id": "default_student",
        "topic": "Ohm's Law",
        "subject": "Physics",
        "student_level": "Beginner",
        "teaching_style": "Visual",
        "duration_target": "20 min",
        "source_type": "topic",
        "source_file": None,
        "rag_context": [],
        "student_profile": {},
        "lesson_plan": {},
        "explanations": [],
        "visual_plans": [],
        "examples": [],
        "questions": [],
        "assessment_plan": {},
        "scenes": [],
        "current_scene_index": 0,
        "student_response": "The current increases because resistance increases",
        "evaluation_result": None,
        "detected_misconceptions": [],
        "adaptive_scenes": [],
        "assessment_result": None,
        "learning_recommendations": [],
        "status": "evaluating",
        "error": None,
        "observability_logs": []
    }

    result = interaction_pipeline.invoke(state)
    eval_res = result.get("evaluation_result", {})
    assert eval_res.get("is_correct") is False
    assert eval_res.get("detected_misconception") is not None
    assert len(result.get("adaptive_scenes", [])) >= 1
    
    adaptive_scene = result["adaptive_scenes"][0]
    assert adaptive_scene["avatar_state"] == "RE_EXPLAINING"
    assert adaptive_scene["visual_type"] == "circuit_remediation"
