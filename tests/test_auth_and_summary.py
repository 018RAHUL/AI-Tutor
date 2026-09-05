import uuid
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.agents.summary_agent import SummaryAgent
from backend.agents.tutor_agent import SocraticTutorAgent
from backend.agents.analytics_agent import MasteryAnalyticsAgent

client = TestClient(app)

def test_auth_registration_login_profile():
    unique_suffix = uuid.uuid4().hex[:6]
    test_user = f"alex_einstein_{unique_suffix}"
    test_email = f"alex_{unique_suffix}@example.com"

    # 1. Register a new student
    reg_payload = {
        "username": test_user,
        "email": test_email,
        "password": "SecurePassword123!",
        "full_name": "Alex Einstein",
        "grade_level": "Beginner",
        "learning_style": "Visual",
        "learning_goal": "Master Physics & Electrical Circuits",
        "avatar_url": "avatar_2"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 200
    reg_data = res_reg.json()
    assert "token" in reg_data
    assert reg_data["user"]["username"] == test_user
    assert reg_data["user"]["full_name"] == "Alex Einstein"
    assert reg_data["user"]["profile"]["learning_style"] == "Visual"
    user_id = reg_data["user"]["id"]

    # 2. Login with credentials
    login_payload = {
        "username_or_email": test_email,
        "password": "SecurePassword123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    login_data = res_login.json()
    token = login_data["token"]
    assert token.startswith("usr_tok_")

    # 3. Update profile
    update_payload = {
        "user_id": user_id,
        "full_name": "Dr. Alex Einstein",
        "grade_level": "Intermediate",
        "learning_style": "Socratic"
    }
    res_up = client.put("/api/auth/profile", json=update_payload)
    assert res_up.status_code == 200
    up_data = res_up.json()
    assert up_data["user"]["full_name"] == "Dr. Alex Einstein"
    assert up_data["user"]["profile"]["grade_level"] == "Intermediate"
    assert up_data["user"]["profile"]["learning_style"] == "Socratic"


def test_summary_agent_and_endpoints():
    # 1. Test SummaryAgent directly
    summary = SummaryAgent.generate_summary("Ohm's Law", "Physics", "Beginner")
    assert "executive_summary" in summary
    assert len(summary["formulas"]) >= 3
    assert len(summary["flashcards"]) >= 2
    assert len(summary["common_pitfalls"]) >= 2

    # 2. Test Markdown generation
    md_text = SummaryAgent.generate_markdown_notes(summary)
    assert "Ohm's Law" in md_text
    assert "Executive Summary" in md_text
    assert "Key Formulas" in md_text


def test_socratic_tutor_agent():
    # 1. Ask for a hint
    reply_hint = SocraticTutorAgent.answer_query(
        topic="Ohm's Law",
        current_scene_title="Interactive Checkpoint",
        current_scene_narration="If voltage is constant and resistance increases, what happens?",
        student_query="Can you give me a hint about resistance?",
        learning_style="Visual"
    )
    assert "response" in reply_hint
    assert "denominator" in reply_hint["response"].lower() or "formula" in reply_hint["response"].lower() or "hint" in reply_hint["response"].lower()

    # 2. Ask for an analogy
    reply_analogy = SocraticTutorAgent.answer_query(
        topic="Ohm's Law",
        current_scene_title="Analogy Scene",
        current_scene_narration="",
        student_query="Explain this to me with a water pipe analogy",
        learning_style="Visual"
    )
    assert "water" in reply_analogy["response"].lower() or "pipe" in reply_analogy["response"].lower()


def test_mastery_analytics_agent():
    quiz_schema = {
        "quiz_title": "Ohm's Law Mastery Evaluation",
        "questions": [
            {"id": "q1", "question": "Unit of resistance?", "correct_answer": "Ohm (Ω)", "explanation": "Measured in Ohms"},
            {"id": "q2", "question": "I = V / R with 12V and 4Ω?", "correct_answer": "3 A", "explanation": "12 / 4 = 3"}
        ]
    }
    submission = [
        {"question_id": "q1", "selected_answer": "Ohm (Ω)"},
        {"question_id": "q2", "selected_answer": "3 A"}
    ]
    eval_res = MasteryAnalyticsAgent.evaluate_quiz_performance(submission, quiz_schema, {})
    assert eval_res["score_pct"] == 100.0
    assert eval_res["mastery_level"] == "Mastered"
