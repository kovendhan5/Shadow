#!/usr/bin/env python3
"""
Quick test for the enhanced GUI
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from gui_modern import ModernShadowGUI
    print("✅ GUI module imported successfully")
    
    # Test GUI creation
    app = ModernShadowGUI()
    print("✅ GUI created successfully")
    
    # Test for a few seconds to see if there are immediate errors
    app.root.after(3000, app.root.quit)  # Auto-close after 3 seconds
    app.run()
    print("✅ GUI ran without immediate errors")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error creating/running GUI: {e}")
    import traceback
    traceback.print_exc()
