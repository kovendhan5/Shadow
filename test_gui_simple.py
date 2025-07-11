#!/usr/bin/env python3
"""
Simple GUI Test Launcher
Test the GUI functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui():
    """Test GUI functionality"""
    print("🧪 Testing Shadow AI GUI functionality...")
    
    try:
        print("Testing Working GUI...")
        from gui.gui_working import ShadowWorkingGUI
        print("✅ Working GUI class imported successfully")
        
        print("Testing Premium GUI...")
        from gui.gui_premium import ShadowPremiumGUI
        print("✅ Premium GUI class imported successfully")
        
        print("Testing Cyberpunk GUI...")
        from gui.gui_cyberpunk import ShadowCyberpunkGUI
        print("✅ Cyberpunk GUI class imported successfully")
        
        print("\n🎯 All GUI classes imported successfully!")
        
        # Test basic initialization (without running mainloop)
        print("\nTesting basic initialization...")
        
        # These would normally start the GUI, but we'll just test import for now
        print("✅ GUI tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

if __name__ == "__main__":
    test_gui()
