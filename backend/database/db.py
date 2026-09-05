import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.config import DATABASE_URL
from backend.database.models import Base, User, StudentProfile

# SQLite specific config for thread safety
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Safe SQLite schema migration for columns added in v2
    with engine.connect() as conn:
        for col_name, col_type in [
            ("email", "VARCHAR(255)"),
            ("hashed_password", "VARCHAR(255)"),
            ("full_name", "VARCHAR(255)"),
            ("avatar_url", "VARCHAR(512)"),
            ("bookmarks_json", "TEXT")
        ]:
            try:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                conn.commit()
            except Exception:
                pass
        
        for col_name, col_type in [
            ("learning_goal", "VARCHAR(255)"),
            ("total_study_minutes", "INTEGER DEFAULT 0")
        ]:
            try:
                conn.execute(text(f"ALTER TABLE student_profiles ADD COLUMN {col_name} {col_type}"))
                conn.commit()
            except Exception:
                pass

        try:
            conn.execute(text("ALTER TABLE lessons ADD COLUMN summary_json TEXT"))
            conn.commit()
        except Exception:
            pass

    # Ensure default demo user exists
    with get_db() as db:
        user = db.query(User).filter_by(id="default_student").first()
        if not user:
            user = User(
                id="default_student",
                username="default_student",
                email="scholar@aiteacher.io",
                full_name="Alex Learner",
                avatar_url="avatar_1",
                bookmarks_json="[]"
            )
            db.add(user)
            profile = StudentProfile(
                user_id="default_student",
                grade_level="Beginner",
                learning_style="Visual",
                learning_goal="Master core STEM concepts",
                mastery_scores='{"physics.circuits": 0.88, "math.algebra": 0.75}',
                misconceptions_log='[]',
                total_lessons_completed=6,
                total_study_minutes=45
            )
            db.add(profile)
            db.commit()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
