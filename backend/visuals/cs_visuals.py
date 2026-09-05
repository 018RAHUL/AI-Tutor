from typing import Dict, Any, List

class CSVisualGenerator:
    """
    Generates structured visual payloads for Computer Science & Programming concepts.
    Includes Binary Search divide-and-conquer steps, pointer markers, and animated code execution.
    """

    @classmethod
    def get_binary_search_visual(cls) -> Dict[str, Any]:
        return {
            "type": "binary_search_animation",
            "has_simulation": True,
            "title": "Binary Search: Divide and Conquer Execution",
            "target": 23,
            "initial_array": [2, 5, 8, 12, 16, 23, 38],
            "iterations": [
                {
                    "step": 1,
                    "low": 0, "high": 6, "mid": 3,
                    "mid_val": 12,
                    "comparison": "23 > 12",
                    "action": "Target is greater! Eliminate left half [2, 5, 8, 12]. Set low = mid + 1.",
                    "active_range": [4, 6],
                    "eliminated_indices": [0, 1, 2, 3]
                },
                {
                    "step": 2,
                    "low": 4, "high": 6, "mid": 5,
                    "mid_val": 23,
                    "comparison": "23 == 23",
                    "action": "Match found! Target 23 discovered at index 5 in just 2 comparisons.",
                    "active_range": [5, 5],
                    "eliminated_indices": [0, 1, 2, 3, 4, 6],
                    "found": True
                }
            ],
            "code_snippet": """def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid # FOUND!
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1""",
            "time_complexity": "O(log n)"
        }
