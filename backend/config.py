import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
STORAGE_DIR = BASE_DIR / "storage"
AUDIO_DIR = STORAGE_DIR / "audio"
VIDEO_DIR = STORAGE_DIR / "video"
UPLOAD_DIR = STORAGE_DIR / "uploads"
ASSETS_DIR = BASE_DIR / "assets"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{STORAGE_DIR}/ai_teacher.db")

for path in [STORAGE_DIR, AUDIO_DIR, VIDEO_DIR, UPLOAD_DIR, ASSETS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Hardware & Engine Mode
ENGINE_MODE = os.getenv("ENGINE_MODE", "AUTO")  # "AUTO", "CPU", "LOW_GPU", "NORMAL_GPU"
DEFAULT_TTS_VOICE = os.getenv("DEFAULT_TTS_VOICE", "en-US-AriaNeural")
DEFAULT_TEACHER_AVATAR = os.getenv("DEFAULT_TEACHER_AVATAR", "prof_maya")

# Model API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# App settings
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
