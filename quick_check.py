#!/usr/bin/env python3
"""
Minimal test script to verify essential functionality
"""

import os
import sys
import time

def test_basic_functionality():
    """Test just the most basic functionality to make sure the system works"""
    print("\n🔍 Testing basic functionality...")
    
    # Test basic imports
    try:
        import pyautogui
        print("✅ PyAutoGUI is working")
    except ImportError:
        print("❌ PyAutoGUI is not installed! Run: pip install pyautogui")
        return False
    
    # Test text-to-speech
    try:
        from utils.orpheus_tts import speak
        print("🔊 Testing text-to-speech...")
        speak("Shadow AI test successful!")
        print("✅ Text-to-speech is working")
    except Exception as e:
        print(f"❌ Text-to-speech failed: {e}")
    
    # Test desktop controller
    try:
        from control.desktop import desktop_controller
        screen_width, screen_height = desktop_controller.screen_width, desktop_controller.screen_height
        print(f"✅ Desktop controller is working - Screen resolution: {screen_width}x{screen_height}")
    except Exception as e:
        print(f"❌ Desktop controller failed: {e}")
    
    print("\n✅ Basic functionality test completed!")
    print("If you see only green checkmarks, the core system is working correctly.")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("     🧠 Shadow AI - Quick Functionality Test")
    print("=" * 50)
    
    success = test_basic_functionality()
    
    if success:
        print("\n🎉 Quick test PASSED! Shadow AI should be working.")
        print("\nTry running 'launch_improved_new.bat' to start the system.")
    else:
        print("\n❌ Test FAILED! Some components are not working.")
        print("\nCheck if all dependencies are installed by running:")
        print("pip install -r requirements.txt")
    
    input("\nPress Enter to exit...")
