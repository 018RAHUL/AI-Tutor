import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_full_ohms_law_e2e_benchmark():
    # 1. Health check
    res_health = client.get("/api/health")
    assert res_health.status_code == 200

    # 2. Create lesson: Ohm's Law for Beginner
    create_payload = {
        "topic": "Ohm's Law",
        "student_level": "Beginner",
        "teaching_style": "Visual",
        "duration_target": "20 min",
        "user_id": "default_student",
        "source_type": "topic"
    }
    res_create = client.post("/api/lesson/create", json=create_payload)
    assert res_create.status_code == 200
    data = res_create.json()
    lesson_id = data["lesson_id"]
    assert lesson_id is not None
    assert len(data["scenes"]) >= 5
    assert data["estimated_duration_sec"] >= 120.0

    # 3. Retrieve lesson
    res_get = client.get(f"/api/lesson/{lesson_id}")
    assert res_get.status_code == 200
    lesson_data = res_get.json()
    assert len(lesson_data["scenes"]) == len(data["scenes"])

    # 4. Interactive student answer with misconception
    interact_payload = {
        "scene_id": lesson_data["scenes"][4]["id"],
        "question_text": "If Voltage remains constant and Resistance increases, what happens to Current?",
        "student_response": "Current will increase because of higher resistance."
    }
    res_interact = client.post(f"/api/lesson/{lesson_id}/interact", json=interact_payload)
    assert res_interact.status_code == 200
    interact_data = res_interact.json()
    assert interact_data["has_misconception"] is True
    assert interact_data["adaptive_scene"] is not None
    assert interact_data["adaptive_scene"]["avatar_state"] == "RE_EXPLAINING"

    # 5. Check learning profile and path
    res_prof = client.get("/api/profile/default_student")
    assert res_prof.status_code == 200

    res_path = client.get("/api/learning-path/Ohm's Law")
    assert res_path.status_code == 200
    assert len(res_path.json()["nodes"]) >= 3
