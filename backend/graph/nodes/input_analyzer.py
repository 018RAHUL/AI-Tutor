import datetime
from typing import Dict, Any
from backend.graph.state import TeachingSessionState
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType

def get_utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def input_analyzer_node(state: TeachingSessionState) -> Dict[str, Any]:
    topic = state.get("topic", "").strip()
    source_type = state.get("source_type", "topic")
    
    logs = state.get("observability_logs", [])
    logs.append({
        "node": "input_analyzer",
        "timestamp": get_utc_now_iso(),
        "detail": f"Analyzing request: topic='{topic}', source='{source_type}'"
    })

    # Subject classification
    topic_lower = topic.lower()
    subject = "General Science"
    if any(k in topic_lower for k in ["ohm", "circuit", "voltage", "current", "resistor", "newton", "gravity", "force", "velocity", "wave"]):
        subject = "Physics"
    elif any(k in topic_lower for k in ["quadratic", "algebra", "calculus", "derivative", "integral", "geometry", "matrix"]):
        subject = "Mathematics"
    elif any(k in topic_lower for k in ["binary search", "algorithm", "python", "data structure", "tree", "graph", "sort"]):
        subject = "Computer Science"
    elif any(k in topic_lower for k in ["cell", "photosynthesis", "dna", "genetics", "organ", "mitosis"]):
        subject = "Biology"
    elif any(k in topic_lower for k in ["molecule", "acid", "base", "chemical", "atom", "reaction", "periodic"]):
        subject = "Chemistry"

    return {
        "subject": subject,
        "observability_logs": logs
    }


def student_profiler_node(state: TeachingSessionState) -> Dict[str, Any]:
    student_level = state.get("student_level", "Beginner")
    teaching_style = state.get("teaching_style", "Visual")
    
    profile = {
        "level": student_level,
        "style": teaching_style,
        "pacing": "Deliberate and Visual" if student_level == "Beginner" else "Fast and Technical",
        "scaffolding_required": student_level in ("Beginner", "Intermediate"),
        "preferred_representations": ["diagrams", "animations", "worked_examples"]
    }

    logs = state.get("observability_logs", [])
    logs.append({
        "node": "student_profiler",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "detail": f"Profile calibrated: Level={student_level}, Style={teaching_style}"
    })

    return {
        "student_profile": profile,
        "observability_logs": logs
    }
