#!/usr/bin/env python3
"""
Shadow AI Ultra Modern GUI Launcher
Beautiful, modern interface launcher with full feature integration
"""

import sys
import os
import subprocess
from pathlib import Path

def setup_environment():
    """Setup the environment for running the GUI"""
    project_root = Path(__file__).parent
    
    # Add project root to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Change to project directory
    os.chdir(project_root)
    
    print("🚀 Shadow AI Ultra Modern GUI Launcher")
    print("=" * 50)
    print(f"📁 Project Root: {project_root}")
    print(f"🐍 Python Version: {sys.version}")
    print("=" * 50)

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "customtkinter",
        "pillow",
        "psutil",
        "requests",
        "pyautogui"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            print("Please install manually: pip install " + " ".join(missing_packages))
            return False
    
    return True

def launch_gui():
    """Launch the ultra modern GUI"""
    try:
        # Import and run the GUI
        gui_path = Path(__file__).parent / "gui" / "ultra_modern_gui.py"
        
        if gui_path.exists():
            print("🎨 Launching Ultra Modern GUI...")
            sys.path.insert(0, str(gui_path.parent))
            from ultra_modern_gui import main
            main()
        else:
            print(f"❌ GUI file not found: {gui_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main launcher function"""
    print("\n🤖 Shadow AI Ultra Modern Interface")
    print("🎨 Beautiful • 🚀 Fast • 💻 Powerful")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        input("Press Enter to exit...")
        return
    
    print("\n✅ All dependencies ready!")
    
    # Launch GUI
    print("\n🎨 Starting Ultra Modern GUI...")
    success = launch_gui()
    
    if not success:
        print("\n❌ Failed to launch GUI!")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
