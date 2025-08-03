"""
Main GUI window for Glitch Voice Assistant
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import GUI_CONFIG, CURRENT_PHASE
from src.gui.face_animations import FaceAnimator
from src.utils.logger import setup_logger

logger = setup_logger("gui")


class GlitchMainWindow:
    """Main application window for Glitch"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = GUI_CONFIG
        self.theme = self.config["theme"]

        # State management
        self.current_state = "sleeping"
        self.animation_running = True

        # Initialize components
        self.setup_window()
        self.setup_gui_components()
        self.setup_face_animator()

        # Start systems
        self.start_animation_loop()

        logger.info(f"Glitch GUI initialized - Phase: {CURRENT_PHASE}")

    # ... rest of the class remains the same as before
    def setup_window(self):
        """Configure the main window"""
        self.root.title(self.config["window_title"])
        self.root.geometry(self.config["window_size"])
        self.root.configure(bg=self.theme["bg_color"])
        self.root.resizable(True, True)

        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")

    def setup_gui_components(self):
        """Setup all GUI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.theme["bg_color"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        self.create_title()

        # Face display area
        self.create_face_canvas()

        # Status display
        self.create_status_display()

        # Control buttons (for testing)
        self.create_control_buttons()

    def create_title(self):
        """Create the main title"""
        title_label = tk.Label(
            self.main_frame,
            text="J.A.R.V.I.S",
            font=("Arial", 28, "bold"),
            fg=self.theme["primary_color"],
            bg=self.theme["bg_color"]
        )
        title_label.pack(pady=15)

    def create_face_canvas(self):
        """Create the canvas for face animations"""
        canvas_size = self.config["animation"]["face_size"]
        self.face_canvas = tk.Canvas(
            self.main_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.theme["bg_color"],
            highlightthickness=0
        )
        self.face_canvas.pack(pady=20)

    def create_status_display(self):
        """Create status label"""
        self.status_label = tk.Label(
            self.main_frame,
            text="Sleeping...",
            font=("Arial", 16),
            fg=self.theme["secondary_color"],
            bg=self.theme["bg_color"]
        )
        self.status_label.pack(pady=10)

    def create_control_buttons(self):
        """Create control buttons for testing states"""
        button_frame = tk.Frame(self.main_frame, bg=self.theme["bg_color"])
        button_frame.pack(pady=20)

        # State test buttons
        states = [
            ("Sleep", "sleeping"),
            ("Listen", "listening"),
            ("Think", "thinking"),
            ("Speak", "speaking")
        ]

        for text, state in states:
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda s=state: self.change_state(s),
                bg="#004400",
                fg="white",
                font=("Arial", 12),
                width=8,
                relief=tk.RAISED,
                borderwidth=2
            )
            btn.pack(side=tk.LEFT, padx=5)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#006600"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#004400"))

    def setup_face_animator(self):
        """Initialize the face animation system"""
        self.face_animator = FaceAnimator(self.face_canvas)

    def change_state(self, new_state: str):
        """Change Glitch state"""
        logger.info(f"State changed: {self.current_state} -> {new_state}")
        self.current_state = new_state

        # Update status text
        status_texts = {
            "sleeping": "Sleeping...",
            "listening": "Listening...",
            "thinking": "Processing...",
            "speaking": "Speaking..."
        }

        new_status = status_texts.get(new_state, "Unknown State")
        self.status_label.config(text=new_status)

        # Update status label color based on state
        colors = {
            "sleeping": "#003366",
            "listening": "#0066cc",
            "thinking": "#ffcc00",
            "speaking": "#00ff00"
        }
        self.status_label.config(fg=colors.get(new_state, self.theme["secondary_color"]))

    def start_animation_loop(self):
        """Start the main animation loop"""

        def animate():
            fps = self.config["animation"]["fps"]
            frame_time = 1.0 / fps

            while self.animation_running:
                try:
                    start_time = time.time()

                    # Draw face based on current state
                    if self.current_state == "sleeping":
                        self.face_animator.draw_sleeping_face()
                    elif self.current_state == "listening":
                        self.face_animator.draw_listening_face()
                    elif self.current_state == "thinking":
                        self.face_animator.draw_thinking_face()
                    elif self.current_state == "speaking":
                        self.face_animator.draw_speaking_face()

                    # Maintain consistent frame rate
                    elapsed = time.time() - start_time
                    sleep_time = max(0, frame_time - elapsed)
                    time.sleep(sleep_time)

                except Exception as e:
                    logger.error(f"Animation error: {e}")
                    break

        # Start animation in separate thread
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
        logger.info("Animation loop started")

    def shutdown(self):
        """Gracefully shutdown the GUI"""
        logger.info("Shutting down Glitch GUI...")
        self.animation_running = False
        if hasattr(self, 'animation_thread'):
            self.animation_thread.join(timeout=1)
