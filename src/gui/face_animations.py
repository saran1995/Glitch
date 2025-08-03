"""
Face animation system for Glitch GUI
"""
import tkinter as tk
import math
import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import GUI_CONFIG


class FaceAnimator:
    """Handles all face drawing and animation logic"""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.theme = GUI_CONFIG["theme"]
        self.face_size = GUI_CONFIG["animation"]["face_size"]
        self.center_x = self.face_size // 2
        self.center_y = self.face_size // 2

    def clear_face(self):
        """Clear the canvas"""
        self.canvas.delete("all")

    def draw_sleeping_face(self):
        """Draw a peaceful sleeping face"""
        self.clear_face()
        color = "#003366"  # Dim blue

        # Face outline
        self._draw_face_outline(color)

        # Sleeping eyes (arcs)
        self._draw_sleeping_eyes(color)

        # Small mouth
        self.canvas.create_line(
            self.center_x - 20, self.center_y + 30,
            self.center_x + 20, self.center_y + 30,
            fill=color, width=2
        )

        # Sleep indicators
        self._draw_sleep_indicators(color)

    def draw_listening_face(self):
        """Draw an alert, listening face"""
        self.clear_face()
        color = "#0066cc"  # Bright blue

        # Face outline
        self._draw_face_outline(color)

        # Alert eyes
        self._draw_alert_eyes(color)

        # Attentive mouth
        self.canvas.create_oval(
            self.center_x - 10, self.center_y + 25,
            self.center_x + 10, self.center_y + 35,
            outline=color, fill=color
        )

        # Sound wave indicators
        self._draw_sound_waves(color)

    def draw_thinking_face(self):
        """Draw a concentrated thinking face"""
        self.clear_face()
        color = "#ffcc00"  # Yellow

        # Face outline
        self._draw_face_outline(color)

        # Concentrated eyes
        self._draw_thinking_eyes(color)

        # Concentrated mouth
        self.canvas.create_line(
            self.center_x - 15, self.center_y + 30,
            self.center_x + 15, self.center_y + 25,
            fill=color, width=3
        )

        # Animated thinking dots
        self._draw_thinking_dots(color)

    def draw_speaking_face(self):
        """Draw an animated speaking face"""
        self.clear_face()
        color = "#00ff00"  # Green

        # Face outline
        self._draw_face_outline(color)

        # Active eyes
        self._draw_alert_eyes(color)

        # Animated mouth
        self._draw_animated_mouth(color)

        # Speech waves
        self._draw_speech_waves(color)

    def _draw_face_outline(self, color: str):
        """Draw the main face circle"""
        margin = 50
        self.canvas.create_oval(
            margin, margin,
            self.face_size - margin, self.face_size - margin,
            outline=color, width=3
        )

    def _draw_sleeping_eyes(self, color: str):
        """Draw closed sleeping eyes"""
        eye_y = self.center_y - 30

        # Left eye arc
        self.canvas.create_arc(
            self.center_x - 65, eye_y - 10,
            self.center_x - 25, eye_y + 10,
            start=0, extent=180, outline=color, width=3, style='arc'
        )

        # Right eye arc
        self.canvas.create_arc(
            self.center_x + 25, eye_y - 10,
            self.center_x + 65, eye_y + 10,
            start=0, extent=180, outline=color, width=3, style='arc'
        )

    def _draw_alert_eyes(self, color: str):
        """Draw open, alert eyes"""
        eye_y = self.center_y - 30

        # Left eye
        self.canvas.create_oval(
            self.center_x - 65, eye_y - 15,
            self.center_x - 35, eye_y + 15,
            outline=color, fill=color
        )

        # Right eye
        self.canvas.create_oval(
            self.center_x + 35, eye_y - 15,
            self.center_x + 65, eye_y + 15,
            outline=color, fill=color
        )

    def _draw_thinking_eyes(self, color: str):
        """Draw concentrated thinking eyes"""
        eye_y = self.center_y - 25

        # Left eye (angled)
        self.canvas.create_line(
            self.center_x - 65, eye_y - 5,
            self.center_x - 35, eye_y + 5,
            fill=color, width=4
        )
        self.canvas.create_line(
            self.center_x - 35, eye_y + 5,
            self.center_x - 35, eye_y + 15,
            fill=color, width=4
        )

        # Right eye (angled)
        self.canvas.create_line(
            self.center_x + 65, eye_y - 5,
            self.center_x + 35, eye_y + 5,
            fill=color, width=4
        )
        self.canvas.create_line(
            self.center_x + 35, eye_y + 5,
            self.center_x + 35, eye_y + 15,
            fill=color, width=4
        )

    def _draw_sleep_indicators(self, color: str):
        """Draw Z characters for sleeping"""
        self.canvas.create_text(
            self.center_x + 70, self.center_y - 70,
            text="Z", fill=color, font=("Arial", 16)
        )
        self.canvas.create_text(
            self.center_x + 80, self.center_y - 90,
            text="z", fill=color, font=("Arial", 12)
        )

    def _draw_sound_waves(self, color: str):
        """Draw sound wave indicators for listening"""
        for i in range(3):
            radius = 120 + i * 15
            self.canvas.create_arc(
                self.center_x - radius // 2, self.center_y - radius // 2,
                self.center_x + radius // 2, self.center_y + radius // 2,
                start=45, extent=90, outline=color, width=1
            )

    def _draw_thinking_dots(self, color: str):
        """Draw animated thinking dots"""
        dots_x = [self.center_x + 60, self.center_x + 70, self.center_x + 80]
        dots_y = self.center_y - 50

        for i, x in enumerate(dots_x):
            size = 3 + math.sin(time.time() * 2 + i) * 2
            self.canvas.create_oval(
                x - size, dots_y - size,
                x + size, dots_y + size,
                fill=color, outline=color
            )

    def _draw_animated_mouth(self, color: str):
        """Draw animated speaking mouth"""
        mouth_open = abs(math.sin(time.time() * 8)) * 15 + 5
        self.canvas.create_oval(
            self.center_x - 15, self.center_y + 25,
            self.center_x + 15, self.center_y + 25 + mouth_open,
            outline=color, fill=color
        )

    def _draw_speech_waves(self, color: str):
        """Draw speech wave indicators"""
        for i in range(2):
            wave_size = (abs(math.sin(time.time() * 6 + i)) * 20) + 10
            self.canvas.create_arc(
                self.center_x - wave_size, self.center_y + 30 - wave_size // 2,
                self.center_x + wave_size, self.center_y + 30 + wave_size // 2,
                start=30, extent=120, outline=color, width=2
            )
