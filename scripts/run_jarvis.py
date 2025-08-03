#!/usr/bin/env python3
"""
Main entry point for Glitch Voice Assistant
"""
import sys
import tkinter as tk
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.gui.main_window import GlitchMainWindow
from src.utils.logger import setup_logger
from config.settings import CURRENT_PHASE


def main():
    """Main application entry point"""
    logger = setup_logger("main")

    print("🤖 Starting GLITCH Voice Assistant")
    print(f"📍 Current Phase: {CURRENT_PHASE}")
    print("=" * 50)

    try:
        # Create main window
        root = tk.Tk()
        app = GlitchMainWindow(root)

        # Handle window close event
        def on_closing():
            app.shutdown()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        logger.info("Starting main event loop")

        # Start the main loop
        root.mainloop()

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        logger.info("Application interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        print("👋 Glitch shutdown complete")
        logger.info("Application shutdown complete")


if __name__ == "__main__":
    main()
