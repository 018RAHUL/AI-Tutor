import datetime
import uuid
from typing import Dict, Any, List
from backend.graph.state import TeachingSessionState
from backend.models.llm_provider import LLMProvider
from backend.models.tts_provider import TTSProvider
from backend.models.router import TaskType
from backend.visuals.circuit_visuals import CircuitVisualGenerator

def adaptive_router_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Decides routing logic based on student understanding.
    If a misconception is detected, synthesizes a brand-new adaptive visual scene
    with targeted remediation, different physical analogy, and dynamic visual state.
    """
    eval_res = state.get("evaluation_result", {})
    is_correct = eval_res.get("is_correct", False)
    topic = state.get("topic", "Ohm's Law")
    lesson_id = state.get("lesson_id", str(uuid.uuid4()))
    
    scenes = list(state.get("scenes", []))
    adaptive_scenes = list(state.get("adaptive_scenes", []))
    logs = state.get("observability_logs", [])

    if not is_correct:
        logs.append({
            "node": "adaptive_router",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "detail": "Routing to ADAPTIVE RE-TEACHING: Generating remediation visual and analogy scene."
        })

        system_prompt = "You are an adaptive pedagogical specialist. Create a fresh explanation with a concrete mechanical analogy and simplified visual."
        user_prompt = f"Topic: {topic}. Misconception: {eval_res.get('detected_misconception')}. Create an adaptive scene."

        adapt_data = LLMProvider.generate_json(
            task_type=TaskType.ADAPTATION,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema_desc="{'adaptive_scene': dict}"
        )
        
        raw_scene = adapt_data.get("adaptive_scene", {})
        narration = raw_scene.get("narration", "Let's revisit this using a direct visual example: higher resistance narrows the path, reducing the flow of current.")
        
        # Synthesize voice for the adaptive scene
        tts_res = TTSProvider.synthesize(narration)
        duration_sec = tts_res.get("duration_sec", 25.0)
        audio_filename = tts_res.get("audio_filename")

        adaptive_scene_obj = {
            "id": f"scene_{lesson_id}_adaptive_{len(adaptive_scenes)+1}",
            "order_index": 999,  # inserted dynamically
            "chapter_title": raw_scene.get("chapter_title", "Adaptive Clarification"),
            "concept": raw_scene.get("concept", "Resistance vs Current Opposition"),
            "learning_objective": "Directly resolve the inverse proportionality misconception",
            "narration": narration,
            "duration_sec": duration_sec,
            "visual_type": "circuit_remediation",
            "visual_payload": CircuitVisualGenerator.get_remediation_visual(),
            "animation_steps": ["highlight_bottleneck", "compare_current_values"],
            "avatar_state": "RE_EXPLAINING",
            "subtitle": narration,
            "transition": "fade",
            "audio_url": f"/api/media/{audio_filename}" if audio_filename else None,
            "audio_path": tts_res.get("audio_path"),
            "is_interactive": True,
            "interaction_type": "question_pause",
            "question_text": raw_scene.get("question", "If we reduce resistance by opening the valve, what happens to current?"),
            "question_options": raw_scene.get("options", ["Current increases", "Current decreases", "Current stays unchanged"]),
            "expected_answer": raw_scene.get("expected_answer", "Current increases"),
            "is_adaptive": True
        }
        
        adaptive_scenes.append(adaptive_scene_obj)

    else:
        logs.append({
            "node": "adaptive_router",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "detail": "Routing to SUCCESS CONTINUATION: Student demonstrated clear comprehension."
        })

    return {
        "adaptive_scenes": adaptive_scenes,
        "observability_logs": logs
    }
