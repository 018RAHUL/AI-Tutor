import os
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from backend.config import AUDIO_DIR, DEFAULT_TTS_VOICE

class TTSProvider:
    """
    High-fidelity Text-to-Speech provider powered by Edge-TTS.
    Generates audio files, extracts approximate viseme/timing cues for lip-sync,
    and caches generated speech to avoid repeated generation.
    """

    @classmethod
    def get_cache_path(cls, text: str, voice: str) -> Path:
        content_hash = hashlib.sha256(f"{voice}_{text.strip()}".encode("utf-8")).hexdigest()
        return AUDIO_DIR / f"{content_hash}.mp3"

    @classmethod
    async def synthesize_async(cls, text: str, voice: Optional[str] = None) -> Dict[str, Any]:
        voice = voice or DEFAULT_TTS_VOICE
        cached_file = cls.get_cache_path(text, voice)
        
        # Approximate speech duration calculation (avg 140 words per minute -> ~2.3 words/sec)
        words = text.split()
        estimated_duration = max(3.0, round(len(words) / 2.3, 1))

        if cached_file.exists() and cached_file.stat().st_size > 0:
            return {
                "audio_path": str(cached_file),
                "audio_filename": cached_file.name,
                "duration_sec": estimated_duration,
                "cached": True
            }

        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice)
            await asyncio.wait_for(communicate.save(str(cached_file)), timeout=25.0)
            
            # If successfully saved
            if cached_file.exists() and cached_file.stat().st_size > 500:
                return {
                    "audio_path": str(cached_file),
                    "audio_filename": cached_file.name,
                    "duration_sec": estimated_duration,
                    "cached": False
                }
        except Exception as e:
            print(f"[TTSProvider] Edge-TTS warning ({e}). Using robust duration model.")

        return {
            "audio_path": None,
            "audio_filename": None,
            "duration_sec": estimated_duration,
            "cached": False,
            "error": "TTS offline fallback"
        }

    @classmethod
    def synthesize(cls, text: str, voice: Optional[str] = None) -> Dict[str, Any]:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(cls.synthesize_async(text, voice))
            else:
                return asyncio.run(cls.synthesize_async(text, voice))
        except Exception:
            return asyncio.run(cls.synthesize_async(text, voice))
