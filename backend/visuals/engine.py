from typing import Dict, Any, List
from backend.visuals.circuit_visuals import CircuitVisualGenerator
from backend.visuals.cs_visuals import CSVisualGenerator
from backend.visuals.math_visuals import MathVisualGenerator

class VisualEngine:
    """
    Master Visual Reasoning & Generation Engine.
    Interprets concept, subject, narration, and chapter context to generate
    deterministic, beautiful, educational interactive visual payloads.
    """

    @classmethod
    def generate_visual_for_scene(
        cls,
        subject: str,
        topic: str,
        concept: str,
        narration: str,
        chapter_id: str = "",
        student_level: str = "Beginner"
    ) -> Dict[str, Any]:
        
        topic_lower = topic.lower()
        concept_lower = concept.lower()
        narration_lower = narration.lower()
        clean_topic = topic.strip() or "Foundational Concept"

        # 1. Ohm's Law & Circuits Domain
        if any(k in topic_lower for k in ["ohm", "circuit", "voltage", "current", "resistan", "resistor", "electricity"]):
            if "water" in narration_lower or "analogy" in concept_lower or "pipe" in narration_lower:
                return CircuitVisualGenerator.get_water_analogy_visual()
            elif "formula" in concept_lower or "v = i" in narration_lower or "relationship" in concept_lower:
                return CircuitVisualGenerator.get_formula_breakdown_visual()
            elif "example" in concept_lower or "solve" in narration_lower or "12" in narration_lower:
                return CircuitVisualGenerator.get_worked_example_visual()
            elif "remediation" in concept_lower or "misconception" in concept_lower:
                return CircuitVisualGenerator.get_remediation_visual()
            else:
                return CircuitVisualGenerator.get_intro_visual()

        # 2. Biology: Photosynthesis & Cellular Biology
        elif any(k in topic_lower for k in ["photosynthesis", "chloroplast", "plant", "chlorophyll", "light reaction", "calvin", "mitosis", "cell", "dna"]):
            if "light" in concept_lower or "thylakoid" in narration_lower or "water" in narration_lower:
                return {
                    "type": "biology_photosynthesis",
                    "has_simulation": False,
                    "subtype": "light_reactions",
                    "title": f"Photosynthesis: Light-Dependent Phase in Thylakoids",
                    "formula": "6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂",
                    "formula_latex": "6\\text{CO}_2 + 6\\text{H}_2\\text{O} + h\\nu \\rightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2",
                    "key_points": [
                        {"label": "Solar Energy Absorption", "detail": "Chlorophyll pigments in thylakoid membranes capture photons."},
                        {"label": "Photolysis of Water", "detail": "H₂O molecules split into protons, electrons, and O₂ gas."},
                        {"label": "Energy Carriers", "detail": "Converts ADP and NADP+ into high-energy ATP and NADPH."}
                    ],
                    "diagram_type": "chloroplast_thylakoid",
                    "highlight_color": "#10b981"
                }
            elif "calvin" in concept_lower or "glucose" in narration_lower or "stroma" in narration_lower or "carbon" in narration_lower:
                return {
                    "type": "biology_photosynthesis",
                    "has_simulation": False,
                    "subtype": "calvin_cycle",
                    "title": f"Photosynthesis: Calvin Cycle & Carbon Fixation",
                    "formula": "6CO₂ + 18ATP + 12NADPH → C₆H₁₂O₆ + 18ADP + 12NADP⁺",
                    "formula_latex": "6\\text{CO}_2 + 18\\text{ATP} + 12\\text{NADPH} \\rightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6",
                    "key_points": [
                        {"label": "Carbon Fixation", "detail": "CO₂ gas from atmosphere fixed by RuBisCO enzyme in stroma."},
                        {"label": "Sugar Synthesis", "detail": "Synthesizes glucose (C₆H₁₂O₆) for cellular energy and biomass."},
                        {"label": "Ecological Balance", "detail": "Powers terrestrial and aquatic food chains globally."}
                    ],
                    "diagram_type": "calvin_cycle_stroma",
                    "highlight_color": "#34d399"
                }
            else:
                return {
                    "type": "biology_photosynthesis",
                    "has_simulation": False,
                    "subtype": "overview",
                    "title": f"Chloroplast Architecture & Photosynthetic Pathways",
                    "formula": "6CO₂ + 6H₂O + Light → C₆H₁₂O₆ + 6O₂",
                    "formula_latex": "6\\text{CO}_2 + 6\\text{H}_2\\text{O} + h\\nu \\rightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2",
                    "key_points": [
                        {"label": "Solar Conversion", "detail": "Transforms solar electromagnetic radiation into biochemical energy."},
                        {"label": "Oxygen Release", "detail": "Byproduct of water photolysis sustains aerobic life on Earth."},
                        {"label": "Biomass Production", "detail": "Produces carbohydrate sugars forming plant cell walls."}
                    ],
                    "diagram_type": "chloroplast_overview",
                    "highlight_color": "#10b981"
                }

        # 3. Physics Mechanics: Newton's Laws & Classical Dynamics
        elif any(k in topic_lower for k in ["newton", "force", "gravity", "gravitation", "motion", "inertia", "acceleration", "friction", "momentum"]):
            if "second" in concept_lower or "f = m" in narration_lower or "acceleration" in concept_lower:
                return {
                    "type": "physics_mechanics",
                    "has_simulation": False,
                    "subtype": "second_law",
                    "title": "Newton's Second Law: Net Force & Acceleration (F = ma)",
                    "formula": "F_net = m * a",
                    "formula_latex": "F_{\\text{net}} = m \\times a",
                    "key_points": [
                        {"label": "Net Force (F)", "detail": "Vector sum of all external forces acting on mass (Newtons, N)."},
                        {"label": "Mass Inertia (m)", "detail": "Opposition to velocity changes (Kilograms, kg)."},
                        {"label": "Acceleration (a)", "detail": "Rate of change of velocity (m/s²). a = F / m."}
                    ],
                    "diagram_type": "force_vector_dynamics",
                    "highlight_color": "#0ea5e9"
                }
            elif "third" in concept_lower or "action" in concept_lower or "reaction" in narration_lower:
                return {
                    "type": "physics_mechanics",
                    "has_simulation": False,
                    "subtype": "third_law",
                    "title": "Newton's Third Law: Action-Reaction Pairs",
                    "formula": "F_AB = - F_BA",
                    "formula_latex": "F_{AB} = -F_{BA}",
                    "key_points": [
                        {"label": "Mutual Interaction", "detail": "Every applied force produces an equal and opposite reaction."},
                        {"label": "Simultaneous Pairs", "detail": "Forces act on two different bodies and never cancel each other."},
                        {"label": "Rocket Propulsion", "detail": "Exhaust gases pushed backward drive the spacecraft forward."}
                    ],
                    "diagram_type": "action_reaction_vectors",
                    "highlight_color": "#f59e0b"
                }
            else:
                return {
                    "type": "physics_mechanics",
                    "has_simulation": False,
                    "subtype": "first_law",
                    "title": "Newton's First Law: The Principle of Inertia",
                    "formula": "Σ F = 0 ⟹ a = 0 (v = const)",
                    "formula_latex": "\\sum F = 0 \\implies v = \\text{constant}",
                    "key_points": [
                        {"label": "Inertial State", "detail": "Objects at rest or uniform motion maintain velocity unless acted on."},
                        {"label": "Equilibrium", "detail": "When net external force equals zero, acceleration is zero."},
                        {"label": "Mass as Inertia", "detail": "Heavier objects require greater net force to accelerate."}
                    ],
                    "diagram_type": "inertia_motion",
                    "highlight_color": "#38bdf8"
                }

        # 4. Computer Science & Algorithms
        elif "binary search" in topic_lower:
            return CSVisualGenerator.get_binary_search_visual()
        elif "search" in topic_lower:
            return {"type":"cs_algorithm_visual","has_simulation":False,"subtype":"search","title":f"Search Strategies: {clean_topic}","key_points":[{"label":"Linear scan","detail":"Inspect elements sequentially."},{"label":"Divide and conquer","detail":"Reduce the search space when ordering permits."},{"label":"Complexity","detail":"Choose a strategy based on constraints."}],"diagram_type":"search_strategy"}
        elif any(k in topic_lower for k in ["tree", "bst"]):
            return {"type":"cs_algorithm_visual","has_simulation":False,"subtype":"tree","title":f"Tree Structures: {clean_topic}","key_points":[{"label":"Root","detail":"Starting node of a tree."},{"label":"Children","detail":"Nodes connected below a parent."},{"label":"Traversal","detail":"Visit nodes systematically using DFS or BFS."}],"diagram_type":"tree_structure"}
        elif any(k in topic_lower for k in ["sort", "sorting"]):
            return {"type":"cs_algorithm_visual","has_simulation":False,"subtype":"sorting","title":f"Sorting Algorithms: {clean_topic}","key_points":[{"label":"Compare","detail":"Algorithms compare elements or keys."},{"label":"Reorder","detail":"Elements move toward the required ordering."},{"label":"Complexity","detail":"Runtime and memory trade-offs matter."}],"diagram_type":"sorting_steps"}
        elif "graph" in topic_lower:
            return {"type":"cs_algorithm_visual","has_simulation":False,"subtype":"graph","title":f"Graph Algorithms: {clean_topic}","key_points":[{"label":"Vertices","detail":"Represent entities or states."},{"label":"Edges","detail":"Represent relationships or transitions."},{"label":"Traversal","detail":"BFS and DFS explore connected structure."}],"diagram_type":"graph_network"}
        elif any(k in topic_lower for k in ["algorithm", "array", "data structure"]):
            return {"type":"cs_algorithm_visual","has_simulation":False,"subtype":"generic","title":f"Algorithmic Model: {clean_topic}","key_points":[{"label":"Input","detail":"Define the data and constraints."},{"label":"Process","detail":"Apply the algorithmic steps."},{"label":"Output","detail":"Verify correctness and complexity."}],"diagram_type":"algorithm_flow"}

        # 5. Mathematics & Equations
        elif any(k in topic_lower for k in ["quadratic", "parabola"]):
            return MathVisualGenerator.get_quadratic_equation_visual()
        elif any(k in topic_lower for k in ["derivative", "differentiation", "calculus"]):
            return {"type":"math_calculus_visual","has_simulation":False,"subtype":"derivative","title":f"Derivative Intuition: {clean_topic}","formula":"dy/dx","formula_latex":"\\frac{dy}{dx}","key_points":[{"label":"Rate of change","detail":"A derivative measures local change."},{"label":"Slope","detail":"Geometrically it is the tangent slope."},{"label":"Applications","detail":"Used for optimization and motion analysis."}],"diagram_type":"derivative_curve"}
        elif any(k in topic_lower for k in ["integral", "integration"]):
            return {"type":"math_calculus_visual","has_simulation":False,"subtype":"integral","title":f"Integration Intuition: {clean_topic}","formula":"∫ f(x) dx","formula_latex":"\\int f(x)\\,dx","key_points":[{"label":"Accumulation","detail":"Integrals accumulate quantities over an interval."},{"label":"Area","detail":"A definite integral can represent signed area."},{"label":"Fundamental theorem","detail":"Differentiation and integration are linked."}],"diagram_type":"integral_area"}
        elif any(k in topic_lower for k in ["algebra", "polynomial", "equation"]):
            return {"type":"math_algebra_visual","has_simulation":False,"subtype":"equation","title":f"Algebraic Relationships: {clean_topic}","key_points":[{"label":"Variables","detail":"Symbols represent unknown or changing values."},{"label":"Operations","detail":"Preserve equality while transforming expressions."},{"label":"Solutions","detail":"Verify candidate values in the original equation."}],"diagram_type":"equation_balance"}

        # 6. Chemistry & Molecular Science
        elif any(k in topic_lower for k in ["periodic table", "element", "atom"]):
            return {"type":"chemistry_atomic_visual","has_simulation":False,"subtype":"atomic_structure","title":f"Atomic Structure: {clean_topic}","key_points":[{"label":"Nucleus","detail":"Contains protons and neutrons."},{"label":"Electrons","detail":"Occupy quantized states around the nucleus."},{"label":"Atomic number","detail":"Equals the number of protons."}],"diagram_type":"atomic_structure"}
        elif any(k in topic_lower for k in ["molecule", "acid", "base", "chemical", "reaction", "bond"]):
            return {
                "type": "chemistry_reaction",
                "has_simulation": False,
                "subtype": "molecular_kinetics",
                "title": f"Molecular Dynamics & Chemical Bonding in {clean_topic}",
                "formula": f"Reactants → Products + ΔE",
                "formula_latex": "\\text{Reactants} \\longrightarrow \\text{Products} + \\Delta H",
                "key_points": [
                    {"label": "Electron Valency", "detail": "Atoms interact via covalent and ionic chemical bonding."},
                    {"label": "Activation Energy", "detail": "Minimum kinetic collision energy required to break bonds."},
                    {"label": "Conservation of Mass", "detail": "Atoms are neither created nor destroyed in chemical changes."}
                ],
                "diagram_type": "molecular_bonds",
                "highlight_color": "#a855f7"
            }

        # 7. Universal Dynamic Topic Visual Engine (Humanities, History, Concepts)
        return {
            "type": "dynamic_concept_model",
            "has_simulation": False,
            "title": f"Core Structural Framework: {concept or clean_topic}",
            "topic": clean_topic,
            "formula": f"Governing Principles of {clean_topic}",
            "key_points": [
                {"label": "Foundational Definition", "detail": f"Fundamental property and mechanism governing {clean_topic}."},
                {"label": "Active Mechanism", "detail": f"Observed parameter interactions and cause-and-effect relationships in {clean_topic}."},
                {"label": "Applied Problem Solving", "detail": f"Direct mathematical, scientific, or practical application of {clean_topic}."}
            ],
            "diagram_type": "conceptual_system_map",
            "highlight_color": "#38bdf8"
        }

