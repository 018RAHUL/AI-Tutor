import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List
from backend.video.renderer import VideoRenderer

class VideoGenerationAgent:
    """
    Dedicated AI Video Generation Agent.
    Generates high-definition MP4 educational video clips for each scene
    in parallel, embedding audio and animations.
    """

    @classmethod
    def generate_videos_for_scenes(cls, scenes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for scene in scenes:
                f = executor.submit(
                    VideoRenderer.generate_scene_mp4,
                    scene_id=scene.get("id", "scene_vid"),
                    scene_type=scene.get("visual_type", "circuit_intro"),
                    chapter_title=scene.get("chapter_title", "Concept Lesson"),
                    narration=scene.get("narration", ""),
                    audio_path=scene.get("audio_path"),
                    duration_sec=scene.get("duration_sec", 25.0),
                    topic=scene.get("topic", "Core STEM Concept"),
                    subject=scene.get("subject", "STEM"),
                    visual_payload=scene.get("visual_payload", {}),
                    formula=scene.get("formula")
                )
                futures.append((scene, f))

            for scene, fut in futures:
                try:
                    res = fut.result()
                    if res.get("video_url"):
                        scene["video_url"] = res["video_url"]
                        scene["video_path"] = res.get("video_path")
                except Exception as e:
                    print(f"[VideoGenerationAgent] Video generation warning: {e}")

        return scenes
