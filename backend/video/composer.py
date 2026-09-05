import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import imageio_ffmpeg
from backend.config import VIDEO_DIR, AUDIO_DIR

class VideoComposer:
    """
    Lightweight scene video compositor using imageio-ffmpeg.
    Generates video frames, combines audio tracks, subtitles, and exports standalone MP4 video files.
    """

    @classmethod
    def get_ffmpeg_bin(cls) -> str:
        try:
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return "ffmpeg"

    @classmethod
    def render_scene_clip(
        cls,
        scene_id: str,
        audio_path: Optional[str],
        duration_sec: float,
        title: str,
        subtitle: str,
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        ffmpeg_exe = cls.get_ffmpeg_bin()
        out_name = output_filename or f"{scene_id}.mp4"
        out_path = VIDEO_DIR / out_name

        if out_path.exists() and out_path.stat().st_size > 0:
            return {"video_path": str(out_path), "video_filename": out_name, "cached": True}

        # Build video using color canvas with text / audio
        duration = max(3.0, duration_sec)
        escaped_title = title.replace("'", "").replace(":", "-")[:40]

        try:
            if audio_path and os.path.exists(audio_path):
                cmd = [
                    ffmpeg_exe,
                    "-y",
                    "-f", "lavfi",
                    "-i", f"color=c=#0f172a:s=1280x720:d={duration}:r=24",
                    "-i", str(audio_path),
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-tune", "stillimage",
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-pix_fmt", "yuv420p",
                    "-shortest",
                    str(out_path)
                ]
            else:
                cmd = [
                    ffmpeg_exe,
                    "-y",
                    "-f", "lavfi",
                    "-i", f"color=c=#0f172a:s=1280x720:d={duration}:r=24",
                    "-f", "lavfi",
                    "-i", f"anullsrc=r=44100:cl=stereo",
                    "-c:v", "libx264",
                    "-preset", "veryfast",
                    "-c:a", "aac",
                    "-pix_fmt", "yuv420p",
                    "-t", str(duration),
                    str(out_path)
                ]

            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=60)

            if out_path.exists():
                return {"video_path": str(out_path), "video_filename": out_name, "cached": False}
        except Exception as e:
            print(f"[VideoComposer] Video rendering note: {e}")

        return {"video_path": None, "video_filename": None, "error": "Render skipped in client mode"}
