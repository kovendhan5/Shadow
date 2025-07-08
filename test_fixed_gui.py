#!/usr/bin/env python3
"""Test the fixed GUI that should start without voice calibration issues"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fixed_gui():
    print("🔧 Testing Fixed Shadow AI Modern GUI")
    print("=" * 50)
    print("🎯 This version should start without microphone calibration")
    print()
    
    try:
        print("📦 Importing gui_modern...")
        from gui_modern import ModernShadowGUI
        print("✅ Import successful!")
        
        print("🚀 Creating GUI instance...")
        app = ModernShadowGUI()
        print("✅ GUI created successfully!")
        
        print()
        print("🎨 GUI Features:")
        print("  • Beautiful dark theme")
        print("  • Real-time animations")
        print("  • Text command input")
        print("  • Example commands")
        print("  • Voice input (on-demand)")
        print("  • Progress visualization")
        print()
        
        print("🎬 Starting GUI...")
        print("💡 Try these commands:")
        print("  - 'Write an article about AI'")
        print("  - 'Open Notepad'")
        print("  - Double-click examples")
        print("  - Click 🎤 for voice (when ready)")
        print()
        
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_gui()
