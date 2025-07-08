#!/usr/bin/env python3
"""
Simple syntax check for GUI
"""
import sys
import traceback

def check_gui_syntax():
    try:
        print("🔍 Checking GUI syntax and imports...")
        
        # Check if we can import the GUI without running it
        import ast
        
        with open('gui_modern.py', 'r', encoding='utf-8') as f:
            gui_code = f.read()
        
        # Parse the code to check for syntax errors
        try:
            ast.parse(gui_code)
            print("✅ GUI syntax is valid")
        except SyntaxError as e:
            print(f"❌ Syntax error in GUI: {e}")
            return False
        
        # Test imports without running
        print("📦 Testing imports...")
        
        import tkinter as tk
        print("✅ tkinter works")
        
        import math
        print("✅ math works")
        
        import random  
        print("✅ random works")
        
        # Try importing the GUI class
        from gui_modern import ModernShadowGUI
        print("✅ GUI class imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if check_gui_syntax():
        print("\n🎯 GUI syntax and imports are OK. Let's try a minimal run...")
        
        try:
            from gui_modern import ModernShadowGUI
            
            # Create but don't run
            app = ModernShadowGUI()
            print("✅ GUI object created successfully")
            
            # Try to get window info
            print(f"📐 Window size: {app.root.geometry()}")
            print(f"🎨 Window title: {app.root.title()}")
            
            # Destroy immediately
            app.root.destroy()
            print("✅ GUI test completed successfully")
            
        except Exception as e:
            print(f"❌ Error creating GUI: {e}")
            traceback.print_exc()
    else:
        print("❌ GUI has syntax or import issues")
