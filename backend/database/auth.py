import base64
import hashlib
import hmac
import json
import secrets
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.config import APP_SECRET_KEY, SESSION_TTL_SECONDS
from backend.database.models import User, StudentProfile

PBKDF2_ITERATIONS = 210_000
TOKEN_VERSION = "v2"

def hash_password(password: str) -> str:
    if not password or len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(key).decode()}"

def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, iterations, salt_b64, key_b64 = encoded.split("$", 3)
        if scheme != "pbkdf2_sha256": return False
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(key_b64.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

def generate_session_token(user_id: str) -> str:
    payload = {"v": TOKEN_VERSION, "sub": user_id, "iat": int(datetime.now(timezone.utc).timestamp()), "exp": int(datetime.now(timezone.utc).timestamp()) + SESSION_TTL_SECONDS, "jti": secrets.token_hex(12)}
    body = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    sig = _b64(hmac.new(APP_SECRET_KEY.encode(), body.encode(), hashlib.sha256).digest())
    return f"usr_tok_{body}.{sig}"

def verify_session_token(token: str) -> Optional[str]:
    try:
        token = token.removeprefix("usr_tok_")
        body, sig = token.split(".", 1)
        expected = _b64(hmac.new(APP_SECRET_KEY.encode(), body.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected): return None
        payload = json.loads(_unb64(body))
        now = int(datetime.now(timezone.utc).timestamp())
        if payload.get("v") != TOKEN_VERSION or payload.get("exp", 0) <= now: return None
        sub = payload.get("sub")
        return sub if isinstance(sub, str) and sub else None
    except Exception:
        return None

def register_user(db: Session, username: str, email: Optional[str] = None, password: Optional[str] = None, full_name: str = "", grade_level: str = "Beginner", learning_style: str = "Visual", learning_goal: str = "Master core STEM concepts", avatar_url: str = "avatar_1") -> Tuple[Optional[User], Optional[str]]:
    username = username.strip()
    email = email.strip().lower() if email else None
    if len(username) < 3 or len(username) > 64:
        return None, "Username must be between 3 and 64 characters"
    if not username.replace("_", "").replace("-", "").isalnum():
        return None, "Username may contain letters, numbers, underscores and hyphens only"
    if not password or len(password) < 8:
        return None, "Password must contain at least 8 characters"
    existing = db.query(User).filter((User.username == username) | ((User.email == email) if email else (User.id == "__never__"))).first()
    if existing:
        return None, "Username or email is already registered"
    user = User(id=f"usr_{uuid.uuid4().hex[:12]}", username=username, email=email, hashed_password=hash_password(password), full_name=(full_name or username).strip(), avatar_url=avatar_url or "avatar_1", bookmarks_json="[]")
    db.add(user)
    db.flush()
    db.add(StudentProfile(user_id=user.id, grade_level=grade_level, learning_style=learning_style, learning_goal=learning_goal))
    db.commit()
    db.refresh(user)
    return user, None

def authenticate_user(db: Session, username_or_email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    value = username_or_email.strip()
    user = db.query(User).filter((User.username == value) | (User.email == value.lower())).first()
    if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
        return None, "Invalid username/email or password"
    return user, None

def format_user_profile(user: User) -> Dict[str, Any]:
    profile = user.profile
    try: bookmarks = json.loads(user.bookmarks_json or "[]")
    except Exception: bookmarks = []
    try: mastery = json.loads(profile.mastery_scores or "{}") if profile else {}
    except Exception: mastery = {}
    try: misconceptions = json.loads(profile.misconceptions_log or "[]") if profile else []
    except Exception: misconceptions = []
    return {"id": user.id, "username": user.username, "email": user.email, "full_name": user.full_name, "avatar_url": user.avatar_url, "bookmarks": bookmarks, "profile": {"grade_level": profile.grade_level if profile else "Beginner", "learning_style": profile.learning_style if profile else "Visual", "learning_goal": profile.learning_goal if profile else "Master core STEM concepts", "mastery_scores": mastery, "total_lessons_completed": profile.total_lessons_completed if profile else 0, "total_study_minutes": profile.total_study_minutes if profile else 0, "recent_misconceptions": misconceptions[-10:]}}
