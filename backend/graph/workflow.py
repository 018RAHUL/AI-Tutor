from langgraph.graph import StateGraph, END
from backend.graph.state import TeachingSessionState
from backend.graph.nodes.input_analyzer import input_analyzer_node, student_profiler_node
from backend.graph.nodes.lesson_planner import lesson_planner_node
from backend.graph.nodes.parallel_prep import parallel_prep_node
from backend.graph.nodes.scene_planner import scene_planner_node
from backend.graph.nodes.evaluator import evaluator_node, misconception_detector_node
from backend.graph.nodes.adaptive_router import adaptive_router_node
from backend.graph.nodes.assessment_node import assessment_node

def build_lesson_creation_graph() -> StateGraph:
    """
    Builds the main LangGraph pipeline for creating full educational video lessons:
    Input Analysis -> Student Profiling -> Lesson Planning -> Parallel Prep -> Scene Planner Fan-In
    """
    workflow = StateGraph(TeachingSessionState)

    workflow.add_node("input_analyzer", input_analyzer_node)
    workflow.add_node("student_profiler", student_profiler_node)
    workflow.add_node("lesson_planner", lesson_planner_node)
    workflow.add_node("parallel_prep", parallel_prep_node)
    workflow.add_node("scene_planner", scene_planner_node)

    workflow.set_entry_point("input_analyzer")
    workflow.add_edge("input_analyzer", "student_profiler")
    workflow.add_edge("student_profiler", "lesson_planner")
    workflow.add_edge("lesson_planner", "parallel_prep")
    workflow.add_edge("parallel_prep", "scene_planner")
    workflow.add_edge("scene_planner", END)

    return workflow.compile()


def build_interaction_evaluation_graph() -> StateGraph:
    """
    Builds the adaptive interaction evaluation graph:
    Evaluator -> Misconception Detector -> Adaptive Router -> Assessment Node
    """
    workflow = StateGraph(TeachingSessionState)

    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("misconception_detector", misconception_detector_node)
    workflow.add_node("adaptive_router", adaptive_router_node)
    workflow.add_node("assessment_node", assessment_node)

    workflow.set_entry_point("evaluator")
    workflow.add_edge("evaluator", "misconception_detector")
    workflow.add_edge("misconception_detector", "adaptive_router")
    workflow.add_edge("adaptive_router", "assessment_node")
    workflow.add_edge("assessment_node", END)

    return workflow.compile()

# Pre-compiled instances for direct invocation
lesson_pipeline = build_lesson_creation_graph()
interaction_pipeline = build_interaction_evaluation_graph()
