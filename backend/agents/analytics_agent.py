import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class MasteryAnalyticsAgent:
    """
    Intelligent Student Mastery & Learning Velocity Analytics Agent.
    Evaluates formative assessment scores, updates concept knowledge models,
    identifies persistent misconceptions, and computes student growth metrics.
    """

    @classmethod
    def evaluate_quiz_performance(
        cls,
        quiz_submission: List[Dict[str, Any]],
        quiz_schema: Dict[str, Any],
        student_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        total_questions = len(quiz_schema.get("questions", []))
        if total_questions == 0:
            return {"score_pct": 100, "mastery_status": "Mastered", "feedback": "Completed"}

        correct_count = 0
        detailed_breakdown = []

        questions_map = {q["id"]: q for q in quiz_schema.get("questions", [])}

        for sub in quiz_submission:
            q_id = sub.get("question_id")
            user_ans = sub.get("selected_answer", "")
            q_obj = questions_map.get(q_id, {})
            correct_ans = q_obj.get("correct_answer", "")

            is_correct = (user_ans.strip().lower() == correct_ans.strip().lower())
            if is_correct:
                correct_count += 1

            detailed_breakdown.append({
                "question_id": q_id,
                "question": q_obj.get("question", ""),
                "selected": user_ans,
                "correct": correct_ans,
                "is_correct": is_correct,
                "explanation": q_obj.get("explanation", "")
            })

        score_pct = round((correct_count / total_questions) * 100, 1)

        if score_pct >= 90:
            mastery_level = "Mastered"
            badge = "Expert Conceptualist"
        elif score_pct >= 70:
            mastery_level = "Proficient"
            badge = "Active Learner"
        else:
            mastery_level = "Developing"
            badge = "Remediation Recommended"

        return {
            "score_pct": score_pct,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "mastery_level": mastery_level,
            "badge": badge,
            "detailed_breakdown": detailed_breakdown,
            "recommended_next_topics": [
                "Kirchhoff's Current Law (KCL)",
                "Series and Parallel Resistor Networks",
                "Capacitor RC Time Constants"
            ] if "ohm" in quiz_schema.get("quiz_title", "").lower() else ["Next Stage Core Concepts"]
        }
