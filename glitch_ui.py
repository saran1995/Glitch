import tkinter as tk
from tkinter import ttk
import threading
import time
import math

import speech_recognition as sr
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))


class GlitchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Glitch Voice Assistant - Step 1")
        self.root.geometry("600x500")
        self.root.configure(bg='black')

        # State variables
        self.current_state = "sleeping"  # sleeping, listening, thinking, speaking
        self.animation_running = True

        self.setup_gui()
        self.start_animation()
        self.setup_wake_word_detection()

    def setup_wake_word_detection(self):
        """Initialize Whisper-based wake word detection"""
        try:
            print("🚀 Setting up Whisper wake word detection...")

            from src.audio.wake_word_detector import GlitchWhisperWakeDetector

            self.wake_detector = GlitchWhisperWakeDetector()

            if self.wake_detector.initialize():
                self.wake_detector.set_wake_callback(self.on_wake_word_detected)
                self.has_wake_detection = True
                print("✅ Whisper wake word detection ready!")
            else:
                self.has_wake_detection = False
                print("❌ Whisper wake word detection failed")

        except Exception as e:
            print(f"❌ Whisper setup failed: {e}")
            import traceback
            traceback.print_exc()
            self.has_wake_detection = False

    def on_wake_word_detected(self, wake_word, full_text):
        """Handle wake word detection"""
        print(f"🚨 WAKE WORD: '{wake_word}' in '{full_text}'")

        # Update GUI on main thread
        self.root.after(100, lambda: self.wake_up_glitch(wake_word))

    def wake_up_glitch(self, wake_word):
        """Wake up Glitch with animation"""
        self.change_state("listening")
        self.status_label.config(text=f"👋 Hey! I heard '{wake_word}'!")

        # Return to sleep after 3 seconds
        self.root.after(3000, lambda: self.change_state("sleeping"))

    # Add wake word control buttons
    def create_control_buttons(self):
        # ... your existing button code ...

        # Add wake word button if available
        if hasattr(self, 'has_wake_detection') and self.has_wake_detection:
            self.wake_btn = tk.Button(
                button_frame,
                text="👂 Start Wake",
                command=self.toggle_wake_listening,
                bg="#440088",
                fg="white",
                font=("Arial", 12),
                width=12
            )
            self.wake_btn.pack(side=tk.LEFT, padx=5)

    def toggle_wake_listening(self):
        """Toggle wake word listening"""
        if not hasattr(self, 'wake_detector'):
            return

        if self.wake_detector.is_listening:
            self.wake_detector.stop_listening_for_wake()
            self.wake_btn.config(text="👂 Start Wake", bg="#440088")
            self.status_label.config(text="🔇 Wake detection off")
        else:
            self.wake_detector.start_listening()
            self.wake_btn.config(text="👂 Stop Wake", bg="#880044")
            self.status_label.config(text="👂 Listening for 'Hey Glitch'...")

    def setup_gui(self):
        """Setup the basic GUI components"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="G.L.I.T.C.H",
                               font=("Arial", 28, "bold"),
                               fg="#00ffff", bg='black')
        title_label.pack(pady=15)

        # Face canvas - this is where the magic happens
        self.face_canvas = tk.Canvas(main_frame, width=300, height=300,
                                     bg='black', highlightthickness=0)
        self.face_canvas.pack(pady=20)

        # Status label
        self.status_label = tk.Label(main_frame, text="Sleeping...",
                                     font=("Arial", 16),
                                     fg="#00ff00", bg='black')
        self.status_label.pack(pady=10)

        # Test buttons to change states
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(pady=20)

        # State test buttons
        states = [("Sleep", "sleeping"), ("Listen", "listening"),
                  ("Think", "thinking"), ("Speak", "speaking")]

        for text, state in states:
            btn = tk.Button(button_frame, text=text,
                            command=lambda s=state: self.change_state(s),
                            bg="#004400", fg="white", font=("Arial", 12),
                            width=8)
            btn.pack(side=tk.LEFT, padx=5)

    def change_state(self, new_state):
        """Change the current state of Glitch"""
        self.current_state = new_state

        # Update status text
        status_texts = {
            "sleeping": "Sleeping...",
            "listening": "Listening...",
            "thinking": "Processing...",
            "speaking": "Speaking..."
        }
        self.status_label.config(text=status_texts.get(new_state, "Unknown"))

        # The face will automatically update in the animation loop

    def draw_face(self):
        """Draw the face based on current state"""
        self.face_canvas.delete("all")

        if self.current_state == "sleeping":
            self.draw_sleeping_face()
        elif self.current_state == "listening":
            self.draw_listening_face()
        elif self.current_state == "thinking":
            self.draw_thinking_face()
        elif self.current_state == "speaking":
            self.draw_speaking_face()

    def draw_sleeping_face(self):
        """Draw a sleeping face - peaceful and dim"""
        # Dim blue color scheme
        color = "#003366"

        # Face outline (circle)
        self.face_canvas.create_oval(50, 50, 250, 250, outline=color, width=3)

        # Sleeping eyes (curved lines)
        self.face_canvas.create_arc(100, 120, 140, 140, start=0, extent=180,
                                    outline=color, width=3, style='arc')
        self.face_canvas.create_arc(160, 120, 200, 140, start=0, extent=180,
                                    outline=color, width=3, style='arc')

        # Small peaceful mouth
        self.face_canvas.create_line(130, 180, 170, 180, fill=color, width=2)

        # Add some "Z" characters for sleeping effect
        self.face_canvas.create_text(220, 80, text="Z", fill=color, font=("Arial", 16))
        self.face_canvas.create_text(230, 60, text="z", fill=color, font=("Arial", 12))

    def draw_listening_face(self):
        """Draw an attentive listening face"""
        # Bright blue color scheme
        color = "#0066cc"

        # Face outline
        self.face_canvas.create_oval(50, 50, 250, 250, outline=color, width=3)

        # Alert eyes (filled circles)
        self.face_canvas.create_oval(100, 120, 130, 150, outline=color,
                                     fill=color, width=2)
        self.face_canvas.create_oval(170, 120, 200, 150, outline=color,
                                     fill=color, width=2)

        # Slightly open mouth showing attention
        self.face_canvas.create_oval(140, 175, 160, 185, outline=color,
                                     fill=color, width=2)

        # Add sound wave indicators
        for i in range(3):
            radius = 120 + i * 15
            self.face_canvas.create_arc(150 - radius // 2, 150 - radius // 2,
                                        150 + radius // 2, 150 + radius // 2,
                                        start=45, extent=90, outline=color, width=1)

    def draw_thinking_face(self):
        """Draw a thinking/processing face"""
        # Yellow/orange color scheme
        color = "#ffcc00"

        # Face outline
        self.face_canvas.create_oval(50, 50, 250, 250, outline=color, width=3)

        # Concentrated eyes (angled lines)
        self.face_canvas.create_line(100, 125, 130, 135, fill=color, width=4)
        self.face_canvas.create_line(130, 135, 130, 145, fill=color, width=4)

        self.face_canvas.create_line(200, 125, 170, 135, fill=color, width=4)
        self.face_canvas.create_line(170, 135, 170, 145, fill=color, width=4)

        # Slightly pursed mouth
        self.face_canvas.create_line(135, 180, 165, 175, fill=color, width=3)

        # Thinking dots
        dots_x = [210, 220, 230]
        for i, x in enumerate(dots_x):
            size = 3 + math.sin(time.time() * 2 + i) * 2
            self.face_canvas.create_oval(x - size, 100 - size, x + size, 100 + size,
                                         fill=color, outline=color)

    def draw_speaking_face(self):
        """Draw a speaking face with animated mouth"""
        # Green color scheme
        color = "#00ff00"

        # Face outline
        self.face_canvas.create_oval(50, 50, 250, 250, outline=color, width=3)

        # Active eyes
        self.face_canvas.create_oval(100, 120, 130, 150, outline=color,
                                     fill=color, width=2)
        self.face_canvas.create_oval(170, 120, 200, 150, outline=color,
                                     fill=color, width=2)

        # Animated mouth (changes size based on time)
        mouth_open = abs(math.sin(time.time() * 8)) * 15 + 5
        self.face_canvas.create_oval(135, 175, 165, 175 + mouth_open,
                                     outline=color, fill=color, width=2)

        # Sound waves coming from mouth
        for i in range(2):
            wave_size = (abs(math.sin(time.time() * 6 + i)) * 20) + 10
            self.face_canvas.create_arc(150 - wave_size, 180 - wave_size // 2,
                                        150 + wave_size, 180 + wave_size // 2,
                                        start=30, extent=120, outline=color, width=2)

    def start_animation(self):
        """Start the animation loop"""

        def animate():
            while self.animation_running:
                try:
                    self.draw_face()
                    time.sleep(0.1)  # Update 10 times per second
                except:
                    break

        # Run animation in separate thread
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()


def main():
    print("🚀 Starting Glitch GUI - Step 1")
    print("Use the buttons to test different face states!")

    root = tk.Tk()
    app = GlitchGUI(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Glitch...")
        app.animation_running = False


if __name__ == "__main__":
    main()
