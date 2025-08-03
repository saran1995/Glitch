"""
Whisper-powered Wake Word Detection for Glitch
Much more reliable than Google Speech Recognition
"""
import whisper
import pyaudio
import wave
import threading
import tempfile
import os
import time
import logging
import numpy as np

logger = logging.getLogger("glitch_wake_word")

class GlitchWhisperWakeDetector:
    """Whisper-based wake word detector for Glitch"""

    def __init__(self):
        self.wake_words = ["glitch", "hey glitch", "hi glitch", "ग्लिच"]  # Added Hindi option
        self.is_listening = False
        self.callback_function = None

        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1

        # Whisper model
        self.whisper_model = None
        self.audio_stream = None

        # Threading
        self.listen_thread = None
        self.stop_listening = threading.Event()

    def initialize(self) -> bool:
        """Initialize Whisper model and audio system"""
        try:
            logger.info("🚀 Loading Whisper model...")

            # Load Whisper model (base is good balance of speed vs accuracy)
            self.whisper_model = whisper.load_model("base")
            logger.info("✅ Whisper model loaded!")

            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()

            # Test microphone
            try:
                test_stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
                test_stream.close()
                logger.info("✅ Microphone access confirmed!")

            except Exception as e:
                logger.error(f"❌ Microphone test failed: {e}")
                return False

            return True

        except Exception as e:
            logger.error(f"❌ Whisper initialization failed: {e}")
            return False

    def set_wake_callback(self, callback):
        """Set callback for wake word detection"""
        self.callback_function = callback
        logger.info("📞 Wake word callback registered")

    def start_listening(self):
        """Start listening for wake words"""
        if self.is_listening:
            return

        self.is_listening = True
        self.stop_listening.clear()

        self.listen_thread = threading.Thread(target=self._whisper_listen_loop, daemon=True)
        self.listen_thread.start()

        logger.info("👂 Whisper listening for: " + ", ".join(self.wake_words))

    def stop_listening_for_wake(self):
        """Stop listening"""
        self.is_listening = False
        self.stop_listening.set()

        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)

        logger.info("🔇 Stopped Whisper listening")

    def _whisper_listen_loop(self):
        """Main Whisper listening loop"""
        try:
            # Open audio stream
            self.audio_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            logger.info("🎤 Whisper listening loop started")

            audio_buffer = []
            silence_threshold = 500  # Adjust based on your environment
            min_audio_length = self.sample_rate * 1  # 1 second minimum
            max_audio_length = self.sample_rate * 5  # 5 seconds maximum

            while self.is_listening and not self.stop_listening.is_set():
                # Read audio data
                data = self.audio_stream.read(self.chunk_size, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)

                # Check if there's sound (simple voice activity detection)
                if np.abs(audio_data).mean() > silence_threshold:
                    audio_buffer.extend(audio_data)

                    # If we have enough audio, process it
                    if len(audio_buffer) >= min_audio_length:
                        # Convert to the right format for Whisper
                        audio_array = np.array(audio_buffer, dtype=np.float32) / 32768.0

                        # Process with Whisper
                        self._process_audio_with_whisper(audio_array)

                        # Clear buffer
                        audio_buffer = []

                # Prevent buffer from getting too large
                if len(audio_buffer) > max_audio_length:
                    audio_buffer = audio_buffer[-min_audio_length:]

                time.sleep(0.01)  # Small delay

        except Exception as e:
            logger.error(f"❌ Whisper listen loop error: {e}")
        finally:
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()

    def _process_audio_with_whisper(self, audio_data):
        """Process audio data with Whisper"""
        try:
            # Use Whisper to transcribe
            result = self.whisper_model.transcribe(
                audio_data,
                language="en",  # Can be set to None for auto-detection
                task="transcribe"
            )

            text = result["text"].lower().strip()

            if text:  # Only process non-empty results
                logger.debug(f"🎯 Whisper heard: '{text}'")

                # Check for wake words
                for wake_word in self.wake_words:
                    if wake_word in text:
                        logger.info(f"🚨 Wake word detected: '{wake_word}' in '{text}'")
                        if self.callback_function:
                            self.callback_function(wake_word, text)
                        return  # Exit after first match

        except Exception as e:
            logger.error(f"❌ Whisper processing error: {e}")
