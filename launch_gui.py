# launch_gui.py
"""
Beautiful GUI Launcher for Shadow AI
Modern, animated interface with real-time task visualization
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if all required modules are available"""
    required_modules = [
        'tkinter', 'threading', 'queue', 'datetime', 'pathlib',
        'pyautogui', 'pyttsx3', 'google.generativeai'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Missing required modules: {', '.join(missing_modules)}\n\n"
        error_msg += "Please install them using:\n"
        error_msg += "pip install " + " ".join(missing_modules)
        
        # Show error in a simple dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Missing Dependencies", error_msg)
        root.destroy()
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🧠 Shadow AI - Modern GUI Launcher")
    print("=" * 50)
    
    # Check environment
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required modules.")
        return
    
    # Check .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("⚠️  Warning: .env file not found. Please create it with your API keys.")
        print("   You can copy .env.template to .env and fill in your keys.")
    
    try:
        # Import and run the modern GUI
        from gui_modern import ModernShadowGUI
        
        print("✅ Dependencies loaded successfully")
        print("🚀 Starting Shadow AI Modern GUI...")
        print("📱 The GUI window should open shortly...")
        
        # Create and run the GUI
        app = ModernShadowGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all Shadow AI modules are available.")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        logging.error(f"GUI startup error: {e}")

if __name__ == "__main__":
    main()
