import json
import os
import re
import secrets
import shutil
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel, Field, ConfigDict

from backend.config import STORAGE_DIR, AUDIO_DIR, VIDEO_DIR, UPLOAD_DIR, SERVER_HOST, SERVER_PORT, PROJECT_ROOT, ALLOWED_ORIGINS, MAX_UPLOAD_BYTES
from backend.database.db import init_db, get_db
from backend.database.models import User, StudentProfile, Lesson, Scene, Interaction, StudyNote
from backend.database.auth import register_user, authenticate_user, generate_session_token, verify_session_token, format_user_profile
from backend.graph.workflow import lesson_pipeline, interaction_pipeline
from backend.rag.parser import DocumentParser
from backend.rag.retriever import RAGRetriever
from backend.agents.summary_agent import SummaryAgent
from backend.agents.tutor_agent import SocraticTutorAgent
from backend.agents.analytics_agent import MasteryAnalyticsAgent

init_db()
rag_retriever = RAGRetriever()
app = FastAPI(title="AI Teacher", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=True, allow_methods=["GET","POST","PUT","DELETE","OPTIONS"], allow_headers=["Authorization","Content-Type"], max_age=600)
app.mount("/api/media/video", StaticFiles(directory=str(VIDEO_DIR)), name="media_video")
app.mount("/api/media", StaticFiles(directory=str(AUDIO_DIR)), name="media_audio")

