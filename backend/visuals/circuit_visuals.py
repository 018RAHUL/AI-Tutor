from typing import Dict, Any, List

class CircuitVisualGenerator:
    """
    Generates rich deterministic visual payloads for electrical circuits and Ohm's Law.
    Includes circuit schematics with moving charges, water pipe analogy,
    and step-by-step formula derivations.
    """

    @classmethod
    def get_intro_visual(cls) -> Dict[str, Any]:
        return {
            "type": "circuit_intro",
            "has_simulation": True,
            "title": "Introduction to Electrical Circuits",
            "components": [
                {"type": "battery", "label": "Voltage Source (V)", "value": "12V", "x": 100, "y": 200},
                {"type": "resistor", "label": "Load / Resistor (R)", "value": "4 Ω", "x": 400, "y": 200},
                {"type": "wire_loop", "status": "closed", "current_flow": "active"}
            ],
            "animation": {
                "particle_speed": 1.0,
                "particle_color": "#38bdf8",
                "particle_count": 24,
                "highlight_component": "battery"
            },
            "callout": "Every closed circuit requires a driving energy source (Voltage) and a path for charge flow (Current)."
        }

    @classmethod
    def get_water_analogy_visual(cls) -> Dict[str, Any]:
        return {
            "type": "water_analogy",
            "has_simulation": True,
            "title": "The Water Pipe Physical Analogy",
            "subsections": [
                {
                    "name": "Water Pump (Voltage)",
                    "icon": "water_pump",
                    "analogy": "Pump Pressure pushing water = Electric Voltage pushing electrons",
                    "color": "#38bdf8",
                    "pressure_level": 80
                },
                {
                    "name": "Water Flow (Current)",
                    "icon": "flow_rate",
                    "analogy": "Gallons of water passing per second = Amperes of charge flowing",
                    "color": "#4ade80",
                    "flow_rate": 60
                },
                {
                    "name": "Pipe Constriction (Resistance)",
                    "icon": "valve_constriction",
                    "analogy": "Narrow pipe / pebbles opposing water = Resistor opposing electron flow",
                    "color": "#f87171",
                    "resistance_width": 20
                }
            ],
            "animation": {
                "pipe_state": "flowing",
                "flow_speed": 1.2,
                "pinch_factor": 0.4
            },
            "formula_banner": "Pressure (V) = Flow Rate (I) × Pipe Restriction (R)"
        }

    @classmethod
    def get_formula_breakdown_visual(cls) -> Dict[str, Any]:
        return {
            "type": "math_formula_interactive",
            "has_simulation": True,
            "title": "Ohm's Law: Mathematical Formulation",
            "main_equation": "V = I \\times R",
            "variables": [
                {"symbol": "V", "name": "Voltage", "unit": "Volts (V)", "role": "Electrical Potential Difference (The Push)", "color": "#38bdf8"},
                {"symbol": "I", "name": "Current", "unit": "Amperes (A)", "role": "Flow Rate of Electric Charge", "color": "#4ade80"},
                {"symbol": "R", "name": "Resistance", "unit": "Ohms (Ω)", "role": "Opposition to Current Flow", "color": "#f87171"}
            ],
            "derived_forms": [
                {"form": "I = \\frac{V}{R}", "description": "Current is directly proportional to Voltage and inversely proportional to Resistance."},
                {"form": "R = \\frac{V}{I}", "description": "Resistance is the ratio of Voltage applied to Current produced."}
            ],
            "triangle_mnemonic": {
                "top": "V",
                "bottom_left": "I",
                "bottom_right": "R"
            }
        }

    @classmethod
    def get_worked_example_visual(cls) -> Dict[str, Any]:
        return {
            "type": "worked_example",
            "has_simulation": True,
            "title": "Worked Example: Calculating Circuit Current",
            "given": {"Voltage (V)": "12 V", "Resistance (R)": "4 Ω"},
            "target": "Find Current (I)",
            "steps": [
                {"step_num": 1, "formula": "I = \\frac{V}{R}", "explanation": "Select Ohm's Law solved for Current."},
                {"step_num": 2, "substitution": "I = \\frac{12\\text{ V}}{4\\text{ }\\Omega}", "explanation": "Substitute given values into the equation."},
                {"step_num": 3, "calculation": "I = 3\\text{ A}", "explanation": "Divide 12 by 4 to obtain the result in Amperes.", "highlight": True}
            ],
            "circuit_diagram": {
                "voltage": 12,
                "resistance": 4,
                "calculated_current": 3,
                "meter_reading": "3.00 A"
            }
        }

    @classmethod
    def get_remediation_visual(cls) -> Dict[str, Any]:
        return {
            "type": "circuit_remediation",
            "has_simulation": True,
            "title": "Misconception Clarification: Why Resistance Reduces Current",
            "comparison": [
                {
                    "case": "Initial Circuit (R = 4 Ω)",
                    "voltage": "12V",
                    "resistance": "4 Ω",
                    "current": "3.0 A",
                    "particle_speed": "Normal (Fast Flow)",
                    "pipe_width": "Wide Open"
                },
                {
                    "case": "Doubled Resistance (R = 8 Ω)",
                    "voltage": "12V",
                    "resistance": "8 Ω",
                    "current": "1.5 A",
                    "particle_speed": "Half Speed (Restricted Flow)",
                    "pipe_width": "Narrowed Constriction"
                }
            ],
            "key_takeaway": "Because I = V / R, increasing the denominator (Resistance) ALWAYS reduces the resulting Current!"
        }
