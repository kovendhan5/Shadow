#!/usr/bin/env python3
"""
Test the GUI with error handling
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    try:
        print("🔧 Testing GUI imports...")
        
        # Test imports
        import tkinter as tk
        print("✅ tkinter imported")
        
        import math
        print("✅ math imported")
        
        import random
        print("✅ random imported")
        
        # Test GUI
        from gui_modern import ModernShadowGUI
        print("✅ GUI module imported successfully")
        
        print("🚀 Creating GUI instance...")
        app = ModernShadowGUI()
        print("✅ GUI instance created")
        
        print("🎨 Starting GUI...")
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
