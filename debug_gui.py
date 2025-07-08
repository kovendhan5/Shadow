#!/usr/bin/env python3
"""
Debug version of the GUI to catch errors
"""
import sys
import traceback

def test_gui():
    try:
        print("🔧 Testing GUI components...")
        
        # Test basic imports
        import tkinter as tk
        print("✅ tkinter imported")
        
        import math
        print("✅ math imported")
        
        import random
        print("✅ random imported")
        
        # Test creating a simple tkinter window first
        print("🪟 Testing basic tkinter window...")
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")
        
        label = tk.Label(root, text="Test GUI", font=('Arial', 16))
        label.pack(pady=50)
        
        # Auto close after 2 seconds
        root.after(2000, root.destroy)
        root.mainloop()
        print("✅ Basic tkinter window works")
        
        # Now test our GUI imports
        print("📦 Testing Shadow AI GUI imports...")
        
        try:
            from brain.universal_processor import process_universal_command
            print("✅ universal_processor imported")
        except Exception as e:
            print(f"⚠️ universal_processor import failed: {e}")
        
        try:
            from brain.universal_executor import execute_universal_task
            print("✅ universal_executor imported")
        except Exception as e:
            print(f"⚠️ universal_executor import failed: {e}")
        
        try:
            from utils.logging import setup_logging
            print("✅ logging utils imported")
        except Exception as e:
            print(f"⚠️ logging utils import failed: {e}")
        
        # Test GUI class import
        print("🎨 Testing GUI class import...")
        from gui_modern import ModernShadowGUI
        print("✅ ModernShadowGUI class imported")
        
        # Test GUI creation
        print("🚀 Testing GUI creation...")
        app = ModernShadowGUI()
        print("✅ GUI object created successfully")
        
        # Test running for 3 seconds
        print("⏰ Testing GUI run for 3 seconds...")
        app.root.after(3000, app.root.destroy)
        app.run()
        print("✅ GUI ran successfully!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()