class RegisterRequest(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    full_name: Optional[str] = ""
    grade_level: str = "Beginner"
    learning_style: str = "Visual"
    learning_goal: str = "Master core STEM concepts"
    avatar_url: str = "avatar_1"
class LoginRequest(BaseModel):
    username_or_email: str
    password: str
class UpdateProfileRequest(BaseModel):
    # user_id is accepted for old clients but intentionally ignored; identity comes from the signed session.
    user_id: Optional[str] = None
    model_config=ConfigDict(extra="ignore")
    full_name: Optional[str]=None; grade_level: Optional[str]=None; learning_style: Optional[str]=None; learning_goal: Optional[str]=None; avatar_url: Optional[str]=None
class BookmarkRequest(BaseModel):
    lesson_id: str
class CreateLessonRequest(BaseModel):
    topic: str
    student_level: str="Beginner"; teaching_style: str="Visual"; duration_target: str="20 min"
    source_type: str="topic"; source_filename: Optional[str]=None; model_provider: Optional[str]="autonomous"
class SubmitAnswerRequest(BaseModel):
    scene_id: str; question_text: str; student_response: str
class TutorAskRequest(BaseModel):
    student_query: str; scene_title: Optional[str]=""; scene_narration: Optional[str]=""; learning_style: Optional[str]="Visual"; chat_history: List[Dict[str,str]]=Field(default_factory=list)
class SaveNoteRequest(BaseModel):
    lesson_id: Optional[str]=None; topic: str; content: str; tags: List[str]=Field(default_factory=list)
class QuizSubmitRequest(BaseModel):
    quiz_submission: List[Dict[str,Any]]; quiz_schema: Dict[str,Any]

def current_user(authorization: Optional[str]=Header(None)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401,"Authentication required")
    token=authorization.split(" ",1)[1].strip()
    user_id=verify_session_token(token)
    if not user_id: raise HTTPException(401,"Invalid or expired session")
    with get_db() as db:
        user=db.query(User).filter_by(id=user_id).first()
        if not user: raise HTTPException(401,"User session no longer exists")
        # detach a minimal identity object before the session closes
        data={"id":user.id,"username":user.username}
    return data

def user_id(dep=Depends(current_user)):
    return dep["id"]

def serialize_scene(s):
    return {"id":s.id,"order_index":s.order_index,"chapter_title":s.chapter_title,"concept":s.concept,"learning_objective":s.learning_objective,"narration":s.narration,"duration_sec":s.duration_sec,"visual_type":s.visual_type,"visual_payload":json.loads(s.visual_data_json or "{}"),"animation_steps":json.loads(s.animation_steps_json or "[]"),"avatar_state":s.avatar_state,"subtitle":s.subtitle,"transition":s.transition,"audio_url":s.audio_path,"video_url":s.video_clip_path,"is_interactive":s.is_interactive,"interaction_type":s.interaction_type,"question_text":s.question_text,"question_options":json.loads(s.question_options_json or "[]"),"expected_answer":s.expected_answer,"has_simulation":json.loads(s.visual_data_json or "{}").get("has_simulation",False),"is_adaptive":s.is_adaptive}

@app.get("/api/health")
def health(): return {"status":"ok","version":"3.0.0","service":"AI Teacher"}

@app.post("/api/auth/register")
def register(req:RegisterRequest):
    with get_db() as db:
        user,err=register_user(db,req.username,req.email,req.password,req.full_name or req.username,req.grade_level,req.learning_style,req.learning_goal,req.avatar_url)
        if err: raise HTTPException(400,err)
        return {"token":generate_session_token(user.id),"user":format_user_profile(user),"message":"Account created successfully"}

@app.post("/api/auth/login")
def login(req:LoginRequest):
    with get_db() as db:
        user,err=authenticate_user(db,req.username_or_email,req.password)
        if err: raise HTTPException(401,err)
        return {"token":generate_session_token(user.id),"user":format_user_profile(user),"message":"Logged in successfully"}

@app.post("/api/auth/logout")
def logout(_:dict=Depends(current_user)): return {"message":"Logged out. Remove the token on the client."}

@app.get("/api/auth/me")
def me(dep=Depends(current_user)):
    with get_db() as db:
        user=db.query(User).filter_by(id=dep["id"]).first()
        return {"user":format_user_profile(user)}

@app.put("/api/auth/profile")
def update_profile(req:UpdateProfileRequest, uid:str=Depends(user_id)):
    with get_db() as db:
        user=db.query(User).filter_by(id=uid).first()
        if not user: raise HTTPException(404,"User not found")
        for field in ["full_name","avatar_url"]:
            val=getattr(req,field)
            if val is not None: setattr(user,field,val.strip() if isinstance(val,str) else val)
        if user.profile:
            for field in ["grade_level","learning_style","learning_goal"]:
                val=getattr(req,field)
                if val is not None: setattr(user.profile,field,val.strip())
        db.commit(); db.refresh(user)
        return {"user":format_user_profile(user)}

@app.post("/api/auth/bookmark")
def toggle_bookmark(req:BookmarkRequest, uid:str=Depends(user_id)):
    with get_db() as db:
        user=db.query(User).filter_by(id=uid).first()
        lesson=db.query(Lesson).filter_by(id=req.lesson_id,user_id=uid).first()
        if not lesson: raise HTTPException(404,"Lesson not found")
        try: bookmarks=json.loads(user.bookmarks_json or "[]")
        except Exception: bookmarks=[]
        if req.lesson_id in bookmarks: bookmarks.remove(req.lesson_id); state=False
        else: bookmarks.append(req.lesson_id); state=True
        user.bookmarks_json=json.dumps(bookmarks); db.commit()
        return {"is_bookmarked":state,"bookmarks":bookmarks}

@app.post("/api/lesson/create")
def create_lesson(req:CreateLessonRequest, uid:str=Depends(user_id)):
    topic=req.topic.strip()
    if not 2 <= len(topic) <= 255: raise HTTPException(422,"Topic must be between 2 and 255 characters")
    lesson_id=f"lesson_{uuid.uuid4().hex[:12]}"
    with get_db() as db:
        profile=db.query(StudentProfile).filter_by(user_id=uid).first()
        if not profile: raise HTTPException(400,"Student profile is missing")
        initial_state={"lesson_id":lesson_id,"user_id":uid,"topic":topic,"subject":"General Science","student_level":req.student_level,"teaching_style":req.teaching_style,"duration_target":req.duration_target,"source_type":req.source_type,"source_file":req.source_filename,"rag_context":rag_retriever.search(topic,uid),"student_profile":{"grade_level":profile.grade_level,"learning_style":profile.learning_style,"learning_goal":profile.learning_goal,"mastery_scores":json.loads(profile.mastery_scores or "{}")},"lesson_plan":{},"explanations":[],"visual_plans":[],"examples":[],"questions":[],"assessment_plan":{},"scenes":[],"current_scene_index":0,"student_response":None,"evaluation_result":None,"detected_misconceptions":[],"adaptive_scenes":[],"summary":{},"assessment_result":None,"learning_recommendations":[],"status":"planning","error":None,"observability_logs":[]}
    try: final_state=lesson_pipeline.invoke(initial_state)
    except Exception as exc:
        raise HTTPException(500,f"Lesson generation failed: {type(exc).__name__}: {exc}")
    scenes=final_state.get("scenes",[])
    summary=final_state.get("summary") or SummaryAgent.generate_summary(topic=topic,subject=final_state.get("subject","General Science"),student_level=req.student_level,scenes=scenes,lesson_plan=final_state.get("lesson_plan",{}))
    with get_db() as db:
        lesson=Lesson(id=lesson_id,user_id=uid,topic=topic,subject=final_state.get("subject","General Science"),student_level=req.student_level,teaching_style=req.teaching_style,duration_target=req.duration_target,status="ready",total_scenes=len(scenes),estimated_duration_sec=sum(float(s.get("duration_sec",25)) for s in scenes),source_type=req.source_type,source_filename=req.source_filename,lesson_plan_json=json.dumps(final_state.get("lesson_plan",{})),assessment_json=json.dumps(final_state.get("assessment_plan",{})),summary_json=json.dumps(summary))
        db.add(lesson)
        for s in scenes:
            db.add(Scene(id=s.get("id") or f"scene_{uuid.uuid4().hex}",lesson_id=lesson_id,order_index=s.get("order_index",1),chapter_title=s.get("chapter_title",""),concept=s.get("concept",topic),learning_objective=s.get("learning_objective"),narration=s.get("narration","")[:200000],duration_sec=s.get("duration_sec",25),visual_type=s.get("visual_type","diagram"),visual_description=s.get("visual_payload",{}).get("title",""),visual_data_json=json.dumps(s.get("visual_payload",{})),animation_steps_json=json.dumps(s.get("animation_steps",[])),avatar_state=s.get("avatar_state","SPEAKING"),subtitle=s.get("subtitle"),transition=s.get("transition","fade"),audio_path=s.get("audio_url"),video_clip_path=s.get("video_url"),is_interactive=s.get("is_interactive",False),interaction_type=s.get("interaction_type"),question_text=s.get("question_text"),question_options_json=json.dumps(s.get("question_options",[])),expected_answer=s.get("expected_answer")))
        db.commit()
    return {"id":lesson_id,"lesson_id":lesson_id,"topic":topic,"subject":final_state.get("subject"),"total_scenes":len(scenes),"estimated_duration_sec":sum(float(s.get("duration_sec",25)) for s in scenes),"lesson_plan":final_state.get("lesson_plan"),"scenes":scenes,"summary":summary,"assessment_plan":final_state.get("assessment_plan"),"observability_logs":final_state.get("observability_logs",[]),"status":"ready"}

@app.get("/api/lesson/{lesson_id}")
def get_lesson(lesson_id:str,uid:str=Depends(user_id)):
    with get_db() as db:
        lesson=db.query(Lesson).filter_by(id=lesson_id,user_id=uid).first()
        if not lesson: raise HTTPException(404,"Lesson not found")
        scenes=[serialize_scene(s) for s in db.query(Scene).filter_by(lesson_id=lesson_id).order_by(Scene.order_index).all()]
        return {"id":lesson.id,"topic":lesson.topic,"subject":lesson.subject,"student_level":lesson.student_level,"teaching_style":lesson.teaching_style,"duration_target":lesson.duration_target,"status":lesson.status,"total_scenes":len(scenes),"estimated_duration_sec":lesson.estimated_duration_sec,"lesson_plan":json.loads(lesson.lesson_plan_json or "{}"),"summary":json.loads(lesson.summary_json or "{}"),"assessment_plan":json.loads(lesson.assessment_json or "{}"),"scenes":scenes}

@app.get("/api/lesson/{lesson_id}/summary")
def summary(lesson_id:str,uid:str=Depends(user_id)):
    with get_db() as db:
        lesson=db.query(Lesson).filter_by(id=lesson_id,user_id=uid).first()
        if not lesson: raise HTTPException(404,"Lesson not found")
        return json.loads(lesson.summary_json or "{}")

@app.get("/api/lesson/{lesson_id}/summary/notes.md")
def summary_notes(lesson_id:str,uid:str=Depends(user_id)):
    with get_db() as db:
        lesson=db.query(Lesson).filter_by(id=lesson_id,user_id=uid).first()
        if not lesson: raise HTTPException(404,"Lesson not found")
        return PlainTextResponse(SummaryAgent.generate_markdown_notes(json.loads(lesson.summary_json or "{}")),media_type="text/markdown")

@app.post("/api/lesson/{lesson_id}/tutor-ask")
def tutor(lesson_id:str,req:TutorAskRequest,uid:str=Depends(user_id)):
    with get_db() as db:
        lesson=db.query(Lesson).filter_by(id=lesson_id,user_id=uid).first()
        if not lesson: raise HTTPException(404,"Lesson not found")
        topic=lesson.topic
    return SocraticTutorAgent.answer_query(topic=topic,current_scene_title=req.scene_title or "",current_scene_narration=req.scene_narration or "",student_query=req.student_query.strip(),learning_style=req.learning_style or "Visual",chat_history=req.chat_history[-20:])

@app.post("/api/lesson/{lesson_id}/interact")
def interact(lesson_id:str,req:SubmitAnswerRequest,uid:str=Depends(user_id)):
    with get_db() as db:
        lesson=db.query(Lesson).filter_by(id=lesson_id,user_id=uid).first(); scene=db.query(Scene).filter_by(id=req.scene_id,lesson_id=lesson_id).first()
        if not lesson or not scene: raise HTTPException(404,"Lesson or scene not found")
        state={"lesson_id":lesson_id,"user_id":uid,"topic":lesson.topic,"subject":lesson.subject,"student_level":lesson.student_level,"teaching_style":lesson.teaching_style,"duration_target":lesson.duration_target,"source_type":lesson.source_type,"source_file":lesson.source_filename,"rag_context":rag_retriever.search(lesson.topic,uid),"student_profile":{},"lesson_plan":json.loads(lesson.lesson_plan_json or "{}"),"explanations":[],"visual_plans":[],"examples":[],"questions":[],"assessment_plan":json.loads(lesson.assessment_json or "{}"),"scenes":[],"current_scene_index":scene.order_index-1,"student_response":req.student_response,"evaluation_result":None,"detected_misconceptions":[],"adaptive_scenes":[],"summary":{},"assessment_result":None,"learning_recommendations":[],"status":"in_progress","error":None,"observability_logs":[]}
    try: out=interaction_pipeline.invoke(state)
    except Exception as exc: raise HTTPException(500,f"Answer evaluation failed: {type(exc).__name__}: {exc}")
    eval_result=out.get("evaluation_result") or {}
    with get_db() as db:
        db.add(Interaction(id=f"int_{uuid.uuid4().hex[:12]}",lesson_id=lesson_id,scene_id=req.scene_id,question_text=req.question_text[:10000],student_response=req.student_response[:10000],is_correct=bool(eval_result.get("is_correct")),confidence_score=float(eval_result.get("confidence",0)),misconception_detected=eval_result.get("detected_misconception"),explanation_feedback=eval_result.get("feedback"),adaptation_strategy=eval_result.get("adaptation_strategy")))
        profile=db.query(StudentProfile).filter_by(user_id=uid).first()
        if profile and out.get("assessment_result"):
            scores=json.loads(profile.mastery_scores or "{}"); scores[lesson.topic.lower()]=float(out["assessment_result"].get("mastery_score",scores.get(lesson.topic.lower(),0))); profile.mastery_scores=json.dumps(scores)
        db.commit()
    return {"evaluation":eval_result,"has_misconception":bool(eval_result.get("detected_misconception")),"adaptive_scene":(out.get("adaptive_scenes") or [None])[0],"assessment_result":out.get("assessment_result"),"observability_logs":out.get("observability_logs",[])}

@app.post("/api/notes/save")
def save_note(req:SaveNoteRequest,uid:str=Depends(user_id)):
    if len(req.content.strip())<1: raise HTTPException(422,"Note cannot be empty")
    with get_db() as db:
        if req.lesson_id and not db.query(Lesson).filter_by(id=req.lesson_id,user_id=uid).first(): raise HTTPException(404,"Lesson not found")
        note=StudyNote(id=f"note_{uuid.uuid4().hex[:12]}",user_id=uid,lesson_id=req.lesson_id,topic=req.topic.strip()[:255],content=req.content[:100000],tags_json=json.dumps(req.tags[:20])); db.add(note); db.commit(); db.refresh(note)
        return {"id":note.id,"topic":note.topic,"content":note.content,"tags":req.tags[:20],"created_at":note.created_at.isoformat() if note.created_at else None}

@app.get("/api/notes")
def notes(uid:str=Depends(user_id)):
    with get_db() as db:
        rows=db.query(StudyNote).filter_by(user_id=uid).order_by(StudyNote.created_at.desc()).all()
        return [{"id":n.id,"lesson_id":n.lesson_id,"topic":n.topic,"content":n.content,"tags":json.loads(n.tags_json or "[]"),"created_at":n.created_at.isoformat() if n.created_at else None} for n in rows]

@app.get("/api/notes/{legacy_user_id}")
def legacy_notes(legacy_user_id:str,uid:str=Depends(user_id)):
    if legacy_user_id!=uid: raise HTTPException(403,"You can only access your own notes")
    return notes(uid)

@app.post("/api/assessment/evaluate")
def assessment(req:QuizSubmitRequest,uid:str=Depends(user_id)):
    analytics=MasteryAnalyticsAgent.evaluate_quiz_performance(quiz_submission=req.quiz_submission,quiz_schema=req.quiz_schema,student_profile={})
    with get_db() as db:
        profile=db.query(StudentProfile).filter_by(user_id=uid).first()
        if profile:
            scores=json.loads(profile.mastery_scores or "{}"); scores[str(req.quiz_schema.get("quiz_title","general")).lower()]=analytics["score_pct"]/100; profile.mastery_scores=json.dumps(scores); db.commit()
    return analytics

@app.post("/api/rag/upload")
async def upload_document(file:UploadFile=File(...),uid:str=Depends(user_id)):
    allowed={".pdf",".txt",".md"}; suffix=Path(file.filename or "").suffix.lower()
    if suffix not in allowed: raise HTTPException(415,"Only PDF, TXT and Markdown files are supported")
    if not file.filename or len(file.filename)>255: raise HTTPException(400,"Invalid filename")
    safe_name=f"{uuid.uuid4().hex}{suffix}"; path=UPLOAD_DIR/safe_name; total=0
    try:
        with path.open("wb") as out:
            while True:
                chunk=await file.read(1024*1024)
                if not chunk: break
                total+=len(chunk)
                if total>MAX_UPLOAD_BYTES: raise HTTPException(413,f"File exceeds {MAX_UPLOAD_BYTES//(1024*1024)} MB limit")
                out.write(chunk)
        chunks=DocumentParser.parse(str(path))
        if not chunks: raise HTTPException(422,"No readable text was found in the document")
        rag_retriever.add_documents(chunks,uid,file.filename)
        return {"status":"success","filename":file.filename,"total_chunks_indexed":len(chunks)}
    except HTTPException: path.unlink(missing_ok=True); raise
    except Exception as exc: path.unlink(missing_ok=True); raise HTTPException(422,f"Could not parse document: {type(exc).__name__}")

@app.get("/api/profile")
def profile(uid:str=Depends(user_id)):
    with get_db() as db:
        user=db.query(User).filter_by(id=uid).first()
        if not user: raise HTTPException(404,"User not found")
        return format_user_profile(user)

@app.get("/api/learning-path/{topic}")
def learning_path(topic:str,uid:str=Depends(user_id)):
    # Keep a useful deterministic fallback, but personalize progress from stored mastery.
    with get_db() as db:
        p=db.query(StudentProfile).filter_by(user_id=uid).first(); mastery=json.loads(p.mastery_scores or "{}") if p else {}
    nodes=[{"id":"node_1","title":f"Foundations of {topic}","status":"in_progress","duration":"15 min"},{"id":"node_2","title":f"Core mechanisms of {topic}","status":"locked","duration":"20 min"},{"id":"node_3","title":f"Worked problems in {topic}","status":"locked","duration":"30 min"},{"id":"node_4","title":f"Applications of {topic}","status":"locked","duration":"25 min"}]
    score=float(mastery.get(topic.lower(),0))
    if score>=0.8: nodes[0]["status"]="completed"; nodes[1]["status"]="in_progress"
    return {"topic":topic,"domain":"STEM","nodes":nodes}

FRONTEND_DIST=PROJECT_ROOT/"frontend"/"dist"
if FRONTEND_DIST.exists():
    if (FRONTEND_DIST/"assets").exists(): app.mount("/assets",StaticFiles(directory=str(FRONTEND_DIST/"assets")),name="frontend_assets")
    @app.get("/")
    def index(): return FileResponse(FRONTEND_DIST/"index.html")
    @app.get("/{full_path:path}")
    def spa(full_path:str):
        if full_path.startswith("api/"): raise HTTPException(404,"API route not found")
        target=FRONTEND_DIST/full_path
        return FileResponse(target if target.exists() and target.is_file() else FRONTEND_DIST/"index.html")
