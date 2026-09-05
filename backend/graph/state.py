from typing import TypedDict, List, Dict, Any, Optional

class TeachingSessionState(TypedDict):
    # Session & Lesson Metadata
    lesson_id: str
    user_id: str
    topic: str
    subject: str
    student_level: str  # Beginner, Intermediate, Advanced
    teaching_style: str  # Simple, Visual, Practical, Technical, Socratic
    duration_target: str  # 5 min, 20 min, 60 min, 7 days
    source_type: str  # topic or document
    source_file: Optional[str]
    rag_context: List[Dict[str, Any]]
    
    # Student Profile
    student_profile: Dict[str, Any]
    
    # Lesson Plan & Curriculum
    lesson_plan: Dict[str, Any]
    
    # Parallel Preparation Branch Outputs
    explanations: List[Dict[str, Any]]
    visual_plans: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    questions: List[Dict[str, Any]]
    assessment_plan: Dict[str, Any]
    
    # Rendered & Sequenced Scenes
    scenes: List[Dict[str, Any]]
    current_scene_index: int
    
    # Interactive & Evaluation State
    student_response: Optional[str]
    evaluation_result: Optional[Dict[str, Any]]
    detected_misconceptions: List[Dict[str, Any]]
    adaptive_scenes: List[Dict[str, Any]]
    
    # Final Outcomes
    summary: Optional[Dict[str, Any]]
    assessment_result: Optional[Dict[str, Any]]
    learning_recommendations: List[str]
    status: str
    error: Optional[str]
    observability_logs: List[Dict[str, Any]]
