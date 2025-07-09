# demo_gui.py
"""
Demo script for Shadow AI Modern GUI
Shows the beautiful interface in action
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_gui():
    """Demo the modern GUI"""
    print("🎨 Shadow AI Modern GUI Demo")
    print("=" * 40)
    print()
    print("✨ Features:")
    print("• Beautiful dark theme with animations")
    print("• Real-time task progress visualization")  
    print("• Voice and text input support")
    print("• Activity log with color coding")
    print("• Example commands for quick testing")
    print("• Animated status indicators")
    print()
    print("🚀 Starting the GUI...")
    
    try:
        from gui_modern import ModernShadowGUI
        
        # Create and show the GUI
        app = ModernShadowGUI()
        
        # Show demo message
        root = app.root
        root.after(2000, lambda: app.add_log_entry("🎉 Demo mode - Try these commands:", "info"))
        root.after(3000, lambda: app.add_log_entry("• 'Write an article about AI'", "info"))
        root.after(4000, lambda: app.add_log_entry("• 'Open Notepad and type hello'", "info"))
        root.after(5000, lambda: app.add_log_entry("• Double-click examples to try them", "success"))
        
        app.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure tkinter is installed and available")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demo_gui()
