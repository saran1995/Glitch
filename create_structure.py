#!/usr/bin/env python3
"""
Setup script to create the Glitch project structure
"""
import os


def create_project_structure():
    """Create the complete folder structure for Glitch project"""

    folders = [
        "requirements",
        "config",
        "src",
        "src/gui",
        "src/gui/components",
        "src/audio",
        "src/ai",
        "src/hardware",
        "src/utils",
        "tests",
        "assets/icons",
        "assets/sounds",
        "logs",
        "data/conversations",
        "scripts",
        "docs"
    ]

    # Create directories
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

        # Create __init__.py files for Python packages
        if folder.startswith("src/"):
            init_file = os.path.join(folder, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('"""Glitch Voice Assistant Module"""\n')

    print("✅ Project structure created successfully!")
    print("📁 Created folders:")
    for folder in folders:
        print(f"   - {folder}/")


if __name__ == "__main__":
    create_project_structure()
