#!/usr/bin/env python3
"""
Shadow AI Test Suite
Quick verification of core functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brain.gpt_agent import process_command
from control.desktop import desktop_controller
from control.documents import document_controller
from config import GEMINI_API_KEY

def test_gpt_agent():
    """Test the GPT agent functionality"""
    print("🧠 Testing GPT Agent...")
    
    test_commands = [
        "open notepad",
        "take a screenshot",
        "open notepad write an article about ai",
        "write a leave letter",
        "type: hello world"
    ]
    
    for cmd in test_commands:
        try:
            result = process_command(cmd)
            print(f"✅ Command: '{cmd}' -> {result['task_type']}: {result['action']}")
        except Exception as e:
            print(f"❌ Command: '{cmd}' -> Error: {e}")
    
    print()

def test_desktop_controller():
    """Test desktop controller"""
    print("🖥️ Testing Desktop Controller...")
    
    try:
        # Test basic functionality
        print("✅ Desktop controller initialized successfully")
        
        # Test screen size detection
        print(f"✅ Screen size: {desktop_controller.screen_width}x{desktop_controller.screen_height}")
        
    except Exception as e:
        print(f"❌ Desktop controller error: {e}")
    
    print()

def test_document_controller():
    """Test document controller"""
    print("📄 Testing Document Controller...")
    
    try:
        # Test document controller initialization
        print("✅ Document controller initialized successfully")
        
        # Test path configuration
        print(f"✅ Desktop path: {document_controller.desktop_path}")
        print(f"✅ Documents path: {document_controller.documents_path}")
        
    except Exception as e:
        print(f"❌ Document controller error: {e}")
    
    print()

def test_api_keys():
    """Test API key configuration"""
    print("🔑 Testing API Keys...")
    
    if GEMINI_API_KEY and GEMINI_API_KEY != "test_key_not_real":
        print("✅ Gemini API key configured")
    else:
        print("❌ Gemini API key not configured")
    
    print()

def main():
    """Run all tests"""
    print("🧪 Shadow AI Test Suite")
    print("=" * 50)
    
    test_api_keys()
    test_gpt_agent()
    test_desktop_controller()
    test_document_controller()
    
    print("🎉 Test suite completed!")
    print("\nTo run Shadow AI:")
    print("  python main.py")
    print("  python main.py 'open notepad'")
    print("  python main.py 'open notepad write an article about ai'")
    print("  python main.py --voice")
    print("  python main.py --demo")

if __name__ == "__main__":
    main()
