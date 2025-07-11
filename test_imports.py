#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Shadow AI imports...")
    
    try:
        # Test config
        import config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        # Test brain modules
        from brain.gpt_agent import GPTAgent, process_command
        print("✅ Brain GPTAgent imported successfully")
    except Exception as e:
        print(f"❌ Brain GPTAgent import failed: {e}")
    
    try:
        from brain.universal_processor import UniversalProcessor
        print("✅ Brain UniversalProcessor imported successfully")
    except Exception as e:
        print(f"❌ Brain UniversalProcessor import failed: {e}")
    
    try:
        from brain.universal_executor import UniversalExecutor
        print("✅ Brain UniversalExecutor imported successfully")
    except Exception as e:
        print(f"❌ Brain UniversalExecutor import failed: {e}")
    
    try:
        # Test control modules
        from control.desktop import desktop_controller
        print("✅ Control Desktop imported successfully")
    except Exception as e:
        print(f"❌ Control Desktop import failed: {e}")
    
    try:
        from control.browser import get_browser_controller, close_browser
        print("✅ Control Browser imported successfully")
    except Exception as e:
        print(f"❌ Control Browser import failed: {e}")
    
    try:
        # Test input modules
        from input.text_input import get_text_input, show_message
        print("✅ Input modules imported successfully")
    except Exception as e:
        print(f"❌ Input modules import failed: {e}")
    
    try:
        # Test utils modules
        from utils.logging import setup_logging
        print("✅ Utils modules imported successfully")
    except Exception as e:
        print(f"❌ Utils modules import failed: {e}")
    
    print("\n🎯 Import test completed!")
    return True

if __name__ == "__main__":
    test_imports()
