import os
import uuid
import json
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from pydantic import BaseModel

from backend.config import (
    STORAGE_DIR, AUDIO_DIR, VIDEO_DIR, UPLOAD_DIR,
    SERVER_HOST, SERVER_PORT, PROJECT_ROOT
)
from backend.database.db import init_db, get_db
from backend.database.models import User, StudentProfile, Lesson, Scene, Interaction, LearningPath, StudyNote
from backend.database.auth import (
    register_user, authenticate_user, generate_session_token, format_user_profile
)
from backend.graph.workflow import lesson_pipeline, interaction_pipeline
from backend.rag.parser import DocumentParser
from backend.rag.retriever import RAGRetriever
from backend.agents.summary_agent import SummaryAgent
from backend.agents.tutor_agent import SocraticTutorAgent
from backend.agents.analytics_agent import MasteryAnalyticsAgent
from backend.models.llm_provider import LLMProvider

# Global RAG Retriever instance
rag_retriever = RAGRetriever()

# Initialize DB
init_db()

app = FastAPI(
    title="AI Teacher — AI-Generated Visual Educational Tutor",
    description="Full Scene-Based Educational Video Generator, Adaptive AI Teacher & Multi-Agent Study Platform",
    version="2.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static media route for video and audio
app.mount("/api/media/video", StaticFiles(directory=str(VIDEO_DIR)), name="media_video")
app.mount("/api/media", StaticFiles(directory=str(AUDIO_DIR)), name="media_audio")

# Schemas
class RegisterRequest(BaseModel):
    username: str
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = ""
    grade_level: str = "Beginner"
    learning_style: str = "Visual"
    learning_goal: str = "Master core STEM concepts"
    avatar_url: str = "avatar_1"

class LoginRequest(BaseModel):
    username_or_email: str
    password: Optional[str] = None

class UpdateProfileRequest(BaseModel):
    user_id: str
    full_name: Optional[str] = None
    grade_level: Optional[str] = None
    learning_style: Optional[str] = None
    learning_goal: Optional[str] = None
    avatar_url: Optional[str] = None

class BookmarkRequest(BaseModel):
    user_id: str
    lesson_id: str

class CreateLessonRequest(BaseModel):
    topic: str
    student_level: str = "Beginner"
    teaching_style: str = "Visual"
    duration_target: str = "20 min"
    user_id: str = "default_student"
    source_type: str = "topic"
    api_key: Optional[str] = None
    model_provider: Optional[str] = "autonomous"

class SubmitAnswerRequest(BaseModel):
    scene_id: str
    question_text: str
    student_response: str
    user_id: str = "default_student"

class TutorAskRequest(BaseModel):
    student_query: str
    scene_title: Optional[str] = ""
    scene_narration: Optional[str] = ""
    learning_style: Optional[str] = "Visual"
    chat_history: Optional[List[Dict[str, str]]] = []

class SaveNoteRequest(BaseModel):
    user_id: str
    lesson_id: Optional[str] = None
    topic: str
    content: str
    tags: Optional[List[str]] = []

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz_submission: List[Dict[str, Any]]
    quiz_schema: Dict[str, Any]


# ==========================================
# Authentication & User Management Endpoints
# ==========================================

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    with get_db() as db:
        user, err = register_user(
            db=db,
            username=req.username,
            email=req.email,
            password=req.password,
            full_name=req.full_name or req.username,
            grade_level=req.grade_level,
            learning_style=req.learning_style,
            learning_goal=req.learning_goal,
            avatar_url=req.avatar_url
        )
        if err:
            raise HTTPException(status_code=400, detail=err)

        token = generate_session_token(user.id)
        return {
            "token": token,
            "user": format_user_profile(user),
            "message": "Account created successfully"
        }


@app.post("/api/auth/login")
def login(req: LoginRequest):
    with get_db() as db:
        user, err = authenticate_user(
            db=db,
            username_or_email=req.username_or_email,
            password=req.password or ""
        )
        if err or not user:
            raise HTTPException(status_code=401, detail=err or "Authentication failed")

        token = generate_session_token(user.id)
        return {
            "token": token,
            "user": format_user_profile(user),
            "message": "Logged in successfully"
        }


@app.get("/api/auth/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization token provided")
    
    # Token format: Bearer usr_tok_<user_id>_<rand> or usr_tok_<user_id>_<rand>
    raw_token = authorization.replace("Bearer ", "").strip()
    if not raw_token.startswith("usr_tok_"):
        raise HTTPException(status_code=401, detail="Invalid token format")

    parts = raw_token.split("_")
    if len(parts) < 4:
        raise HTTPException(status_code=401, detail="Invalid token structure")
    
    # usr_tok_usr_<hex>_<rand>
    user_id = f"{parts[2]}_{parts[3]}"
    
    with get_db() as db:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            # Fallback to default user if testing
            user = db.query(User).first()
            if not user:
                raise HTTPException(status_code=404, detail="User session not found")

        return {
            "user": format_user_profile(user)
        }


@app.put("/api/auth/profile")
def update_profile(req: UpdateProfileRequest):
    with get_db() as db:
        user = db.query(User).filter_by(id=req.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if req.full_name is not None:
            user.full_name = req.full_name
        if req.avatar_url is not None:
            user.avatar_url = req.avatar_url

        if user.profile:
            if req.grade_level:
                user.profile.grade_level = req.grade_level
            if req.learning_style:
                user.profile.learning_style = req.learning_style
            if req.learning_goal:
                user.profile.learning_goal = req.learning_goal

        db.commit()
        db.refresh(user)
        return {
            "user": format_user_profile(user),
            "message": "Profile updated successfully"
        }


@app.post("/api/auth/bookmark")
def toggle_bookmark(req: BookmarkRequest):
    with get_db() as db:
        user = db.query(User).filter_by(id=req.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            bookmarks = json.loads(user.bookmarks_json or "[]")
        except Exception:
            bookmarks = []

        if req.lesson_id in bookmarks:
            bookmarks.remove(req.lesson_id)
            is_bookmarked = False
        else:
            bookmarks.append(req.lesson_id)
            is_bookmarked = True

        user.bookmarks_json = json.dumps(bookmarks)
        db.commit()

        return {
            "is_bookmarked": is_bookmarked,
            "bookmarks": bookmarks
        }


# ==========================================
# Core Lesson & Agent Endpoints
# ==========================================

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Teacher Advanced Platform",
        "version": "2.0.0",
        "agents": ["ExplanationAgent", "VisualAgent", "ExamplesAgent", "QuestionsAgent", "AssessmentAgent", "SummaryAgent", "SocraticTutorAgent", "MasteryAnalyticsAgent", "VideoGenerationAgent"]
    }


@app.post("/api/lesson/create")
def create_lesson(req: CreateLessonRequest):
    lesson_id = f"lesson_{uuid.uuid4().hex[:10]}"
    
    # Configure custom LLM credentials if provided
    if req.api_key or req.model_provider:
        LLMProvider.set_session_credentials(req.api_key, req.model_provider)

    # Retrieve grounded context if RAG has documents
    rag_context = rag_retriever.retrieve(req.topic, top_k=3)

    initial_state = {
        "lesson_id": lesson_id,
        "user_id": req.user_id,
        "topic": req.topic,
        "subject": "Physics",
        "student_level": req.student_level,
        "teaching_style": req.teaching_style,
        "duration_target": req.duration_target,
        "source_type": req.source_type,
        "source_file": None,
        "rag_context": rag_context,
        "student_profile": {},
        "lesson_plan": {},
        "explanations": [],
        "visual_plans": [],
        "examples": [],
        "questions": [],
        "assessment_plan": {},
        "scenes": [],
        "current_scene_index": 0,
        "student_response": None,
        "evaluation_result": None,
        "detected_misconceptions": [],
        "adaptive_scenes": [],
        "summary": {},
        "assessment_result": None,
        "learning_recommendations": [],
        "status": "in_progress",
        "error": None,
        "observability_logs": []
    }

    # Execute LangGraph Pipeline
    final_state = lesson_pipeline.invoke(initial_state)

    summary_data = final_state.get("summary") or SummaryAgent.generate_summary(
        topic=req.topic,
        subject=final_state.get("subject", "Physics"),
        student_level=req.student_level,
        scenes=final_state.get("scenes", []),
        lesson_plan=final_state.get("lesson_plan", {})
    )

    # Persist in SQLite
    with get_db() as db:
        # Check if user exists or default
        user = db.query(User).filter_by(id=req.user_id).first()
        if not user:
            # Ensure default user exists
            default_user = db.query(User).filter_by(id="default_student").first()
            if not default_user:
                default_user = User(
                    id="default_student",
                    username="default_student",
                    full_name="Student Scholar",
                    avatar_url="avatar_1"
                )
                db.add(default_user)
                prof = StudentProfile(user_id="default_student", grade_level="Beginner", learning_style="Visual")
                db.add(prof)
                db.commit()

        lesson = Lesson(
            id=lesson_id,
            user_id=req.user_id if user else "default_student",
            topic=req.topic,
            subject=final_state.get("subject", "Physics"),
            student_level=req.student_level,
            teaching_style=req.teaching_style,
            duration_target=req.duration_target,
            status="ready",
            total_scenes=len(final_state.get("scenes", [])),
            estimated_duration_sec=sum(s.get("duration_sec", 25.0) for s in final_state.get("scenes", [])),
            source_type=req.source_type,
            lesson_plan_json=json.dumps(final_state.get("lesson_plan", {})),
            assessment_json=json.dumps(final_state.get("assessment_plan", {})),
            summary_json=json.dumps(summary_data)
        )
        db.add(lesson)

        for s_data in final_state.get("scenes", []):
            scene_db = Scene(
                id=s_data.get("id"),
                lesson_id=lesson_id,
                order_index=s_data.get("order_index", 1),
                chapter_title=s_data.get("chapter_title", ""),
                concept=s_data.get("concept", req.topic),
                learning_objective=s_data.get("learning_objective"),
                narration=s_data.get("narration", ""),
                duration_sec=s_data.get("duration_sec", 25.0),
                visual_type=s_data.get("visual_type", "diagram"),
                visual_description=s_data.get("visual_payload", {}).get("title", ""),
                visual_data_json=json.dumps(s_data.get("visual_payload", {})),
                animation_steps_json=json.dumps(s_data.get("animation_steps", [])),
                avatar_state=s_data.get("avatar_state", "SPEAKING"),
                subtitle=s_data.get("subtitle"),
                transition=s_data.get("transition", "fade"),
                audio_path=s_data.get("audio_url"),
                video_clip_path=s_data.get("video_url"),
                is_interactive=s_data.get("is_interactive", False),
                interaction_type=s_data.get("interaction_type"),
                question_text=s_data.get("question_text"),
                question_options_json=json.dumps(s_data.get("question_options", [])),
                expected_answer=s_data.get("expected_answer"),
                is_adaptive=False
            )
            db.add(scene_db)

        db.commit()

    return {
        "lesson_id": lesson_id,
        "topic": req.topic,
        "subject": final_state.get("subject"),
        "total_scenes": len(final_state.get("scenes", [])),
        "estimated_duration_sec": sum(s.get("duration_sec", 25.0) for s in final_state.get("scenes", [])),
        "lesson_plan": final_state.get("lesson_plan"),
        "scenes": final_state.get("scenes"),
        "summary": summary_data,
        "assessment_plan": final_state.get("assessment_plan"),
        "observability_logs": final_state.get("observability_logs", [])
    }


@app.get("/api/lesson/{lesson_id}")
def get_lesson(lesson_id: str):
    with get_db() as db:
        lesson = db.query(Lesson).filter_by(id=lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        scenes = db.query(Scene).filter_by(lesson_id=lesson_id).order_by(Scene.order_index).all()
        
        scenes_data = []
        for s in scenes:
            scenes_data.append({
                "id": s.id,
                "order_index": s.order_index,
                "chapter_title": s.chapter_title,
                "concept": s.concept,
                "learning_objective": s.learning_objective,
                "narration": s.narration,
                "duration_sec": s.duration_sec,
                "visual_type": s.visual_type,
                "visual_payload": json.loads(s.visual_data_json or "{}"),
                "animation_steps": json.loads(s.animation_steps_json or "[]"),
                "avatar_state": s.avatar_state,
                "subtitle": s.subtitle,
                "transition": s.transition,
                "audio_url": s.audio_path,
                "video_url": s.video_clip_path,
                "is_interactive": s.is_interactive,
                "interaction_type": s.interaction_type,
                "question_text": s.question_text,
                "question_options": json.loads(s.question_options_json or "[]"),
                "expected_answer": s.expected_answer,
                "is_adaptive": s.is_adaptive
            })

        summary_data = {}
        if lesson.summary_json:
            try:
                summary_data = json.loads(lesson.summary_json)
            except Exception:
                summary_data = {}

        if not summary_data:
            summary_data = SummaryAgent.generate_summary(
                topic=lesson.topic,
                subject=lesson.subject,
                student_level=lesson.student_level,
                scenes=scenes_data,
                lesson_plan=json.loads(lesson.lesson_plan_json or "{}")
            )

        return {
            "id": lesson.id,
            "topic": lesson.topic,
            "subject": lesson.subject,
            "student_level": lesson.student_level,
            "teaching_style": lesson.teaching_style,
            "duration_target": lesson.duration_target,
            "status": lesson.status,
            "total_scenes": len(scenes_data),
            "estimated_duration_sec": lesson.estimated_duration_sec,
            "lesson_plan": json.loads(lesson.lesson_plan_json or "{}"),
            "summary": summary_data,
            "assessment_plan": json.loads(lesson.assessment_json or "{}"),
            "scenes": scenes_data
        }


@app.get("/api/lesson/{lesson_id}/summary")
def get_lesson_summary(lesson_id: str):
    with get_db() as db:
        lesson = db.query(Lesson).filter_by(id=lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        if lesson.summary_json:
            try:
                return json.loads(lesson.summary_json)
            except Exception:
                pass

        summary_data = SummaryAgent.generate_summary(
            topic=lesson.topic,
            subject=lesson.subject,
            student_level=lesson.student_level
        )
        return summary_data


@app.get("/api/lesson/{lesson_id}/summary/notes.md")
def download_summary_notes(lesson_id: str):
    with get_db() as db:
        lesson = db.query(Lesson).filter_by(id=lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        summary_data = {}
        if lesson.summary_json:
            try:
                summary_data = json.loads(lesson.summary_json)
            except Exception:
                pass
        if not summary_data:
            summary_data = SummaryAgent.generate_summary(
                topic=lesson.topic,
                subject=lesson.subject,
                student_level=lesson.student_level
            )

        md_content = SummaryAgent.generate_markdown_notes(summary_data)
        return PlainTextResponse(md_content, media_type="text/markdown")


@app.post("/api/lesson/{lesson_id}/tutor-ask")
def ask_socratic_tutor(lesson_id: str, req: TutorAskRequest):
    with get_db() as db:
        lesson = db.query(Lesson).filter_by(id=lesson_id).first()
        topic = lesson.topic if lesson else "Core STEM Concept"

    tutor_reply = SocraticTutorAgent.answer_query(
        topic=topic,
        current_scene_title=req.scene_title or "",
        current_scene_narration=req.scene_narration or "",
        student_query=req.student_query,
        learning_style=req.learning_style or "Visual",
        chat_history=req.chat_history or []
    )
    return tutor_reply


@app.post("/api/lesson/{lesson_id}/interact")
def submit_answer(lesson_id: str, req: SubmitAnswerRequest):
    with get_db() as db:
        lesson = db.query(Lesson).filter_by(id=lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

    interaction_state = {
        "lesson_id": lesson_id,
        "user_id": req.user_id,
        "topic": lesson.topic,
        "subject": lesson.subject,
        "student_level": lesson.student_level,
        "teaching_style": lesson.teaching_style,
        "duration_target": lesson.duration_target,
        "source_type": "topic",
        "source_file": None,
        "rag_context": [],
        "student_profile": {},
        "lesson_plan": {},
        "explanations": [],
        "visual_plans": [],
        "examples": [],
        "questions": [],
        "assessment_plan": {},
        "scenes": [],
        "current_scene_index": 0,
        "student_response": req.student_response,
        "evaluation_result": None,
        "detected_misconceptions": [],
        "adaptive_scenes": [],
        "summary": {},
        "assessment_result": None,
        "learning_recommendations": [],
        "status": "evaluating",
        "error": None,
        "observability_logs": []
    }

    # Run LangGraph Adaptive Evaluation Pipeline
    out_state = interaction_pipeline.invoke(interaction_state)

    eval_result = out_state.get("evaluation_result", {})
    adaptive_scenes = out_state.get("adaptive_scenes", [])
    assessment_result = out_state.get("assessment_result", {})

    # Record in DB
    with get_db() as db:
        interaction = Interaction(
            id=f"int_{uuid.uuid4().hex[:8]}",
            lesson_id=lesson_id,
            scene_id=req.scene_id,
            question_text=req.question_text,
            student_response=req.student_response,
            is_correct=eval_result.get("is_correct", False),
            confidence_score=eval_result.get("confidence", 0.9),
            misconception_detected=eval_result.get("detected_misconception"),
            explanation_feedback=eval_result.get("feedback"),
            adaptation_strategy=eval_result.get("adaptation_strategy")
        )
        db.add(interaction)

        # If adaptive scene generated, insert into DB
        for ad_scene in adaptive_scenes:
            scene_db = Scene(
                id=ad_scene.get("id"),
                lesson_id=lesson_id,
                order_index=50,  # Insert after checkpoint
                chapter_title=ad_scene.get("chapter_title", "Adaptive Remediation"),
                concept=ad_scene.get("concept", "Remediation"),
                learning_objective=ad_scene.get("learning_objective"),
                narration=ad_scene.get("narration", ""),
                duration_sec=ad_scene.get("duration_sec", 25.0),
                visual_type=ad_scene.get("visual_type", "circuit_remediation"),
                visual_description="Adaptive Misconception Remediation",
                visual_data_json=json.dumps(ad_scene.get("visual_payload", {})),
                animation_steps_json=json.dumps(ad_scene.get("animation_steps", [])),
                avatar_state=ad_scene.get("avatar_state", "RE_EXPLAINING"),
                subtitle=ad_scene.get("subtitle"),
                transition="fade",
                audio_path=ad_scene.get("audio_url"),
                is_interactive=ad_scene.get("is_interactive", False),
                interaction_type=ad_scene.get("interaction_type"),
                question_text=ad_scene.get("question_text"),
                question_options_json=json.dumps(ad_scene.get("question_options", [])),
                expected_answer=ad_scene.get("expected_answer"),
                is_adaptive=True
            )
            db.add(scene_db)

        # Update student profile mastery
        profile = db.query(StudentProfile).filter_by(user_id=req.user_id).first()
        if not profile:
            profile = db.query(StudentProfile).filter_by(user_id="default_student").first()

        if profile:
            scores = json.loads(profile.mastery_scores or "{}")
            scores[lesson.topic.lower()] = assessment_result.get("mastery_score", 0.9)
            profile.mastery_scores = json.dumps(scores)
            profile.total_lessons_completed += 1

            if eval_result.get("detected_misconception"):
                try:
                    miscs = json.loads(profile.misconceptions_log or "[]")
                except Exception:
                    miscs = []
                miscs.append({
                    "topic": lesson.topic,
                    "misconception": eval_result.get("detected_misconception"),
                    "status": "remediated" if not eval_result.get("is_correct") else "cleared"
                })
                profile.misconceptions_log = json.dumps(miscs)

        db.commit()

    return {
        "evaluation": eval_result,
        "has_misconception": bool(eval_result.get("detected_misconception")),
        "adaptive_scene": adaptive_scenes[0] if adaptive_scenes else None,
        "assessment_result": assessment_result,
        "observability_logs": out_state.get("observability_logs", [])
    }


# ==========================================
# Study Notes & Quiz Analytics Endpoints
# ==========================================

@app.post("/api/notes/save")
def save_note(req: SaveNoteRequest):
    with get_db() as db:
        note_id = f"note_{uuid.uuid4().hex[:10]}"
        note = StudyNote(
            id=note_id,
            user_id=req.user_id,
            lesson_id=req.lesson_id,
            topic=req.topic,
            content=req.content,
            tags_json=json.dumps(req.tags or [])
        )
        db.add(note)
        db.commit()
        db.refresh(note)

        return {
            "id": note.id,
            "topic": note.topic,
            "content": note.content,
            "tags": req.tags or [],
            "created_at": note.created_at.isoformat() if note.created_at else None,
            "message": "Note saved successfully"
        }


@app.get("/api/notes/{user_id}")
def get_user_notes(user_id: str):
    with get_db() as db:
        notes = db.query(StudyNote).filter_by(user_id=user_id).order_by(StudyNote.created_at.desc()).all()
        return [
            {
                "id": n.id,
                "lesson_id": n.lesson_id,
                "topic": n.topic,
                "content": n.content,
                "tags": json.loads(n.tags_json or "[]"),
                "created_at": n.created_at.isoformat() if n.created_at else None
            }
            for n in notes
        ]


@app.post("/api/assessment/evaluate")
def evaluate_assessment(req: QuizSubmitRequest):
    analytics = MasteryAnalyticsAgent.evaluate_quiz_performance(
        quiz_submission=req.quiz_submission,
        quiz_schema=req.quiz_schema,
        student_profile={}
    )

    with get_db() as db:
        profile = db.query(StudentProfile).filter_by(user_id=req.user_id).first()
        if profile:
            scores = json.loads(profile.mastery_scores or "{}")
            topic_key = req.quiz_schema.get("quiz_title", "general").lower()
            scores[topic_key] = analytics["score_pct"] / 100.0
            profile.mastery_scores = json.dumps(scores)
            db.commit()

    return analytics


@app.post("/api/rag/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = DocumentParser.parse_pdf(str(file_path))
    rag_retriever.add_documents(chunks)

    return {
        "status": "success",
        "filename": filename,
        "total_chunks_indexed": len(chunks),
        "message": f"Successfully parsed and indexed {len(chunks)} chunks from {filename}."
    }


@app.get("/api/profile/{user_id}")
def get_profile(user_id: str):
    with get_db() as db:
        user = db.query(User).filter_by(id=user_id).first()
        if not user or not user.profile:
            return {
                "user_id": user_id,
                "username": user_id,
                "full_name": "Student Scholar",
                "avatar_url": "avatar_1",
                "grade_level": "Beginner",
                "learning_style": "Visual",
                "learning_goal": "Master core STEM concepts",
                "mastery_scores": {"physics.circuits": 0.88, "math.algebra": 0.75},
                "total_lessons_completed": 6,
                "total_study_minutes": 45,
                "recent_misconceptions": []
            }

        return format_user_profile(user)


@app.get("/api/learning-path/{topic}")
def get_learning_path(topic: str):
    topic_lower = topic.lower()
    if "circuit" in topic_lower or "ohm" in topic_lower or "physics" in topic_lower:
        nodes = [
            {"id": "node_1", "title": "Electric Charge & Voltage", "status": "completed", "duration": "15 min"},
            {"id": "node_2", "title": "Ohm's Law & Resistance", "status": "in_progress", "duration": "20 min"},
            {"id": "node_3", "title": "Series & Parallel Circuits", "status": "locked", "duration": "30 min"},
            {"id": "node_4", "title": "Kirchhoff's Laws (KVL/KCL)", "status": "locked", "duration": "45 min"},
            {"id": "node_5", "title": "Power Dissipation & Efficiency", "status": "locked", "duration": "30 min"}
        ]
    elif "binary" in topic_lower or "search" in topic_lower or "algorithm" in topic_lower:
        nodes = [
            {"id": "node_1", "title": "Array Indexing & Linear Search", "status": "completed", "duration": "15 min"},
            {"id": "node_2", "title": "Binary Search Algorithm", "status": "in_progress", "duration": "20 min"},
            {"id": "node_3", "title": "Binary Search on Answer Spaces", "status": "locked", "duration": "35 min"},
            {"id": "node_4", "title": "Two Pointers & Sliding Window", "status": "locked", "duration": "40 min"},
            {"id": "node_5", "title": "Binary Search Trees (BST)", "status": "locked", "duration": "45 min"}
        ]
    else:
        nodes = [
            {"id": "node_1", "title": f"Fundamentals of {topic}", "status": "in_progress", "duration": "20 min"},
            {"id": "node_2", "title": f"Core Mechanisms of {topic}", "status": "locked", "duration": "30 min"},
            {"id": "node_3", "title": f"Advanced Problem Solving in {topic}", "status": "locked", "duration": "45 min"}
        ]

    return {
        "topic": topic,
        "domain": "STEM",
        "nodes": nodes
    }


# Serve frontend static assets and index.html
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
if FRONTEND_DIST.exists():
    if (FRONTEND_DIST / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="frontend_assets")

    @app.get("/")
    def serve_frontend_index():
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{full_path:path}")
    def serve_frontend_catchall(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        target_file = FRONTEND_DIST / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(target_file)
        return FileResponse(FRONTEND_DIST / "index.html")
