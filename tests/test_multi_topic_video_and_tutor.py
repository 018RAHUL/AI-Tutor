import pytest
from backend.agents.tutor_agent import SocraticTutorAgent
from backend.visuals.engine import VisualEngine
from backend.agents.summary_agent import SummaryAgent
from backend.models.llm_provider import LLMProvider
from backend.video.renderer import VideoRenderer

def test_tutor_agent_multi_topic():
    # 1. Photosynthesis
    photo_tutor = SocraticTutorAgent.answer_query(
        topic="Photosynthesis",
        current_scene_title="Thylakoid Light Reaction",
        current_scene_narration="Water molecules split into oxygen and protons.",
        student_query="Where does the released oxygen come from?",
        learning_style="Visual"
    )
    assert "photosynthesis" in photo_tutor["response"].lower() or "water" in photo_tutor["response"].lower() or "light" in photo_tutor["response"].lower()

    # 2. Newton's Laws
    newton_tutor = SocraticTutorAgent.answer_query(
        topic="Newton's Second Law",
        current_scene_title="Force and Acceleration",
        current_scene_narration="Applying 2500N thrust on a 500kg mass.",
        student_query="Can you give me a hint on how to calculate acceleration?",
        learning_style="Visual"
    )
    assert "newton" in newton_tutor["response"].lower() or "force" in newton_tutor["response"].lower() or "acceleration" in newton_tutor["response"].lower() or "f = m * a" in newton_tutor["response"].lower() or "f_net" in newton_tutor["response"].lower()

    # 3. Custom Topic
    quantum_tutor = SocraticTutorAgent.answer_query(
        topic="Quantum Superposition",
        current_scene_title="Wavefunction State",
        current_scene_narration="A quantum system exists in multiple states simultaneously.",
        student_query="What is the core intuition of superposition?",
        learning_style="Visual"
    )
    assert "quantum superposition" in quantum_tutor["response"].lower()


def test_visual_engine_multi_topic():
    # 1. Photosynthesis (Biology)
    vis_photo = VisualEngine.generate_visual_for_scene(
        subject="Biology",
        topic="Photosynthesis",
        concept="Light-Dependent Reactions",
        narration="Chlorophyll absorbs photons in thylakoids."
    )
    assert "photosynthesis" in vis_photo.get("type", "") or "biology" in vis_photo.get("type", "")
    assert "CO₂" in vis_photo.get("formula", "") or "Glucose" in vis_photo.get("formula", "") or "Light" in vis_photo.get("formula", "")

    # 2. Newton's Laws (Physics)
    vis_newton = VisualEngine.generate_visual_for_scene(
        subject="Physics",
        topic="Newton's Second Law",
        concept="F = ma Dynamic Acceleration",
        narration="Calculating acceleration from net force."
    )
    assert "physics" in vis_newton.get("type", "") or "mechanics" in vis_newton.get("type", "")
    assert "F_net" in vis_newton.get("formula", "") or "a" in vis_newton.get("formula", "")

    # 3. Dynamic Topic
    vis_dynamic = VisualEngine.generate_visual_for_scene(
        subject="Chemistry",
        topic="Chemical Bonding",
        concept="Covalent Bonds",
        narration="Sharing electron pairs between atoms."
    )
    assert "chemical" in vis_dynamic.get("title", "").lower() or "bond" in vis_dynamic.get("title", "").lower()


def test_summary_agent_multi_topic():
    # Photosynthesis
    sum_photo = SummaryAgent.generate_summary(topic="Photosynthesis", subject="Biology")
    assert "Photosynthesis" in sum_photo["topic"]
    assert len(sum_photo["formulas"]) >= 1
    assert "C6H12O6" in sum_photo["formulas"][0]["formula_text"] or "CO2" in sum_photo["formulas"][0]["formula_text"]

    # Newton's Laws
    sum_newton = SummaryAgent.generate_summary(topic="Newton's Laws of Motion", subject="Physics")
    assert "Newton" in sum_newton["topic"]
    assert "F = m * a" in sum_newton["formulas"][0]["formula_text"] or "F" in sum_newton["formulas"][0]["formula_text"]
