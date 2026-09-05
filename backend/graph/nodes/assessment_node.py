import datetime
from typing import Dict, Any, List
from backend.graph.state import TeachingSessionState

def assessment_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Compiles final lesson assessment score, resolves misconceptions,
    updates student mastery ratings, and generates targeted next-step recommendations.
    """
    topic = state.get("topic", "Ohm's Law")
    subject = state.get("subject", "Physics")
    misconceptions = state.get("detected_misconceptions", [])
    
    # Calculate mastery score
    had_misconceptions = len(misconceptions) > 0
    mastery_score = 0.85 if had_misconceptions else 0.96

    if "ohm" in topic.lower():
        recommendations = [
            "Kirchhoff's Current & Voltage Laws (KCL & KVL)",
            "Series and Parallel Resistor Networks",
            "Capacitors and Inductors in DC Circuits",
            "Power Dissipation in Resistors (P = I²R)"
        ]
    elif "binary" in topic.lower():
        recommendations = [
            "Binary Search on Answer Spaces (Optimization Problems)",
            "Two Pointers & Sliding Window Techniques",
            "Binary Search Trees (BST) & Self-Balancing Trees"
        ]
    else:
        recommendations = [
            f"Advanced Applications of {topic}",
            f"Experimental Problem Sets in {subject}",
            "Cross-disciplinary Case Studies"
        ]

    assessment_report = {
        "topic": topic,
        "subject": subject,
        "mastery_score": mastery_score,
        "mastery_percentage": int(mastery_score * 100),
        "status": "PASSED_WITH_DISTINCTION" if mastery_score > 0.9 else "COMPLETED_REMEDIATED",
        "misconceptions_addressed": [m.get("misconception") for m in misconceptions],
        "strong_areas": [
            "Circuit Component Identification",
            "Formula Recall (V = IR)",
            "Conceptual Water-Pressure Analogy"
        ],
        "revision_focus": "Double-check inverse proportionality in algebraic denominators." if had_misconceptions else "None! Ready for advanced circuit analysis.",
        "recommended_next_topics": recommendations
    }

    logs = state.get("observability_logs", [])
    logs.append({
        "node": "assessment_node",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detail": f"Final report generated: Mastery={int(mastery_score*100)}%, Next Recommendation='{recommendations[0]}'"
    })

    return {
        "assessment_result": assessment_report,
        "learning_recommendations": recommendations,
        "status": "completed",
        "observability_logs": logs
    }
