import pytest
from backend.graph.workflow import lesson_pipeline, interaction_pipeline
from backend.graph.state import TeachingSessionState

def test_langgraph_lesson_pipeline_parallel_prep():
    state: TeachingSessionState = {
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
        "student_response": None,
        "evaluation_result": None,
        "detected_misconceptions": [],
        "adaptive_scenes": [],
        "assessment_result": None,
        "learning_recommendations": [],
        "status": "created",
        "error": None,
        "observability_logs": []
    }

    result = lesson_pipeline.invoke(state)
    assert result["status"] == "ready"
    assert len(result["scenes"]) >= 5
    # Check that video duration is 2+ minutes (>= 120 sec)
    total_dur = sum(s["duration_sec"] for s in result["scenes"])
    assert total_dur >= 120.0
    
    # Check that parallel prep logs exist
    parallel_log = any("parallel_prep" in l.get("node", "") for l in result["observability_logs"])
    assert parallel_log is True
