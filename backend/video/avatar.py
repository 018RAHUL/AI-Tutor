from typing import Dict, Any, List

class AvatarController:
    """
    Teacher Avatar State and Expression Controller.
    Manages facial states, visemes, idle micro-animations, and responsiveness.
    """

    STATES = {
        "IDLE": {"expression": "neutral", "eye_state": "open", "blink_rate_sec": 3.5, "head_tilt": 0.0, "mouth_base": "closed"},
        "SPEAKING": {"expression": "engaged", "eye_state": "focused", "blink_rate_sec": 4.0, "head_tilt": 2.0, "mouth_base": "phoneme_active"},
        "EXPLAINING": {"expression": "enthusiastic", "eye_state": "focused", "blink_rate_sec": 4.5, "head_tilt": -3.0, "mouth_base": "phoneme_active"},
        "QUESTIONING": {"expression": "curious_inquisitive", "eye_state": "wide", "blink_rate_sec": 5.0, "head_tilt": 5.0, "mouth_base": "gentle_smile"},
        "LISTENING": {"expression": "attentive", "eye_state": "focused", "blink_rate_sec": 3.0, "head_tilt": 4.0, "mouth_base": "closed"},
        "THINKING": {"expression": "analytical", "eye_state": "squint_up", "blink_rate_sec": 6.0, "head_tilt": -6.0, "mouth_base": "closed"},
        "CORRECT": {"expression": "delighted_proud", "eye_state": "smiling_eyes", "blink_rate_sec": 3.5, "head_tilt": 2.0, "mouth_base": "warm_smile"},
        "MISCONCEPTION": {"expression": "empathetic_concern", "eye_state": "soft_wide", "blink_rate_sec": 3.0, "head_tilt": -4.0, "mouth_base": "slight_o"},
        "RE_EXPLAINING": {"expression": "encouraging_clear", "eye_state": "supportive", "blink_rate_sec": 4.0, "head_tilt": 3.0, "mouth_base": "phoneme_active"}
    }

    @classmethod
    def get_state_config(cls, state_name: str) -> Dict[str, Any]:
        return cls.STATES.get(state_name.upper(), cls.STATES["SPEAKING"])
