from typing import Dict, Any, List

class MathVisualGenerator:
    """
    Generates rich structured visual payloads for Mathematics concepts,
    including Quadratic Equations, coordinate graphing, and step-by-step substitutions.
    """

    @classmethod
    def get_quadratic_equation_visual(cls) -> Dict[str, Any]:
        return {
            "type": "math_quadratic_visual",
            "has_simulation": True,
            "title": "Quadratic Equations: Parabolic Curves and Roots",
            "standard_form": "ax^2 + bx + c = 0",
            "quadratic_formula": "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}",
            "worked_example": {
                "equation": "x^2 - 5x + 6 = 0",
                "coefficients": {"a": 1, "b": -5, "c": 6},
                "discriminant": "(-5)^2 - 4(1)(6) = 25 - 24 = 1",
                "roots": ["x_1 = 3", "x_2 = 2"],
                "vertex": "(2.5, -0.25)"
            },
            "graph_points": [
                {"x": 0, "y": 6},
                {"x": 1, "y": 2},
                {"x": 2, "y": 0, "is_root": True},
                {"x": 2.5, "y": -0.25, "is_vertex": True},
                {"x": 3, "y": 0, "is_root": True},
                {"x": 4, "y": 2},
                {"x": 5, "y": 6}
            ]
        }
