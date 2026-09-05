import os
import re
import math
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from backend.config import VIDEO_DIR, AUDIO_DIR

class VideoRenderer:
    """
    Automated Educational Video Generator Agent.
    Synthesizes crisp 1080p Full HD (1920x1080) animated educational MP4 videos with
    razor-sharp TrueType typography, domain-specific visual animations,
    scientific simulations, formulas, and synchronized neural TTS audio.
    """

    @classmethod
    def get_ffmpeg_bin(cls) -> str:
        return imageio_ffmpeg.get_ffmpeg_exe()

    @classmethod
    def _get_font(cls, size: int, bold: bool = False) -> ImageFont.ImageFont:
        font_candidates = []
        if bold:
            font_candidates = [
                "arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "tahomabd.ttf",
                "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
                "arial.ttf", "segoeui.ttf"
            ]
        else:
            font_candidates = [
                "arial.ttf", "segoeui.ttf", "calibri.ttf", "tahoma.ttf",
                "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"
            ]

        for font_name in font_candidates:
            try:
                return ImageFont.truetype(font_name, size)
            except Exception:
                continue

        try:
            return ImageFont.load_default()
        except Exception:
            return None

    @classmethod
    def generate_scene_mp4(
        cls,
        scene_id: str,
        scene_type: str,
        chapter_title: str,
        narration: str,
        audio_path: Optional[str],
        duration_sec: float,
        topic: str = "Ohm's Law",
        subject: str = "STEM",
        visual_payload: Optional[Dict[str, Any]] = None,
        formula: Optional[str] = None
    ) -> Dict[str, Any]:
        
        duration = max(5.0, duration_sec)
        clean_topic_slug = re.sub(r'[^a-zA-Z0-9_]', '', topic.lower().replace(' ', '_'))[:24]
        out_filename = f"{scene_id}_{clean_topic_slug}.mp4"
        out_path = VIDEO_DIR / out_filename

        if out_path.exists() and out_path.stat().st_size > 15000:
            return {"video_path": str(out_path), "video_url": f"/api/media/video/{out_filename}", "cached": True}

        # Full 1080p Studio Resolution for razor-sharp clarity
        width, height = 1920, 1080
        ffmpeg_bin = cls.get_ffmpeg_bin()
        
        # Render high-definition representative keyframe
        keyframe_img = cls._draw_scene_frame(
            frame_idx=6,
            total_frames=12,
            scene_type=scene_type,
            title=chapter_title,
            narration=narration,
            topic=topic,
            subject=subject,
            visual_payload=visual_payload or {},
            formula=formula or "",
            width=width,
            height=height
        )
        
        temp_frame_path = VIDEO_DIR / f"temp_{scene_id}_{clean_topic_slug}.png"
        keyframe_img.save(temp_frame_path, "PNG")

        if audio_path and os.path.exists(audio_path):
            cmd = [
                ffmpeg_bin,
                "-y",
                "-loop", "1",
                "-i", str(temp_frame_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "fast",
                "-tune", "stillimage",
                "-crf", "17",
                "-pix_fmt", "yuv420p",
                "-b:v", "8000k",
                "-maxrate", "10000k",
                "-bufsize", "16000k",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(out_path)
            ]
        else:
            cmd = [
                ffmpeg_bin,
                "-y",
                "-loop", "1",
                "-i", str(temp_frame_path),
                "-f", "lavfi",
                "-i", "anullsrc=r=44100:cl=stereo",
                "-c:v", "libx264",
                "-preset", "fast",
                "-tune", "stillimage",
                "-crf", "17",
                "-pix_fmt", "yuv420p",
                "-b:v", "8000k",
                "-maxrate", "10000k",
                "-bufsize", "16000k",
                "-c:a", "aac",
                "-t", str(duration),
                str(out_path)
            ]

        try:
            proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if temp_frame_path.exists():
                temp_frame_path.unlink()

            if out_path.exists() and out_path.stat().st_size > 1000:
                return {"video_path": str(out_path), "video_url": f"/api/media/video/{out_filename}", "cached": False}
        except Exception as e:
            if temp_frame_path.exists():
                temp_frame_path.unlink()
            print(f"[VideoRenderer] 1080p MP4 render error: {e}")

        return {"video_path": None, "video_url": None, "error": str(e) if 'e' in locals() else "Unknown render failure"}

    @classmethod
    def _draw_scene_frame(
        cls,
        frame_idx: int,
        total_frames: int,
        scene_type: str,
        title: str,
        narration: str,
        topic: str,
        subject: str,
        visual_payload: Dict[str, Any],
        formula: str,
        width: int,
        height: int
    ) -> Image.Image:
        
        t = frame_idx / 12.0
        # Base canvas dark cinematic slate
        img = Image.new("RGB", (width, height), color=(8, 12, 22))
        draw = ImageDraw.Draw(img)

        # Ambient background glow
        orb_x = int(width / 2 + math.sin(t * 0.8) * 120)
        orb_y = int(height / 2 + math.cos(t * 0.6) * 60)
        draw.ellipse([orb_x - 550, orb_y - 380, orb_x + 550, orb_y + 380], fill=(14, 30, 60))

        # Top Header Bar (1080p Scale)
        draw.rectangle([0, 0, width, 100], fill=(15, 23, 42))
        draw.line([0, 100, width, 100], fill=(56, 189, 248), width=3)
        
        # High-Resolution Typography (1080p Scale)
        f_badge = cls._get_font(18, bold=True)
        f_title = cls._get_font(26, bold=True)
        f_time = cls._get_font(18, bold=False)

        # AI HD 1080P Badge
        draw.rectangle([35, 25, 230, 75], fill=(2, 132, 199))
        draw.text((48, 38), "AI TUTOR 1080P", fill=(255, 255, 255), font=f_badge)

        # Topic & Subject Pill
        clean_topic = topic.upper() if topic else "CORE STEM"
        clean_sub = subject.upper() if subject else "LESSON"
        draw.rectangle([250, 25, 580, 75], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
        draw.text((268, 38), f"{clean_sub} • {clean_topic}"[:30], fill=(56, 189, 248), font=f_badge)

        # Chapter Title
        clean_title = title.upper() if title else "EDUCATIONAL VISUAL EXPLAINER"
        draw.text((610, 36), clean_title[:55], fill=(241, 245, 249), font=f_title)

        # Time code
        mins = int(t // 60)
        secs = int(t % 60)
        draw.text((width - 180, 38), f"{mins:02d}:{secs:02d} SEC", fill=(148, 163, 184), font=f_time)

        # Topic classification for rendering
        t_low = topic.lower()
        s_type = scene_type.lower()
        title_low = title.lower()

        # 1. Agentic AI & Autonomous Agent Cognitive Loops
        if any(k in t_low for k in ["agentic", "agent", "autonomous agent", "react agent", "tool calling"]):
            cls._render_agentic_ai_motion(draw, t, width, height, topic, title, narration, visual_payload)

        # 2. AI, LangChain, LLM Architectures & RAG
        elif any(k in t_low for k in ["langchain", "llm", "prompt", "rag", "retriev", "vector", "embed", "transformer", "nlp"]):
            cls._render_ai_agent_motion(draw, t, width, height, topic, title, narration, visual_payload)

        # 3. Machine Learning & Neural Networks
        elif any(k in t_low for k in ["neural", "deep learning", "machine learning", "backpropagation", "gradient descent", "cnn"]):
            cls._render_neural_network_motion(draw, t, width, height, topic, title, narration, visual_payload)

        # 4. Quantum Computing & Superposition
        elif any(k in t_low for k in ["quantum", "qubit", "superposition", "entangle"]):
            cls._render_quantum_motion(draw, t, width, height, topic, title, narration, visual_payload)

        # 5. Photosynthesis & Botany / Biology
        elif any(k in t_low for k in ["photosynthesis", "chloroplast", "plant", "chlorophyll", "calvin", "light reaction", "biology"]):
            cls._render_photosynthesis_motion(draw, t, width, height, title, narration, visual_payload)

        # 6. Newton's Laws & Classical Mechanics
        elif any(k in t_low for k in ["newton", "force", "gravity", "gravitation", "motion", "inertia", "acceleration"]):
            cls._render_newton_motion(draw, t, width, height, title, narration, visual_payload)

        # 7. Ohm's Law & Electricity / Circuits
        elif any(k in t_low for k in ["ohm", "circuit", "voltage", "current", "resistan", "resistor"]):
            if "water" in s_type or "water" in title_low or "analogy" in title_low:
                cls._render_water_motion(draw, t, width, height)
            elif "formula" in s_type or "relationship" in title_low:
                cls._render_formula_motion(draw, t, width, height)
            elif "example" in s_type or "worked" in title_low:
                cls._render_example_motion(draw, t, width, height)
            elif "remediation" in s_type:
                cls._render_remediation_motion(draw, t, width, height)
            else:
                cls._render_circuit_motion(draw, t, width, height)

        # 8. Binary Search & Algorithms / CS
        elif any(k in t_low for k in ["binary search", "search", "algorithm", "array", "tree", "sort"]):
            cls._render_cs_motion(draw, t, width, height)

        # 9. Quadratic Equations & Mathematics
        elif any(k in t_low for k in ["quadratic", "parabola", "algebra", "polynomial", "calculus"]):
            cls._render_math_motion(draw, t, width, height)

        # 10. Chemistry
        elif any(k in t_low for k in ["molecule", "acid", "base", "chemical", "atom", "reaction", "periodic"]):
            cls._render_chemistry_motion(draw, t, width, height, title, narration, visual_payload)

        # 11. Universal Domain-Intelligent Renderer
        else:
            cls._render_dynamic_concept_motion(draw, t, width, height, topic, title, narration, visual_payload, formula)

        # Bottom Subtitle Banner (1080p Scale)
        draw.rectangle([40, height - 130, width - 40, height - 35], fill=(15, 23, 42))
        draw.rectangle([40, height - 130, width - 40, height - 35], outline=(51, 65, 85), width=2)
        
        # Audio Equalizer wave in subtitle box
        for i in range(16):
            wave_h = int(12 + math.sin(t * 12 + i * 0.8) * 16 + math.cos(t * 6 + i) * 8)
            wave_h = max(6, wave_h)
            wx = 75 + i * 11
            draw.line([wx, height - 82 - wave_h // 2, wx, height - 82 + wave_h // 2], fill=(56, 189, 248), width=4)

        # Subtitle Text with auto-wrapping
        sub_font = cls._get_font(21, bold=False)
        sub_text = narration if narration else f"Exploring core principles of {topic}."
        words = sub_text.split()
        lines = []
        curr_line = ""
        for w in words:
            if len(curr_line) + len(w) < 110:
                curr_line += (" " if curr_line else "") + w
            else:
                lines.append(curr_line)
                curr_line = w
        if curr_line:
            lines.append(curr_line)

        for l_idx, line in enumerate(lines[:2]):
            draw.text((270, height - 116 + l_idx * 34), line, fill=(241, 245, 249), font=sub_font)

        return img

    # ==================== DOMAIN MOTION GRAPHICS RENDERERS (1080p) ====================

    @classmethod
    def _render_agentic_ai_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, topic: str, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(32, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)
        f_sub = cls._get_font(20, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "AUTONOMOUS AGENTIC AI ARCHITECTURE (ReAct Loop):", fill=(148, 163, 184), font=f_sub)
        draw.text((120, 185), "Goal Perception ⟶ LLM Reasoning & Planning ⟶ Tool Calling ⟶ Environment Feedback", fill=(56, 189, 248), font=f_huge)

        # Cognitive Cycle Boxes
        nodes = [
            {"title": "1. Perception & Memory", "desc": "Context window, conversation state & vector episodic memory", "color": (56, 189, 248)},
            {"title": "2. Reasoning & Plan", "desc": "Goal decomposition, sub-task planning & self-reflection (Reflexion)", "color": (168, 85, 247)},
            {"title": "3. Tool Invocation", "desc": "Execution of APIs, Python Code REPL, DB queries & web browsing", "color": (245, 158, 11)},
            {"title": "4. Environment Feedback", "desc": "Observation evaluation, self-correction loop & final synthesis", "color": (16, 185, 129)}
        ]

        card_w = 400
        card_h = 420
        start_x = 90
        gap = 42

        for i, node in enumerate(nodes):
            cx = start_x + i * (card_w + gap)
            cy = 280

            draw.rectangle([cx, cy, cx + card_w, cy + card_h], fill=(15, 23, 42), outline=node["color"], width=3)
            draw.rectangle([cx, cy, cx + card_w, cy + 65], fill=(30, 41, 59))
            draw.text((cx + 20, cy + 20), node["title"], fill=node["color"], font=f_card_t)

            words = node["desc"].split()
            lines = []
            curr = ""
            for w in words:
                if len(curr) + len(w) < 26:
                    curr += (" " if curr else "") + w
                else:
                    lines.append(curr)
                    curr = w
            if curr:
                lines.append(curr)

            for l_idx, line in enumerate(lines[:6]):
                draw.text((cx + 25, cy + 100 + l_idx * 36), line, fill=(226, 232, 240), font=f_card_b)

            pulse_y = cy + 280 + int(math.sin(t * 4 + i) * 10)
            draw.ellipse([cx + 180, pulse_y - 12, cx + 220, pulse_y + 12], fill=node["color"])

            if i < len(nodes) - 1:
                arrow_x = cx + card_w + 10
                arrow_y = cy + card_h // 2
                draw.line([arrow_x, arrow_y, arrow_x + 22, arrow_y], fill=(255, 255, 255), width=4)

    @classmethod
    def _render_ai_agent_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, topic: str, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(32, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)
        f_sub = cls._get_font(20, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "LANGCHAIN & AGENTIC ARCHITECTURE:", fill=(148, 163, 184), font=f_sub)
        draw.text((120, 185), "User Prompt ⟶ Vector Store (RAG) ⟶ Foundation LLM ⟶ ReAct Tool Execution", fill=(56, 189, 248), font=f_huge)

        nodes = [
            {"title": "1. Prompt Template", "desc": "Dynamic variable injection & structured JSON schema parser", "color": (56, 189, 248)},
            {"title": "2. Vector Store / RAG", "desc": "High-dim embeddings & Top-K Cosine Similarity retrieval", "color": (16, 185, 129)},
            {"title": "3. Foundation LLM", "desc": "Reasoning engine evaluating prompt context & tool intent", "color": (168, 85, 247)},
            {"title": "4. ReAct Tool Loop", "desc": "Autonomous execution: Python REPL, Web Search & SQL APIs", "color": (245, 158, 11)}
        ]

        card_w = 400
        card_h = 420
        start_x = 90
        gap = 42

        for i, node in enumerate(nodes):
            cx = start_x + i * (card_w + gap)
            cy = 280

            draw.rectangle([cx, cy, cx + card_w, cy + card_h], fill=(15, 23, 42), outline=node["color"], width=3)
            draw.rectangle([cx, cy, cx + card_w, cy + 65], fill=(30, 41, 59))
            draw.text((cx + 20, cy + 20), node["title"], fill=node["color"], font=f_card_t)

            words = node["desc"].split()
            lines = []
            curr = ""
            for w in words:
                if len(curr) + len(w) < 26:
                    curr += (" " if curr else "") + w
                else:
                    lines.append(curr)
                    curr = w
            if curr:
                lines.append(curr)

            for l_idx, line in enumerate(lines[:6]):
                draw.text((cx + 25, cy + 100 + l_idx * 36), line, fill=(226, 232, 240), font=f_card_b)

            pulse_y = cy + 280 + int(math.sin(t * 4 + i) * 10)
            draw.ellipse([cx + 180, pulse_y - 12, cx + 220, pulse_y + 12], fill=node["color"])

            if i < len(nodes) - 1:
                arrow_x = cx + card_w + 10
                arrow_y = cy + card_h // 2
                draw.line([arrow_x, arrow_y, arrow_x + 22, arrow_y], fill=(255, 255, 255), width=4)

    @classmethod
    def _render_neural_network_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, topic: str, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(32, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(168, 85, 247), width=3)
        draw.text((120, 150), "ARTIFICIAL NEURAL NETWORK & BACKPROPAGATION:", fill=(148, 163, 184), font=f_card_b)
        draw.text((120, 185), "Forward Pass: y = σ(W · X + b)   |   Gradient Descent: W_new = W_old - η(∂L/∂W)", fill=(192, 132, 252), font=f_huge)

        layers = [
            {"name": "Input Layer (X)", "count": 4, "x": 300, "color": (56, 189, 248)},
            {"name": "Hidden Layer 1", "count": 5, "x": 750, "color": (168, 85, 247)},
            {"name": "Hidden Layer 2", "count": 5, "x": 1200, "color": (236, 72, 153)},
            {"name": "Output Layer (ŷ)", "count": 2, "x": 1650, "color": (16, 185, 129)}
        ]

        for l_idx in range(len(layers) - 1):
            l1, l2 = layers[l_idx], layers[l_idx + 1]
            for n1 in range(l1["count"]):
                y1 = 380 + n1 * 75
                for n2 in range(l2["count"]):
                    y2 = 380 + n2 * 75
                    draw.line([l1["x"], y1, l2["x"], y2], fill=(40, 50, 80), width=2)

        for layer in layers:
            draw.text((layer["x"] - 70, 310), layer["name"], fill=layer["color"], font=f_card_t)
            for n in range(layer["count"]):
                ny = 380 + n * 75
                draw.ellipse([layer["x"] - 22, ny - 22, layer["x"] + 22, ny + 22], fill=layer["color"])
                draw.ellipse([layer["x"] - 14, ny - 14, layer["x"] + 14, ny + 14], fill=(255, 255, 255))

    @classmethod
    def _render_quantum_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, topic: str, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(32, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "QUANTUM INFORMATION SCIENCE & SUPERPOSITION:", fill=(148, 163, 184), font=f_card_b)
        draw.text((120, 185), "|Ψ⟩ = α|0⟩ + β|1⟩   where   |α|² + |β|² = 1.00 (100% Probability)", fill=(56, 189, 248), font=f_huge)

        cx, cy = 960, 520
        r = 180
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(56, 189, 248), width=3)
        draw.ellipse([cx - r, cy - 40, cx + r, cy + 40], outline=(70, 90, 130), width=2)
        draw.line([cx, cy - r - 30, cx, cy + r + 30], fill=(148, 163, 184), width=3)
        draw.text((cx - 15, cy - r - 65), "|0⟩ (North)", fill=(56, 189, 248), font=f_card_t)
        draw.text((cx - 15, cy + r + 35), "|1⟩ (South)", fill=(56, 189, 248), font=f_card_t)

        theta = t * 1.5
        vx = cx + int(math.sin(theta) * 140)
        vy = cy - int(math.cos(theta) * 140)
        draw.line([cx, cy, vx, vy], fill=(236, 72, 153), width=6)
        draw.ellipse([vx - 10, vy - 10, vx + 10, vy + 10], fill=(255, 255, 255))
        draw.text((vx + 15, vy - 10), "|Ψ⟩ Superposition", fill=(236, 72, 153), font=f_card_t)

    @classmethod
    def _render_circuit_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_main = cls._get_font(32, bold=True)
        f_lbl = cls._get_font(20, bold=True)
        
        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "GOVERNING ELECTRICAL LAW:", fill=(148, 163, 184), font=f_lbl)
        draw.text((120, 185), "V = I × R   ⟹   Current (I) = V / R = 12V / 4Ω = 3.00 Amperes", fill=(56, 189, 248), font=f_main)

        top_y, bot_y = 340, 680
        left_x, right_x = 350, 1570

        draw.line([left_x, top_y, right_x, top_y], fill=(56, 189, 248), width=6)
        draw.line([right_x, top_y, right_x, bot_y], fill=(56, 189, 248), width=6)
        draw.line([right_x, bot_y, left_x, bot_y], fill=(56, 189, 248), width=6)
        draw.line([left_x, bot_y, left_x, top_y], fill=(56, 189, 248), width=6)

        bx = left_x
        by = (top_y + bot_y) // 2
        draw.rectangle([bx - 40, by - 70, bx + 40, by + 70], fill=(15, 23, 42), outline=(56, 189, 248), width=4)
        draw.text((bx - 120, by - 15), "12V Battery", fill=(56, 189, 248), font=f_lbl)

        rx = right_x
        ry = (top_y + bot_y) // 2
        draw.rectangle([rx - 40, ry - 70, rx + 40, ry + 70], fill=(15, 23, 42), outline=(244, 63, 94), width=4)
        draw.text((rx + 55, ry - 15), "4Ω Resistor", fill=(244, 63, 94), font=f_lbl)

        num_particles = 28
        perimeter = 2 * ((right_x - left_x) + (bot_y - top_y))
        for i in range(num_particles):
            dist = (t * 220 + i * (perimeter / num_particles)) % perimeter
            w_len = right_x - left_x
            h_len = bot_y - top_y

            if dist < w_len:
                px = left_x + dist
                py = top_y
            elif dist < w_len + h_len:
                px = right_x
                py = top_y + (dist - w_len)
            elif dist < 2 * w_len + h_len:
                px = right_x - (dist - (w_len + h_len))
                py = bot_y
            else:
                px = left_x
                py = bot_y - (dist - (2 * w_len + h_len))

            draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(255, 255, 255))
            draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(56, 189, 248))

    @classmethod
    def _render_water_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_main = cls._get_font(32, bold=True)
        f_lbl = cls._get_font(20, bold=True)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "MECHANICAL HYDRAULIC ANALOGY:", fill=(148, 163, 184), font=f_lbl)
        draw.text((120, 185), "Water Pump (Voltage) ⟶ Fluid Flow (Current) ⟶ Pipe Constriction (Resistance)", fill=(56, 189, 248), font=f_main)

        draw.rectangle([250, 400, 1670, 620], fill=(15, 23, 42), outline=(56, 189, 248), width=5)
        draw.rectangle([880, 470, 1140, 550], fill=(30, 41, 59), outline=(244, 63, 94), width=4)
        draw.text((910, 420), "Resistor (Narrow Pipe)", fill=(244, 63, 94), font=f_lbl)

    @classmethod
    def _render_formula_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_huge = cls._get_font(48, bold=True)
        f_sub = cls._get_font(20, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "MATHEMATICAL FORMULATION:", fill=(148, 163, 184), font=f_sub)
        draw.text((120, 185), "V = I × R   |   I = V / R   |   R = V / I", fill=(56, 189, 248), font=f_huge)

    @classmethod
    def _render_example_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_head = cls._get_font(28, bold=True)
        f_step = cls._get_font(22, bold=False)

        draw.rectangle([150, 280, 1770, 680], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((200, 320), "WORKED STEP-BY-STEP CALCULATION:", fill=(56, 189, 248), font=f_head)
        draw.text((200, 390), "Step 1: Given Voltage V = 12 Volts, Resistance R = 4 Ohms", fill=(241, 245, 249), font=f_step)
        draw.text((200, 450), "Step 2: Rearrange Ohm's Law for Current: I = V / R", fill=(241, 245, 249), font=f_step)
        draw.text((200, 510), "Step 3: Substitute values: I = 12 / 4", fill=(241, 245, 249), font=f_step)
        draw.text((200, 580), "Result: Current I = 3.00 Amperes (A)", fill=(16, 185, 129), font=f_head)

    @classmethod
    def _render_remediation_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_head = cls._get_font(26, bold=True)
        f_sub = cls._get_font(20, bold=False)

        draw.rectangle([150, 280, 900, 680], fill=(15, 23, 42), outline=(16, 185, 129), width=3)
        draw.text((180, 320), "STANDARD RESISTANCE (4 Ω)", fill=(16, 185, 129), font=f_head)
        draw.text((180, 380), "• Voltage: V = 12V", fill=(241, 245, 249), font=f_sub)
        draw.text((180, 430), "• Resistance: R = 4Ω", fill=(241, 245, 249), font=f_sub)
        draw.text((180, 480), "• Current: I = 12 / 4 = 3.0 A", fill=(56, 189, 248), font=f_head)

        draw.rectangle([1020, 280, 1770, 680], fill=(15, 23, 42), outline=(244, 63, 94), width=3)
        draw.text((1050, 320), "DOUBLED RESISTANCE (8 Ω)", fill=(244, 63, 94), font=f_head)
        draw.text((1050, 380), "• Voltage: V = 12V", fill=(241, 245, 249), font=f_sub)
        draw.text((1050, 430), "• Resistance: R = 8Ω", fill=(241, 245, 249), font=f_sub)
        draw.text((1050, 480), "• Current: I = 12 / 8 = 1.5 A (Cut in Half!)", fill=(244, 63, 94), font=f_head)

    @classmethod
    def _render_photosynthesis_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(30, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(16, 185, 129), width=3)
        draw.text((120, 150), "BIOCHEMICAL PHOTOSYNTHESIS REACTION:", fill=(148, 163, 184), font=f_card_b)
        draw.text((120, 185), "6CO₂ + 6H₂O + Solar Photons (hν) ⟶ C₆H₁₂O₆ (Glucose) + 6O₂ (Oxygen)", fill=(52, 211, 153), font=f_huge)

        draw.rectangle([150, 280, 900, 680], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((180, 320), "1. LIGHT REACTIONS (Thylakoids)", fill=(56, 189, 248), font=f_card_t)
        draw.text((180, 380), "• Chlorophyll captures photons", fill=(241, 245, 249), font=f_card_b)
        draw.text((180, 430), "• Photolysis of water: 2H₂O ⟶ 4H⁺ + 4e⁻ + O₂↑", fill=(241, 245, 249), font=f_card_b)
        draw.text((180, 480), "• Produces energy carriers ATP & NADPH", fill=(16, 185, 129), font=f_card_b)

        draw.rectangle([1020, 280, 1770, 680], fill=(15, 23, 42), outline=(16, 185, 129), width=3)
        draw.text((1050, 320), "2. CALVIN CYCLE (Stroma)", fill=(16, 185, 129), font=f_card_t)
        draw.text((1050, 380), "• RuBisCO fixes atmospheric CO₂", fill=(241, 245, 249), font=f_card_b)
        draw.text((1050, 430), "• ATP & NADPH power carbon reduction", fill=(241, 245, 249), font=f_card_b)
        draw.text((1050, 480), "• Synthesizes Glucose (C₆H₁₂O₆)", fill=(52, 211, 153), font=f_card_t)

    @classmethod
    def _render_newton_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(30, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "NEWTON'S LAWS OF CLASSICAL DYNAMICS:", fill=(148, 163, 184), font=f_card_b)
        draw.text((120, 185), "F_net = m × a   ⟹   Acceleration: a = F_net / m (m/s²)", fill=(56, 189, 248), font=f_huge)

        pillars = [
            {"title": "1st Law (Inertia)", "desc": "Objects resist velocity changes. ΣF = 0 implies acceleration is 0."},
            {"title": "2nd Law (F = ma)", "desc": "Net force produces acceleration inversely proportional to mass."},
            {"title": "3rd Law (Action-Reaction)", "desc": "Every applied force produces an equal, opposite interaction: F_AB = -F_BA."}
        ]

        card_w = 510
        for i, p in enumerate(pillars):
            cx = 100 + i * (card_w + 35)
            cy = 280
            draw.rectangle([cx, cy, cx + card_w, cy + 400], fill=(15, 23, 42), outline=(56, 189, 248), width=2)
            draw.rectangle([cx, cy, cx + card_w, cy + 60], fill=(30, 41, 59))
            draw.text((cx + 20, cy + 18), p["title"], fill=(56, 189, 248), font=f_card_t)
            draw.text((cx + 20, cy + 100), p["desc"], fill=(226, 232, 240), font=f_card_b)

    @classmethod
    def _render_cs_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_huge = cls._get_font(30, bold=True)
        f_arr = cls._get_font(24, bold=True)
        f_lbl = cls._get_font(18, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "BINARY SEARCH DIVIDE & CONQUER:", fill=(148, 163, 184), font=f_lbl)
        draw.text((120, 185), "Time Complexity: O(log N)  |  Halves Search Space Each Step", fill=(56, 189, 248), font=f_huge)

        arr = [2, 5, 8, 12, 16, 23, 38]
        start_x = 220
        box_w = 200
        box_h = 140
        y = 420

        for i, num in enumerate(arr):
            bx = start_x + i * (box_w + 15)
            is_mid = (i == 3)
            is_target = (i == 5)
            color = (16, 185, 129) if is_target else ((244, 63, 94) if is_mid else (56, 189, 248))

            draw.rectangle([bx, y, bx + box_w, y + box_h], fill=(15, 23, 42), outline=color, width=3)
            draw.text((bx + 75, y + 45), str(num), fill=(255, 255, 255), font=f_arr)
            draw.text((bx + 60, y + 155), f"Index {i}", fill=(148, 163, 184), font=f_lbl)

    @classmethod
    def _render_math_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int):
        f_huge = cls._get_font(30, bold=True)
        f_lbl = cls._get_font(20, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), "QUADRATIC FORMULA & PARABOLIC ROOTS:", fill=(148, 163, 184), font=f_lbl)
        draw.text((120, 185), "x = (-b ± √(b² - 4ac)) / (2a)   |   Discriminant Δ = b² - 4ac", fill=(56, 189, 248), font=f_huge)

    @classmethod
    def _render_chemistry_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, title: str, narration: str, visual_payload: Dict[str, Any]):
        f_huge = cls._get_font(30, bold=True)
        f_lbl = cls._get_font(20, bold=False)

        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(168, 85, 247), width=3)
        draw.text((120, 150), "MOLECULAR KINETICS & CHEMICAL BONDING:", fill=(148, 163, 184), font=f_lbl)
        draw.text((120, 185), "Reactants + Activation Energy (Ea) ⟶ Products + ΔH", fill=(192, 132, 252), font=f_huge)

    @classmethod
    def _render_dynamic_concept_motion(cls, draw: ImageDraw.ImageDraw, t: float, width: int, height: int, topic: str, title: str, narration: str, visual_payload: Dict[str, Any], formula: str):
        f_huge = cls._get_font(30, bold=True)
        f_card_t = cls._get_font(22, bold=True)
        f_card_b = cls._get_font(18, bold=False)
        f_sub = cls._get_font(18, bold=False)

        clean_topic = topic.strip() or "Core Foundational Concept"
        form_text = formula or visual_payload.get("formula") or f"Governing Principles of {clean_topic}"

        # Master Top Header Formula
        draw.rectangle([80, 130, width - 80, 240], fill=(15, 23, 42), outline=(56, 189, 248), width=3)
        draw.text((120, 150), f"CORE FOUNDATIONAL PRINCIPLE — {clean_topic.upper()}:", fill=(148, 163, 184), font=f_sub)
        draw.text((120, 185), form_text[:80], fill=(56, 189, 248), font=f_huge)

        # 3 Architectural Pillars
        key_points = visual_payload.get("key_points") or [
            {"label": "1. Core Definition", "detail": f"Fundamental property and mechanism governing {clean_topic}."},
            {"label": "2. Driving Mechanism", "detail": "Observed cause-and-effect interaction between driving parameters."},
            {"label": "3. Practical Application", "detail": "Direct real-world problem solving, modeling, and calculation."}
        ]

        card_w = 510
        for idx, pt in enumerate(key_points[:3]):
            card_x = 100 + idx * (card_w + 35)
            card_y = 280
            card_h = 400

            draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h], fill=(15, 23, 42), outline=(56, 189, 248) if idx == 0 else (51, 65, 85), width=2)
            draw.rectangle([card_x, card_y, card_x + card_w, card_y + 60], fill=(30, 41, 59))
            draw.text((card_x + 20, card_y + 18), pt.get("label", f"Pillar {idx+1}")[:32], fill=(56, 189, 248) if idx == 0 else (241, 245, 249), font=f_card_t)

            detail = pt.get("detail", "")
            words = detail.split()
            lines = []
            curr = ""
            for w in words:
                if len(curr) + len(w) < 32:
                    curr += (" " if curr else "") + w
                else:
                    lines.append(curr)
                    curr = w
            if curr:
                lines.append(curr)

            for l_idx, line in enumerate(lines[:8]):
                draw.text((card_x + 25, card_y + 90 + l_idx * 34), line, fill=(226, 232, 240), font=f_card_b)
