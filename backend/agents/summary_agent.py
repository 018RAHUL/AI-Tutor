import json
from typing import Dict, Any, List, Optional
from backend.models.llm_provider import LLMProvider
from backend.models.router import TaskType

class SummaryAgent:
    """
    Autonomous Pedagogical Summarizer Agent.
    Synthesizes multi-tier study materials, executive summaries, formula cheat-sheets,
    interactive active-recall flashcards, and misconception warning boxes.
    """

    @classmethod
    def generate_summary(
        cls,
        topic: str,
        subject: str = "Physics",
        student_level: str = "Beginner",
        scenes: Optional[List[Dict[str, Any]]] = None,
        lesson_plan: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        topic_lower = topic.lower()

        # Expert Grounded Knowledge for Ohm's Law
        if "ohm" in topic_lower or "circuit" in topic_lower or "resistan" in topic_lower:
            return {
                "topic": "Ohm's Law",
                "subject": "Physics & Electrical Engineering",
                "executive_summary": (
                    "Ohm's Law is the foundational principle describing how electric charge moves through a conductor. "
                    "It establishes that the current (I) flowing through a circuit is directly proportional to the applied "
                    "voltage (V) and inversely proportional to the resistance (R). By modeling electric potential as water pressure, "
                    "current as water flow rate, and resistance as pipe constriction, electrical circuits can be analyzed and designed "
                    "with mathematical precision."
                ),
                "core_intuition": "Voltage is the Push, Resistance is the Brake, and Current is the resulting Flow Rate.",
                "key_takeaways": [
                    "Voltage (V, Volts): Electrical potential difference driving charge carriers through the circuit.",
                    "Current (I, Amperes): Rate of electric charge flow (1 Amp = 1 Coulomb per second).",
                    "Resistance (R, Ohms Ω): Material property opposing the flow of electric charges.",
                    "Direct proportionality: Doubling Voltage doubles Current (if Resistance is constant).",
                    "Inverse proportionality: Doubling Resistance cuts Current in half (if Voltage is constant)."
                ],
                "formulas": [
                    {
                        "name": "Standard Ohm's Law",
                        "latex": "V = I \\times R",
                        "formula_text": "V = I * R",
                        "description": "Calculates required voltage given current and resistance.",
                        "units": "Volts (V) = Amperes (A) × Ohms (Ω)"
                    },
                    {
                        "name": "Current Calculation",
                        "latex": "I = \\frac{V}{R}",
                        "formula_text": "I = V / R",
                        "description": "Calculates resulting flow rate through a given resistance.",
                        "units": "Amperes (A) = Volts (V) / Ohms (Ω)"
                    },
                    {
                        "name": "Resistance Calculation",
                        "latex": "R = \\frac{V}{I}",
                        "formula_text": "R = V / I",
                        "description": "Determines the opposition to current flow in a component.",
                        "units": "Ohms (Ω) = Volts (V) / Amperes (A)"
                    },
                    {
                        "name": "Electrical Power Dissipation",
                        "latex": "P = V \\times I = I^2 R = \\frac{V^2}{R}",
                        "formula_text": "P = V * I = I^2 * R = V^2 / R",
                        "description": "Rate of energy converted into heat or work.",
                        "units": "Watts (W)"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "What is the SI unit of electric current and what does it represent?",
                        "answer": "The Ampere (A). It represents the rate of charge flow: 1 Ampere = 1 Coulomb of charge passing per second.",
                        "hint": "Think about flow rate per second.",
                        "difficulty": "Easy",
                        "category": "Definitions"
                    },
                    {
                        "id": "fc_2",
                        "question": "If Voltage is held constant at 12V and Resistance increases from 4Ω to 8Ω, what happens to Current?",
                        "answer": "Current decreases from 3A down to 1.5A because I = V / R (inverse relationship).",
                        "hint": "Use I = V / R. Higher denominator means smaller result.",
                        "difficulty": "Medium",
                        "category": "Application"
                    },
                    {
                        "id": "fc_3",
                        "question": "In the mechanical water pipe analogy, what physical elements correspond to V, I, and R?",
                        "answer": "Voltage = Water pump pressure; Current = Volume flow rate of water; Resistance = Pipe constriction or filter narrowing.",
                        "hint": "Pump, flow volume, narrow pipe.",
                        "difficulty": "Easy",
                        "category": "Analogies"
                    },
                    {
                        "id": "fc_4",
                        "question": "Why does a short circuit (near zero resistance) cause wires to rapidly overheat?",
                        "answer": "As R approaches 0 with finite V, current I = V/R becomes extremely large. High current generates massive thermal dissipation (P = I²R).",
                        "hint": "Very low resistance yields very high current.",
                        "difficulty": "Hard",
                        "category": "Safety & Physics"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Believing Current increases when Resistance increases.",
                        "correction": "Resistance opposes current. Increasing resistance restricts charge movement, thereby reducing current (I = V/R).",
                        "severity": "High"
                    },
                    {
                        "misconception": "Thinking electrical current is consumed or 'used up' by resistors.",
                        "correction": "Charge is conserved! The same current that enters a resistor exits it; what is consumed is electrical potential energy (voltage drops).",
                        "severity": "Medium"
                    },
                    {
                        "misconception": "Confusing Voltage with Current.",
                        "correction": "Voltage is the potential push across two points; Current is the actual movement of charge through a point.",
                        "severity": "High"
                    }
                ],
                "worked_example_recap": {
                    "title": "12V Battery with 4Ω Heating Resistor",
                    "given": "V = 12V, R = 4Ω",
                    "target": "Find current I",
                    "steps": [
                        "1. State formula: I = V / R",
                        "2. Substitute knowns: I = 12V / 4Ω",
                        "3. Compute: I = 3.0 Amperes (A)"
                    ],
                    "verification": "Check: V = I * R = 3A * 4Ω = 12V (Matches battery voltage)."
                }
            }

        # 2. Photosynthesis & Botany / Biology
        elif any(k in topic_lower for k in ["photosynthesis", "chloroplast", "plant", "chlorophyll", "light reaction", "calvin", "biology"]):
            return {
                "topic": "Photosynthesis",
                "subject": "Biology & Plant Biochemistry",
                "executive_summary": (
                    "Photosynthesis is the fundamental biological engine converting solar light energy into chemical energy stored in glucose. "
                    "In the thylakoid membranes, chlorophyll captures photons to split water molecules (photolysis), releasing oxygen (O2) and generating ATP/NADPH. "
                    "In the stroma, the Calvin Cycle fixes atmospheric carbon dioxide (CO2) to synthesize glucose (C6H12O6)."
                ),
                "core_intuition": "Plants harness solar photons to split water, release oxygen, and assemble carbon dioxide into high-energy sugars.",
                "key_takeaways": [
                    "Balanced chemical equation: 6 CO2 + 6 H2O + Light energy ⟶ C6H12O6 (Glucose) + 6 O2.",
                    "Light-dependent reactions occur in Thylakoids; Light-independent Calvin Cycle occurs in Stroma.",
                    "Released oxygen comes directly from the photolysis of water (H2O), not carbon dioxide.",
                    "Chlorophyll pigment absorbs blue (430 nm) and red (660 nm) wavelengths, reflecting green light.",
                    "Photosynthesis is the ecological foundation of virtually all aerobic life on Earth."
                ],
                "formulas": [
                    {
                        "name": "Overall Photosynthesis Equation",
                        "latex": "6\\text{CO}_2 + 6\\text{H}_2\\text{O} + h\\nu \\longrightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2",
                        "formula_text": "6CO2 + 6H2O + Light -> C6H12O6 + 6O2",
                        "description": "Balanced net stoichiometric biochemical reaction.",
                        "units": "Molar ratio"
                    },
                    {
                        "name": "Water Photolysis (Light Reaction)",
                        "latex": "2\\text{H}_2\\text{O} \\longrightarrow 4\\text{H}^+ + 4e^- + \\text{O}_2",
                        "formula_text": "2H2O -> 4H+ + 4e- + O2",
                        "description": "Splitting of water under solar excitation releasing oxygen.",
                        "units": "Electrons / Protons"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "Where does the oxygen released by plants during photosynthesis come from?",
                        "answer": "From the photolysis (splitting) of water (H2O) molecules in the thylakoid membranes.",
                        "hint": "Water, not CO2.",
                        "difficulty": "Easy",
                        "category": "Light Reactions"
                    },
                    {
                        "id": "fc_2",
                        "question": "What is the primary role of the Calvin Cycle and where does it occur?",
                        "answer": "It fixes atmospheric CO2 into glucose (C6H12O6) using ATP and NADPH, taking place in the chloroplast stroma.",
                        "hint": "Stroma, carbon fixation.",
                        "difficulty": "Medium",
                        "category": "Dark Reactions"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Believing oxygen is released by splitting carbon dioxide (CO2).",
                        "correction": "Oxygen gas (O2) is produced exclusively from splitting water (H2O) during the light reactions.",
                        "severity": "High"
                    },
                    {
                        "misconception": "Thinking the Calvin Cycle only happens at night.",
                        "correction": "The Calvin Cycle is light-independent, but requires ATP and NADPH produced during daylight.",
                        "severity": "Medium"
                    }
                ],
                "worked_example_recap": {
                    "title": "Stoichiometry of Photosynthesis",
                    "given": "6 moles CO2 + 6 moles H2O + Sunlight",
                    "target": "Synthesize Glucose and Oxygen",
                    "steps": [
                        "1. Absorb 6 CO2 molecules from atmosphere",
                        "2. Split 6 H2O molecules in thylakoids yielding 6 O2",
                        "3. Assemble 1 Glucose molecule (C6H12O6)"
                    ],
                    "verification": "All 6 Carbon, 12 Hydrogen, and 18 Oxygen atoms are fully balanced."
                }
            }

        # 3. Newton's Laws & Classical Mechanics
        elif any(k in topic_lower for k in ["newton", "force", "gravity", "gravitation", "motion", "inertia", "acceleration"]):
            return {
                "topic": "Newton's Laws of Motion",
                "subject": "Classical Mechanics & Physics",
                "executive_summary": (
                    "Sir Isaac Newton's three universal laws form the bedrock of classical dynamics. "
                    "The First Law defines inertia (resistance to velocity changes). "
                    "The Second Law establishes that net force equals mass times acceleration (F = ma). "
                    "The Third Law states all forces exist in simultaneous, equal, and opposite action-reaction pairs."
                ),
                "core_intuition": "Force is the interaction causing acceleration; acceleration is proportional to net force and inversely proportional to mass.",
                "key_takeaways": [
                    "1st Law (Inertia): Objects at rest stay at rest; objects in motion remain at constant velocity unless acted on by net external force.",
                    "2nd Law (F = ma): Net force drives proportional acceleration: a = F_net / m.",
                    "3rd Law (Action-Reaction): Whenever body A exerts a force on body B, body B exerts an equal and opposite force on body A.",
                    "Doubling applied force doubles acceleration; doubling mass cuts acceleration in half.",
                    "Weight is a force: W = m * g (where g ≈ 9.8 m/s² on Earth)."
                ],
                "formulas": [
                    {
                        "name": "Newton's Second Law",
                        "latex": "F_{\\text{net}} = m \\times a",
                        "formula_text": "F = m * a",
                        "description": "Calculates net force required for acceleration.",
                        "units": "Newtons (N) = kg · m/s²"
                    },
                    {
                        "name": "Acceleration Form",
                        "latex": "a = \\frac{F_{\\text{net}}}{m}",
                        "formula_text": "a = F / m",
                        "description": "Determines dynamic acceleration from net force and mass.",
                        "units": "m/s²"
                    },
                    {
                        "name": "Action-Reaction Law",
                        "latex": "F_{AB} = -F_{BA}",
                        "formula_text": "F_AB = -F_BA",
                        "description": "Simultaneous mutual interaction forces between two bodies.",
                        "units": "Newtons (N)"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "If you double the mass of an object while keeping net force constant, what happens to its acceleration?",
                        "answer": "Acceleration is halved (a = F / 2m = 0.5a) due to increased inertia.",
                        "hint": "a = F / m. Mass is in denominator.",
                        "difficulty": "Easy",
                        "category": "Dynamics"
                    },
                    {
                        "id": "fc_2",
                        "question": "Why don't action and reaction force pairs cancel each other out?",
                        "answer": "Because they act on two different objects simultaneously, not the same object.",
                        "hint": "Two distinct bodies.",
                        "difficulty": "Medium",
                        "category": "Newton's Third Law"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Believing a continuous force is needed to keep an object moving at constant speed.",
                        "correction": "Newton's 1st Law states motion continues indefinitely at constant velocity unless opposing friction/forces exist.",
                        "severity": "High"
                    },
                    {
                        "misconception": "Confusing mass (inertia, kg) with weight (gravitational force, N).",
                        "correction": "Mass is constant everywhere; weight depends on local gravitational acceleration (W = mg).",
                        "severity": "High"
                    }
                ],
                "worked_example_recap": {
                    "title": "Rocket Thrust Acceleration",
                    "given": "Thrust F = 2500 N, Mass m = 500 kg",
                    "target": "Calculate acceleration a",
                    "steps": [
                        "1. State formula: a = F / m",
                        "2. Substitute: a = 2500 / 500",
                        "3. Compute: a = 5.0 m/s²"
                    ],
                    "verification": "Check: F = m * a = 500 kg * 5.0 m/s² = 2500 N."
                }
            }

        # 5. Agentic AI & Autonomous Architectures
        elif any(k in topic_lower for k in ["agentic", "autonomous agent", "ai agent", "react agent", "tool calling"]):
            return {
                "topic": "Agentic AI & Autonomous Architectures",
                "subject": "Computer Science & Artificial Intelligence",
                "executive_summary": (
                    "Agentic AI represents a paradigm shift from static, single-turn language models to goal-driven autonomous systems. "
                    "By combining the reasoning power of LLMs with structured cognitive frameworks (such as the ReAct loop), external tool invocation, "
                    "and multi-tier memory (short-term scratchpads and long-term vector stores), AI agents can independently decompose complex objectives, "
                    "interact with sandboxed environments, evaluate feedback, and self-correct to complete multi-step tasks."
                ),
                "core_intuition": "Traditional LLMs generate text; Agentic AI reasons, takes action via tools, observes the environment, and iterates until the goal is accomplished.",
                "key_takeaways": [
                    "ReAct Paradigm: Interleaving Thought, Action (tool call with JSON schema), and Observation (environment feedback).",
                    "Dual-Tier Memory: Short-term conversational context buffers combined with long-term vector embeddings for episodic retrieval.",
                    "Function Calling: Strict JSON schema parameter validation ensuring deterministic interaction with external APIs.",
                    "Self-Correction & Reflection: Evaluating failed tool executions and dynamically refactoring intermediate action plans.",
                    "Stateful Multi-Agent Swarms: Orchestrating specialized agent roles (e.g., Planner, Coder, Reviewer) using state graph architectures (LangGraph)."
                ],
                "formulas": [
                    {
                        "name": "Agent Cognitive Cycle",
                        "latex": "\\text{State}_{t+1} = \\text{Agent}(\\text{Perception}_t, \\text{Memory}_t, \\mathcal{T}) \\implies \\text{Action}_{t+1}",
                        "formula_text": "Agent Cycle: Perception(State) -> Reason & Plan(LLM) -> Action(Tools) -> Observation(Feedback)",
                        "description": "Fundamental closed-loop control cycle for autonomous agents.",
                        "units": "State Transition"
                    },
                    {
                        "name": "Tool Schema Invocation",
                        "latex": "a_t = \\text{ToolCall}(\\text{name} = f, \\text{args} = \\theta \\in \\text{JSONSchema})",
                        "formula_text": "Action_t = ToolCall(name=f, args=JSON_Schema)",
                        "description": "Deterministic tool execution mapping LLM tokens to executable functions.",
                        "units": "Structured Payload"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "What is the core difference between a standard LLM chatbot and an Agentic AI system?",
                        "answer": "A standard LLM is open-loop (one prompt -> one response), while an AI Agent operates in a closed loop: it plans, invokes external tools, observes feedback, and iterates until the goal is solved.",
                        "hint": "Closed-loop feedback and tool execution.",
                        "difficulty": "Easy",
                        "category": "Core Concepts"
                    },
                    {
                        "id": "fc_2",
                        "question": "How does the ReAct framework improve tool-calling reliability?",
                        "answer": "By forcing the agent to output an explicit reasoning step ('Thought') before generating the tool call ('Action'), preventing premature or erroneous function calls.",
                        "hint": "Reason before acting.",
                        "difficulty": "Medium",
                        "category": "Cognitive Architectures"
                    },
                    {
                        "id": "fc_3",
                        "question": "Why is short-term context window insufficient for complex multi-day agent workflows?",
                        "answer": "Context windows have fixed token limits and suffer from attention degradation. Agents require long-term vector stores for semantic memory search across sessions.",
                        "hint": "Token limits and semantic embeddings.",
                        "difficulty": "Hard",
                        "category": "Memory Systems"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Assuming AI agents have unbounded autonomy and require zero human oversight or sandboxing.",
                        "correction": "Agents must operate within deterministic sandbox boundaries with rate limits, permission checks, and human-in-the-loop approvals for sensitive actions.",
                        "severity": "High"
                    },
                    {
                        "misconception": "Confusing standard Prompt Engineering with Agentic State Management.",
                        "correction": "Prompting is static text formatting; agent architecture requires stateful graph persistence, tool schemas, and error recovery loops.",
                        "severity": "Medium"
                    }
                ],
                "worked_example_recap": {
                    "title": "Autonomous Stock Volatility & Reporting Agent",
                    "given": "Goal: 'Fetch AAPL 30-day prices, calculate standard deviation, and email report.'",
                    "target": "Multi-step autonomous execution trajectory",
                    "steps": [
                        "1. Thought: 'I need historical prices.' Action: StockAPI(ticker='AAPL', days=30)",
                        "2. Observation: Receives array of 30 price points. Thought: 'Run statistical analysis in Python.'",
                        "3. Action: PythonREPL('import numpy as np; vol = np.std(prices); print(vol)')",
                        "4. Observation: 'vol = 2.45%'. Thought: 'Analysis complete. Emailing summary.' Action: EmailAPI(body=summary)"
                    ],
                    "verification": "All tool schema parameters verified; execution terminated with Goal Completed."
                }
            }

        # 6. Quantum Computing & Quantum Mechanics
        elif any(k in topic_lower for k in ["quantum", "qubit", "superposition", "entanglement", "bloch", "schrodinger"]):
            return {
                "topic": "Quantum Computing & Superposition",
                "subject": "Quantum Information Science & Physics",
                "executive_summary": (
                    "Quantum computing leverages the fundamental principles of quantum mechanics—namely Superposition and Entanglement—to process "
                    "information in ways exponentially more powerful than classical binary computation. A classical bit is deterministically 0 or 1, "
                    "whereas a quantum bit (Qubit) exists in a continuous linear superposition of states |0⟩ and |1⟩ on the Bloch Sphere until measurement collapses its state."
                ),
                "core_intuition": "Classical bits are like a coin flat on a table (Heads or Tails); a qubit is like a spinning coin, existing in a continuous superposition until caught.",
                "key_takeaways": [
                    "Qubit State: |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex probability amplitudes.",
                    "Normalization Constraint: |α|² + |β|² = 1 (sum of measurement probabilities equals 100%).",
                    "Bloch Sphere: Geometric representation of a 2-level quantum system where pure states lie on the unit sphere surface.",
                    "Hadamard Gate (H): Transforms pure basis states |0⟩ into equal superposition (|0⟩ + |1⟩)/√2.",
                    "Wavefunction Collapse: Measurement forces the qubit probabilistically into |0⟩ or |1⟩ with probabilities |α|² and |β|²."
                ],
                "formulas": [
                    {
                        "name": "Qubit Superposition State",
                        "latex": "|\\psi\\rangle = \\alpha |0\\rangle + \\beta |1\\rangle",
                        "formula_text": "|psi> = alpha|0> + beta|1>",
                        "description": "Linear combination of computational basis states.",
                        "units": "Quantum State Vector"
                    },
                    {
                        "name": "Born Rule Normalization",
                        "latex": "|\\alpha|^2 + |\\beta|^2 = 1",
                        "formula_text": "|alpha|^2 + |beta|^2 = 1",
                        "description": "Total probability conservation across all basis outcomes.",
                        "units": "Probability [0, 1]"
                    },
                    {
                        "name": "Hadamard Transformation",
                        "latex": "H |0\\rangle = \\frac{|0\\rangle + |1\\rangle}{\\sqrt{2}}",
                        "formula_text": "H|0> = (|0> + |1>) / sqrt(2)",
                        "description": "Creates maximum quantum superposition with 50/50 probability.",
                        "units": "Unitary Operator"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "What is the physical meaning of |α|² in the qubit state |ψ⟩ = α|0⟩ + β|1⟩?",
                        "answer": "It represents the exact probability of measuring the qubit in the basis state |0⟩ upon wavefunction collapse.",
                        "hint": "Born rule probability.",
                        "difficulty": "Easy",
                        "category": "Quantum Foundations"
                    },
                    {
                        "id": "fc_2",
                        "question": "If α = 1/√2 and β = 1/√2, what is the probability of measuring state |1⟩?",
                        "answer": "P(|1⟩) = |β|² = (1/√2)² = 1/2 = 50%.",
                        "hint": "Square the magnitude of β.",
                        "difficulty": "Medium",
                        "category": "Measurement"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Believing a qubit in superposition is simply 'secretly 0 or 1' before measurement.",
                        "correction": "Superposition is a genuine physical wave interference state; it is simultaneously in a linear combination until physical measurement forces collapse.",
                        "severity": "High"
                    }
                ],
                "worked_example_recap": {
                    "title": "Applying Hadamard Gate to Ground State Qubit",
                    "given": "Initial Qubit: |ψ⟩ = |0⟩ (α = 1, β = 0)",
                    "target": "Calculate final state after Hadamard gate H",
                    "steps": [
                        "1. State operator: H = (1/√2) [[1, 1], [1, -1]]",
                        "2. Matrix product: H [[1], [0]] = (1/√2) [[1], [1]]",
                        "3. Final state: |ψ'⟩ = (1/√2)|0⟩ + (1/√2)|1⟩"
                    ],
                    "verification": "Normalization check: (1/√2)² + (1/√2)² = 1/2 + 1/2 = 1.0 (Valid)."
                }
            }

        # 7. LangChain, RAG & Vector Architectures
        elif any(k in topic_lower for k in ["langchain", "rag", "retrieval augmented", "vector database", "embedding"]):
            return {
                "topic": "LangChain & RAG Architectures",
                "subject": "Computer Science & Information Retrieval",
                "executive_summary": (
                    "Retrieval-Augmented Generation (RAG) bridges the knowledge gap of static LLMs by dynamically fetching verified external documents. "
                    "Source documents are cleaned, chunked into semantically coherent segments, converted to high-dimensional dense vector embeddings, "
                    "and stored in a vector index. At query time, cosine similarity retrieves the top-k relevant chunks to ground the LLM prompt with zero hallucination."
                ),
                "core_intuition": "RAG gives an LLM an open-book exam: instead of relying purely on memorized training data, it searches your verified documents before answering.",
                "key_takeaways": [
                    "Document Processing: Recursive chunking (500-1000 tokens) with overlap (10-20%) preserves semantic context across split boundaries.",
                    "Dense Embeddings: Neural embedding models map text chunks into high-dimensional vector spaces (e.g., 1536-D).",
                    "Cosine Similarity: Measures directional semantic alignment: sim(u, v) = (u · v) / (||u|| ||v||).",
                    "Context Grounding: Injecting retrieved passages into the system prompt eliminates knowledge cutoff limitations and hallucinations.",
                    "LangChain / LangGraph: Modular chains and stateful directed cyclic graphs coordinating retrievers, parsers, and generation agents."
                ],
                "formulas": [
                    {
                        "name": "Cosine Similarity",
                        "latex": "\\text{CosineSim}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\| \\|\\mathbf{v}\\|}",
                        "formula_text": "Cosine_Sim(u, v) = (u . v) / (||u|| * ||v||)",
                        "description": "Calculates semantic closeness between query vector and document chunks.",
                        "units": "Similarity Score [-1, 1]"
                    }
                ],
                "flashcards": [
                    {
                        "id": "fc_1",
                        "question": "Why is chunk overlap essential when preparing documents for RAG?",
                        "answer": "Overlap ensures sentences that cross chunk boundaries retain their full semantic context, preventing critical information loss.",
                        "hint": "Context preservation across splits.",
                        "difficulty": "Easy",
                        "category": "Ingestion"
                    }
                ],
                "common_pitfalls": [
                    {
                        "misconception": "Assuming RAG requires fine-tuning or re-training the base LLM.",
                        "correction": "RAG requires zero model weight training; knowledge is injected directly at runtime through in-context prompting.",
                        "severity": "High"
                    }
                ],
                "worked_example_recap": {
                    "title": "Cosine Similarity Document Matching",
                    "given": "Query vector u = [0.6, 0.8], Chunk vector v = [0.6, 0.8]",
                    "target": "Compute similarity score",
                    "steps": [
                        "1. Dot product: 0.6(0.6) + 0.8(0.8) = 0.36 + 0.64 = 1.0",
                        "2. Norms: ||u|| = √(0.36+0.64) = 1.0, ||v|| = 1.0",
                        "3. Cosine Sim = 1.0 / (1.0 * 1.0) = 1.0 (Exact Semantic Match)"
                    ],
                    "verification": "Score = 1.0 indicates identical directional semantic alignment."
                }
            }

        # 8. Dynamic Grounding using LLMProvider Knowledge Graph for ANY Unseen Topic
        kg = LLMProvider.get_topic_knowledge_graph(topic)
        clean_topic = kg.get("topic", topic)
        clean_subject = kg.get("subject", subject)
        formula_text = kg.get("formula", f"Governing Principle of {clean_topic}")
        formula_latex = kg.get("formula_latex", "\\text{Output} = f(\\text{Input})")
        intuition = kg.get("core_intuition", f"Master the foundational cause-and-effect relationship driving {clean_topic}.")
        we = kg.get("worked_example", {})
        chk = kg.get("checkpoint", {})

        return {
            "topic": clean_topic,
            "subject": clean_subject,
            "executive_summary": (
                f"{clean_topic} is a vital domain in {clean_subject}. Understanding its foundational architecture, "
                f"governing principles, and boundary conditions enables rigorous analytical problem solving. "
                f"When key input parameters interact within the system, they generate deterministic, predictable state transformations."
            ),
            "core_intuition": intuition,
            "key_takeaways": kg.get("learning_objectives", [
                f"Foundational taxonomy and conceptual architecture of {clean_topic}.",
                f"Governing relationship and mathematical/logical formulations.",
                f"Analysis of operational parameters, bottlenecks, and boundary conditions.",
                f"Step-by-step application of primary principles to solve real scenarios.",
                "Systematic validation and verification of verified outputs."
            ]),
            "formulas": [
                {
                    "name": f"Governing Law of {clean_topic}",
                    "latex": formula_latex,
                    "formula_text": formula_text,
                    "description": f"Core relationship governing dynamic behavior in {clean_topic}.",
                    "units": "Verified SI / Computational Units"
                }
            ],
            "flashcards": [
                {
                    "id": "fc_1",
                    "question": chk.get("question", f"What is the central governing mechanism of {clean_topic}?"),
                    "answer": chk.get("expected_answer", f"A systematic cause-and-effect relationship governed by physical principles."),
                    "hint": intuition[:60],
                    "difficulty": "Easy",
                    "category": "Core Principle"
                },
                {
                    "id": "fc_2",
                    "question": f"How do the input parameters directly influence the state in {clean_topic}?",
                    "answer": f"Through deterministic transformations defined by {formula_text}.",
                    "hint": "Check governing formula.",
                    "difficulty": "Medium",
                    "category": "Parameter Analysis"
                }
            ],
            "common_pitfalls": [
                {
                    "misconception": chk.get("misconception", f"Treating {clean_topic} as random or unconnected to its governing rules."),
                    "correction": chk.get("feedback", f"Outputs in {clean_topic} are determined systematically by interacting variables and boundary constraints."),
                    "severity": "High"
                }
            ],
            "worked_example_recap": {
                "title": we.get("title", f"Applied Problem Solving in {clean_topic}"),
                "given": we.get("given", "Initial operational parameters defined"),
                "target": "Derive verified output state",
                "steps": we.get("steps", [
                    f"1. Extract active input variables in {clean_topic}",
                    "2. Apply foundational governing relationship to compute transformation",
                    "3. Validate output consistency with physical conservation laws"
                ]),
                "verification": we.get("solution", "Verified output state achieved.")
            }
        }

    @classmethod
    def generate_markdown_notes(cls, summary_data: Dict[str, Any]) -> str:
        topic = summary_data.get("topic", "Study Notes")
        subject = summary_data.get("subject", "General")
        exec_sum = summary_data.get("executive_summary", "")
        intuition = summary_data.get("core_intuition", "")
        takeaways = summary_data.get("key_takeaways", [])
        formulas = summary_data.get("formulas", [])
        pitfalls = summary_data.get("common_pitfalls", [])
        worked = summary_data.get("worked_example_recap", {})

        md = []
        md.append(f"# 📚 {topic} — AI Study Master Summary")
        md.append(f"**Subject:** {subject} | **Generated by:** AI Teacher Autonomous Pedagogical Agent\n")
        md.append("## 💡 Executive Summary")
        md.append(exec_sum)
        if intuition:
            md.append(f"\n> **Core Intuition:** *{intuition}*\n")

        md.append("## 🔑 Key Takeaways")
        for t in takeaways:
            md.append(f"- {t}")

        if formulas:
            md.append("\n## 📐 Key Formulas & Mathematical Laws")
            for f in formulas:
                md.append(f"### {f.get('name')}")
                md.append(f"$$\n{f.get('latex', f.get('formula_text'))}\n$$")
                md.append(f"- **Formula:** `{f.get('formula_text')}`")
                md.append(f"- **Description:** {f.get('description')}")
                md.append(f"- **Units:** {f.get('units')}\n")

        if pitfalls:
            md.append("## ⚠️ Common Pitfalls & Misconceptions")
            for p in pitfalls:
                md.append(f"- **Misconception:** {p.get('misconception')}")
                md.append(f"  - *Correction:* {p.get('correction')} *(Severity: {p.get('severity')})*")

        if worked:
            md.append(f"\n## ✍️ Worked Example: {worked.get('title')}")
            md.append(f"- **Given:** {worked.get('given')}")
            md.append(f"- **Target:** {worked.get('target')}")
            md.append("- **Steps:**")
            for step in worked.get("steps", []):
                md.append(f"  - {step}")
            if worked.get("verification"):
                md.append(f"- **Verification:** {worked.get('verification')}")

        return "\n".join(md)
