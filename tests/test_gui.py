#!/usr/bin/env python3
"""Simple test for the modern GUI"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui():
    print("🎨 Testing Shadow AI Modern GUI")
    print("=" * 40)
    
    try:
        print("📦 Importing tkinter...")
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        print("📦 Importing gui_modern...")
        from gui_modern import ModernShadowGUI
        print("✅ gui_modern imported successfully")
        
        print("🚀 Creating GUI instance...")
        app = ModernShadowGUI()
        print("✅ GUI created successfully")
        
        print("🎯 Starting GUI...")
        print("💡 The GUI window should now be visible!")
        print("💡 Try typing a command like 'write an article about AI'")
        print("💡 Or click on an example to try it out")
        print("💡 Close the window to exit")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()
