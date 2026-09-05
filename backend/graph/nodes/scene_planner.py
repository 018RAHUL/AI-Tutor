import datetime
import uuid
from typing import Dict, Any, List
from backend.graph.state import TeachingSessionState
from backend.models.tts_provider import TTSProvider

def scene_planner_node(state: TeachingSessionState) -> Dict[str, Any]:
    """
    Fan-In node: combines parallel preparation outputs (explanations, visual plans,
    examples, questions, assessment) into synchronized, executable scenes.
    Triggers TTS voice synthesis per scene.
    """
    lesson_id = state.get("lesson_id", str(uuid.uuid4()))
    topic = state.get("topic", "Ohm's Law")
    explanations = state.get("explanations", [])
    visual_plans = state.get("visual_plans", [])
    questions = state.get("questions", [])

    scenes: List[Dict[str, Any]] = []
    total_duration = 0.0

    avatar_states = ["SPEAKING", "EXPLAINING", "EXPLAINING", "EXPLAINING", "QUESTIONING", "CORRECT"]

    for idx, exp in enumerate(explanations):
        vis = visual_plans[idx] if idx < len(visual_plans) else {}
        narration = exp.get("script", "")
        
        # Audio synthesis with Edge-TTS
        tts_res = TTSProvider.synthesize(narration)
        duration_sec = tts_res.get("duration_sec", exp.get("target_duration_sec", 25.0))
        audio_filename = tts_res.get("audio_filename")
        total_duration += duration_sec

        is_question_scene = (idx == 4) or ("checkpoint" in exp.get("chapter_id", "").lower())
        q_data = questions[0] if (is_question_scene and questions) else None

        scene_obj = {
            "id": f"scene_{lesson_id}_{idx+1}",
            "order_index": idx + 1,
            "chapter_title": exp.get("chapter_title", f"Chapter {idx+1}"),
            "concept": exp.get("chapter_title", topic),
            "learning_objective": f"Understand {exp.get('chapter_title', topic)}",
            "narration": narration,
            "duration_sec": duration_sec,
            "visual_type": vis.get("visual_type", "diagram"),
            "visual_payload": vis.get("visual_payload", {}),
            "formula": vis.get("visual_payload", {}).get("formula"),
            "topic": topic,
            "subject": state.get("subject", "STEM"),
            "animation_steps": vis.get("animation_triggers", []),
            "avatar_state": avatar_states[min(idx, len(avatar_states)-1)] if not is_question_scene else "QUESTIONING",
            "subtitle": narration,
            "transition": "slide_left" if idx > 0 else "fade_in",
            "audio_url": f"/api/media/{audio_filename}" if audio_filename else None,
            "audio_path": tts_res.get("audio_path"),
            "is_interactive": is_question_scene,
            "interaction_type": "question_pause" if is_question_scene else None,
            "question_text": q_data.get("question") if q_data else None,
            "question_options": q_data.get("options") if q_data else None,
            "expected_answer": q_data.get("expected_answer") if q_data else None,
            "has_simulation": vis.get("visual_payload", {}).get("has_simulation", False),
            "is_adaptive": False
        }
        scenes.append(scene_obj)

    # Trigger dedicated AI Video Generation Agent to render MP4 clips
    try:
        from backend.agents.video_agent import VideoGenerationAgent
        scenes = VideoGenerationAgent.generate_videos_for_scenes(scenes)
    except Exception as e:
        print(f"[ScenePlanner] Video agent warning: {e}")

    # Generate comprehensive summary and study materials via SummaryAgent
    summary_data = {}
    try:
        from backend.agents.summary_agent import SummaryAgent
        summary_data = SummaryAgent.generate_summary(
            topic=topic,
            subject=state.get("subject", "Physics"),
            student_level=state.get("student_level", "Beginner"),
            scenes=scenes,
            lesson_plan=state.get("lesson_plan", {})
        )
    except Exception as e:
        print(f"[ScenePlanner] Summary agent warning: {e}")

    logs = state.get("observability_logs", [])
    logs.append({
        "node": "scene_planner",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detail": f"Fan-In complete: Created {len(scenes)} synchronized scenes and generated comprehensive Summary Hub materials. Total video duration: {round(total_duration, 1)} seconds."
    })

    return {
        "scenes": scenes,
        "summary": summary_data,
        "current_scene_index": 0,
        "status": "ready",
        "observability_logs": logs
    }
