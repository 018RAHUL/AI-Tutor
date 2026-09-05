import hashlib
import hmac
import secrets
import json
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from backend.database.models import User, StudentProfile

# Password hashing with PBKDF2-HMAC-SHA256
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    if not hashed or "$" not in hashed:
        return False
    salt, key_hex = hashed.split("$", 1)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    )
    return hmac.compare_digest(key.hex(), key_hex)

def generate_session_token(user_id: str) -> str:
    random_part = secrets.token_urlsafe(32)
    return f"usr_tok_{user_id}_{random_part}"

def register_user(
    db: Session,
    username: str,
    email: Optional[str] = None,
    password: Optional[str] = None,
    full_name: str = "",
    grade_level: str = "Beginner",
    learning_style: str = "Visual",
    learning_goal: str = "Master core STEM concepts",
    avatar_url: str = "avatar_1"
) -> Tuple[Optional[User], Optional[str]]:
    # Check if username or email already exists
    existing = db.query(User).filter(
        (User.username == username) | (User.email == email if email else False)
    ).first()
    if existing:
        if existing.username == username:
            return None, "Username already taken"
        if email and existing.email == email:
            return None, "Email address already registered"

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    hashed_pwd = hash_password(password) if password else None

    user = User(
        id=user_id,
        username=username.strip(),
        email=email.strip().lower() if email else None,
        hashed_password=hashed_pwd,
        full_name=full_name.strip() or username,
        avatar_url=avatar_url or "avatar_1",
        bookmarks_json="[]"
    )
    db.add(user)

    profile = StudentProfile(
        user_id=user_id,
        grade_level=grade_level,
        learning_style=learning_style,
        learning_goal=learning_goal,
        mastery_scores="{}",
        misconceptions_log="[]",
        total_lessons_completed=0,
        total_study_minutes=0
    )
    db.add(profile)
    db.commit()
    db.refresh(user)
    return user, None

def authenticate_user(
    db: Session,
    username_or_email: str,
    password: str
) -> Tuple[Optional[User], Optional[str]]:
    identifier = username_or_email.strip()
    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier.lower())
    ).first()
    if not user:
        return None, "Invalid username/email or password"

    if user.hashed_password:
        if not verify_password(password, user.hashed_password):
            return None, "Invalid username/email or password"
    return user, None

def format_user_profile(user: User) -> Dict[str, Any]:
    prof = user.profile
    bookmarks = []
    try:
        bookmarks = json.loads(user.bookmarks_json or "[]")
    except Exception:
        bookmarks = []

    mastery = {}
    misconceptions = []
    if prof:
        try:
            mastery = json.loads(prof.mastery_scores or "{}")
        except Exception:
            mastery = {}
        try:
            misconceptions = json.loads(prof.misconceptions_log or "[]")
        except Exception:
            misconceptions = []

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name or user.username,
        "avatar_url": user.avatar_url or "avatar_1",
        "bookmarks": bookmarks,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "profile": {
            "grade_level": prof.grade_level if prof else "Beginner",
            "learning_style": prof.learning_style if prof else "Visual",
            "learning_goal": prof.learning_goal if prof else "Master core STEM concepts",
            "mastery_scores": mastery,
            "misconceptions_log": misconceptions,
            "total_lessons_completed": prof.total_lessons_completed if prof else 0,
            "total_study_minutes": prof.total_study_minutes if prof else 0
        }
    }
