import re
from typing import Dict, Any, List, Optional
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType

class SocraticTutorAgent:
    """
    Real-time Conversational Socratic AI Tutor Agent.
    Engages students in guided Socratic inquiry, provides tiered hints without spoiling answers,
    and breaks down complex visual scene concepts on demand for ANY topic.
    """

    @classmethod
    def answer_query(
        cls,
        topic: str,
        current_scene_title: str,
        current_scene_narration: str,
        student_query: str,
        learning_style: str = "Visual",
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        clean_topic = topic.strip() or "Core STEM Concept"

        system_prompt = (
            f"You are an inspiring, pedagogical AI Socratic Tutor helping a student learn '{clean_topic}'. "
            f"Current Chapter/Scene: '{current_scene_title}'. "
            f"Scene Context / Narration: '{current_scene_narration}'. "
            f"Student Learning Style: '{learning_style}'. "
            f"Guide the student using Socratic inquiry, intuitive mental models, formulas, and tiered hints. "
            f"Never give away complete quiz solutions directly if the student is asking for a hint; guide their discovery."
        )

        user_prompt = (
            f"Topic: '{clean_topic}'\n"
            f"Scene: '{current_scene_title}'\n"
            f"Student Query: '{student_query}'\n"
            f"Provide a comprehensive, accurate Socratic response strictly for '{clean_topic}'."
        )

        schema_desc = "{'response': str, 'actionable_suggestion': str, 'formula_ref': str, 'avatar_reaction': str}"

        try:
            res = LLMProvider.generate_json(
                task_type=TaskType.SOCRATIC_TUTOR,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                schema_desc=schema_desc
            )
            if isinstance(res, dict) and "response" in res:
                return {
                    "response": res.get("response", ""),
                    "actionable_suggestion": res.get("actionable_suggestion", "Review the core governing principle."),
                    "formula_ref": res.get("formula_ref", f"Governing principle of {clean_topic}"),
                    "avatar_reaction": res.get("avatar_reaction", "EXPLAINING")
                }
        except Exception as e:
            print(f"[SocraticTutorAgent] Generation note: {e}")

        # Grounded fallback using topic knowledge graph
        kg = LLMProvider.get_topic_knowledge_graph(clean_topic)
        formula = kg.get("formula", f"Principles of {clean_topic}")
        intuition = kg.get("core_intuition", f"Understand the core driving mechanism of {clean_topic}.")

        return {
            "response": (
                f"🧠 **AI Tutor on {clean_topic}:**\n\n"
                f"In this section (*{current_scene_title}*), our focus is on understanding **{clean_topic}**.\n\n"
                f"- **Governing Rule:** $${formula}$$\n"
                f"- **Key Intuition:** {intuition}\n\n"
                f"When addressing: \"{student_query.strip()}\", trace how changing the underlying parameters influences the result."
            ),
            "actionable_suggestion": f"Apply the governing principle: {formula}",
            "formula_ref": formula,
            "avatar_reaction": "EXPLAINING"
        }

