#!/usr/bin/env python3
"""
Shadow AI - GUI Launcher
Simple Python launcher for Shadow AI GUI interfaces
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main launcher function"""
    print("🤖 Shadow AI - GUI Launcher")
    print("=" * 40)
    
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"📁 Project Directory: {project_root}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print()
    
    # Available GUIs
    guis = [
        ("1", "Beautiful GUI (Recommended)", "gui/beautiful_gui.py"),
        ("2", "Ultra Modern GUI (Advanced)", "gui/ultra_modern_gui.py"),
        ("3", "Standard GUI (Classic)", "gui/gui.py"),
        ("4", "Modern GUI (Enhanced)", "gui/modern_gui.py")
    ]
    
    print("🎨 Available GUI Interfaces:")
    for num, name, path in guis:
        status = "✅" if Path(path).exists() else "❌"
        print(f"  {num}. {status} {name}")
    
    print()
    choice = input("Select GUI (1-4) or press Enter for default: ").strip()
    
    # Default to Beautiful GUI
    if not choice:
        choice = "1"
    
    # Find selected GUI
    selected_gui = None
    for num, name, path in guis:
        if choice == num:
            if Path(path).exists():
                selected_gui = (name, path)
                break
            else:
                print(f"❌ {name} not found at {path}")
                return
    
    if not selected_gui:
        print("❌ Invalid selection")
        return
    
    name, path = selected_gui
    print(f"🚀 Launching {name}...")
    print()
    
    try:
        # Launch the selected GUI
        subprocess.run([sys.executable, path], check=True)
        print("✅ GUI closed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
    except KeyboardInterrupt:
        print("🛑 Launcher interrupted")

if __name__ == "__main__":
    main()
