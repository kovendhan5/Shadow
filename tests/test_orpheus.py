#!/usr/bin/env python3
"""
Quick Test: Orpheus Emotional AI
Simple verification that the emotional AI system is working
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_orpheus():
    """Test Orpheus AI functionality"""
    print("🎭 Testing Orpheus Emotional AI...")
    print("=" * 50)
    
    # Test 1: Import check
    try:
        from brain.orpheus_ai import EmotionalAI
        print("✅ Orpheus AI module imported successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: API key check
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_key_here":
            print("✅ Gemini API key is configured")
        else:
            print("❌ Gemini API key not configured - please set in .env file")
            return False
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Test 3: Initialize Orpheus
    try:
        ai = EmotionalAI()
        print("✅ Orpheus AI initialized successfully")
        print(f"📊 Initial emotional state: {ai.get_emotional_state_description()}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
    
    # Test 4: Generate greeting
    try:
        greeting = ai.generate_greeting()
        print(f"✅ Greeting generated: {greeting[:50]}...")
    except Exception as e:
        print(f"❌ Greeting generation failed: {e}")
        return False
    
    # Test 5: Test conversation (if API key is working)
    try:
        test_message = "Hello, how are you today?"
        response = ai.generate_emotional_response(test_message)
        print(f"✅ Conversation test successful!")
        print(f"   User: {test_message}")
        print(f"   Orpheus: {response[:100]}...")
        print(f"   New state: {ai.get_emotional_state_description()}")
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        print("   This might be due to API quota or network issues")
        return False
    
    print("\n🎉 All tests passed! Orpheus is ready for emotional conversations!")
    return True

if __name__ == "__main__":
    try:
        success = test_orpheus()
        if success:
            print("\n🚀 To start using Orpheus:")
            print("   • Run: python gui_orpheus.py (Beautiful GUI)")
            print("   • Run: python demo_orpheus.py (Interactive demo)")
            print("   • Run: launch_orpheus_master.bat (Master launcher)")
        else:
            print("\n🔧 Please fix the issues above and try again")
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
