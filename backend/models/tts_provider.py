import os
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

from backend.config import AUDIO_DIR, DEFAULT_TTS_VOICE


class TTSProvider:
    """
    Edge-TTS based speech generation.

    Features:
    - Uses Microsoft Edge neural voices through edge-tts
    - Caches generated MP3 files
    - Retries temporary network/TTS failures
    - Uses a generous timeout for cloud TTS
    - Never treats an incomplete audio file as valid
    """

    DEFAULT_TIMEOUT = float(os.getenv("TTS_TIMEOUT_SECONDS", "90"))
    MAX_RETRIES = int(os.getenv("TTS_RETRIES", "3"))

    @classmethod
    def get_cache_path(cls, text: str, voice: str) -> Path:
        content_hash = hashlib.sha256(
            f"{voice}_{text.strip()}".encode("utf-8")
        ).hexdigest()

        AUDIO_DIR.mkdir(parents=True, exist_ok=True)

        return AUDIO_DIR / f"{content_hash}.mp3"

    @classmethod
    async def synthesize_async(
        cls,
        text: str,
        voice: Optional[str] = None
    ) -> Dict[str, Any]:

        text = (text or "").strip()
        voice = voice or DEFAULT_TTS_VOICE

        if not text:
            return {
                "audio_path": None,
                "audio_filename": None,
                "duration_sec": 3.0,
                "cached": False,
                "error": "Empty narration text"
            }

        cached_file = cls.get_cache_path(text, voice)

        # Approximate duration.
        words = text.split()
        estimated_duration = max(
            3.0,
            round(len(words) / 2.3, 1)
        )

        # Use an existing valid MP3.
        if cached_file.exists() and cached_file.stat().st_size > 5000:
            print(
                f"[TTSProvider] Using cached audio: "
                f"{cached_file.name} ({cached_file.stat().st_size} bytes)"
            )

            return {
                "audio_path": str(cached_file),
                "audio_filename": cached_file.name,
                "duration_sec": estimated_duration,
                "cached": True
            }

        last_error = None

        for attempt in range(1, cls.MAX_RETRIES + 1):

            temp_file = cached_file.with_suffix(
                f".attempt{attempt}.tmp"
            )

            try:
                # Remove incomplete files from previous attempts.
                if temp_file.exists():
                    temp_file.unlink()

                print(
                    f"[TTSProvider] Generating speech "
                    f"(attempt {attempt}/{cls.MAX_RETRIES}) "
                    f"voice={voice}"
                )

                import edge_tts

                communicate = edge_tts.Communicate(
                    text,
                    voice
                )

                await asyncio.wait_for(
                    communicate.save(str(temp_file)),
                    timeout=cls.DEFAULT_TIMEOUT
                )

                # Verify that actual audio was produced.
                if (
                    temp_file.exists()
                    and temp_file.stat().st_size > 5000
                ):
                    temp_file.replace(cached_file)

                    print(
                        f"[TTSProvider] TTS success: "
                        f"{cached_file.name} "
                        f"({cached_file.stat().st_size} bytes)"
                    )

                    return {
                        "audio_path": str(cached_file),
                        "audio_filename": cached_file.name,
                        "duration_sec": estimated_duration,
                        "cached": False
                    }

                raise RuntimeError(
                    "Edge-TTS produced an empty or incomplete audio file"
                )

            except Exception as e:
                last_error = e

                print(
                    f"[TTSProvider] TTS attempt "
                    f"{attempt}/{cls.MAX_RETRIES} failed: {e}"
                )

                if temp_file.exists():
                    try:
                        temp_file.unlink()
                    except Exception:
                        pass

                # Small delay before retry.
                if attempt < cls.MAX_RETRIES:
                    await asyncio.sleep(2 * attempt)

        # IMPORTANT:
        # Do not pretend TTS succeeded.
        print(
            f"[TTSProvider] TTS FAILED after "
            f"{cls.MAX_RETRIES} attempts: {last_error}"
        )

        return {
            "audio_path": None,
            "audio_filename": None,
            "duration_sec": estimated_duration,
            "cached": False,
            "error": f"TTS failed: {last_error}"
        }

    @classmethod
    def synthesize(
        cls,
        text: str,
        voice: Optional[str] = None
    ) -> Dict[str, Any]:

        try:
            return asyncio.run(
                cls.synthesize_async(text, voice)
            )

        except RuntimeError as e:
            # Handles environments where an event loop
            # is already running.
            if "asyncio.run()" in str(e):

                loop = asyncio.new_event_loop()

                try:
                    asyncio.set_event_loop(loop)

                    return loop.run_until_complete(
                        cls.synthesize_async(text, voice)
                    )

                finally:
                    loop.close()
                    asyncio.set_event_loop(None)

            raise