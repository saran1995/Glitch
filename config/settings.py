"""
Glitch Configuration Settings
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
LOGS_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"

# GUI Settings
GUI_CONFIG = {
    "window_title": "G.L.I.T.C.H Voice Assistant",
    "window_size": "600x500",
    "theme": {
        "bg_color": "#000000",
        "primary_color": "#00ffff",
        "secondary_color": "#00ff00",
        "accent_color": "#ffcc00",
        "error_color": "#ff0000"
    },
    "animation": {
        "fps": 10,
        "face_size": 300
    }
}

# Audio Settings (for future steps)
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "chunk_size": 1024,
    "channels": 1,
    "timeout": 10,
    "phrase_time_limit": 5
}

# Development Settings
DEBUG = True
LOG_LEVEL = "INFO" if not DEBUG else "DEBUG"

# Phase tracking
CURRENT_PHASE = "step1"  # step1, step2, step3, phase1, phase2, phase3
