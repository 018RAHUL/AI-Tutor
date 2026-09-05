import json
from datetime import datetime, timezone
from sqlalchemy import (
    Index,
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(255), default="")
    avatar_url = Column(String(512), default="avatar_1")
    bookmarks_json = Column(Text, default="[]")  # JSON list of bookmarked lesson IDs
    created_at = Column(DateTime, default=get_utc_now)

    profile = relationship("StudentProfile", back_populates="user", uselist=False)
    lessons = relationship("Lesson", back_populates="user")
    notes = relationship("StudyNote", back_populates="user")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.id"), unique=True)
    grade_level = Column(String(64), default="Beginner")  # Beginner, Intermediate, Advanced
    learning_style = Column(String(64), default="Visual")  # Simple, Visual, Practical, Technical, Socratic
    learning_goal = Column(String(255), default="Master core STEM concepts")
    mastery_scores = Column(Text, default="{}")  # JSON map of concept -> score (0.0 - 1.0)
    misconceptions_log = Column(Text, default="[]")  # JSON list of past misconceptions & status
    total_lessons_completed = Column(Integer, default=0)
    total_study_minutes = Column(Integer, default=0)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    user = relationship("User", back_populates="profile")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(64), primary_key=True)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=True)
    topic = Column(String(255), nullable=False)
    subject = Column(String(128), default="Physics")
    student_level = Column(String(64), default="Beginner")
    teaching_style = Column(String(64), default="Visual")
    duration_target = Column(String(64), default="20 min")  # "5 min", "20 min", "60 min", "7 days"
    status = Column(String(64), default="created")  # created, planning, prepared, ready, in_progress, completed
    total_scenes = Column(Integer, default=0)
    estimated_duration_sec = Column(Float, default=180.0)
    source_type = Column(String(64), default="topic")  # topic or document
    source_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    
    lesson_plan_json = Column(Text, nullable=True)
    assessment_json = Column(Text, nullable=True)
    summary_json = Column(Text, nullable=True)  # Executive summary, formulas, flashcards, takeaways

    user = relationship("User", back_populates="lessons")
    scenes = relationship("Scene", back_populates="lesson", order_by="Scene.order_index")
    interactions = relationship("Interaction", back_populates="lesson")


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(String(64), primary_key=True)
    lesson_id = Column(String(64), ForeignKey("lessons.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    chapter_title = Column(String(255), default="Introduction")
    concept = Column(String(255), nullable=False)
    learning_objective = Column(Text, nullable=True)
    narration = Column(Text, nullable=False)
    duration_sec = Column(Float, default=15.0)
    
    visual_type = Column(String(64), nullable=False)  # circuit_animation, math_equation, graph, code_trace, analogy_diagram, etc.
    visual_description = Column(Text, nullable=True)
    visual_data_json = Column(Text, default="{}")
    animation_steps_json = Column(Text, default="[]")
    
    avatar_state = Column(String(64), default="SPEAKING")  # IDLE, SPEAKING, EXPLAINING, QUESTIONING, LISTENING, THINKING, CORRECT, MISCONCEPTION, RE_EXPLAINING
    subtitle = Column(Text, nullable=True)
    transition = Column(String(64), default="fade")
    audio_path = Column(String(512), nullable=True)
    video_clip_path = Column(String(512), nullable=True)
    
    is_interactive = Column(Boolean, default=False)
    interaction_type = Column(String(64), nullable=True)  # question_pause, checkpoint, slider
    question_text = Column(Text, nullable=True)
    question_options_json = Column(Text, nullable=True)
    expected_answer = Column(Text, nullable=True)
    is_adaptive = Column(Boolean, default=False)

    lesson = relationship("Lesson", back_populates="scenes")


Index("ix_lessons_user_created", Lesson.user_id, Lesson.created_at)

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String(64), primary_key=True)
    lesson_id = Column(String(64), ForeignKey("lessons.id"), nullable=False)
    scene_id = Column(String(64), ForeignKey("scenes.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    student_response = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    confidence_score = Column(Float, default=0.0)
    misconception_detected = Column(String(255), nullable=True)
    explanation_feedback = Column(Text, nullable=True)
    adaptation_strategy = Column(String(128), nullable=True)
    timestamp = Column(DateTime, default=get_utc_now)

    lesson = relationship("Lesson", back_populates="interactions")


Index("ix_interactions_lesson_timestamp", Interaction.lesson_id, Interaction.timestamp)

class StudyNote(Base):
    __tablename__ = "study_notes"

    id = Column(String(64), primary_key=True)
    user_id = Column(String(64), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String(64), ForeignKey("lessons.id"), nullable=True)
    topic = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    user = relationship("User", back_populates="notes")


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(String(64), primary_key=True)
    topic = Column(String(255), nullable=False)
    domain = Column(String(128), default="General")
    nodes_json = Column(Text, default="[]")  # Roadmap nodes
    edges_json = Column(Text, default="[]")  # Prerequisite links
    created_at = Column(DateTime, default=get_utc_now)
