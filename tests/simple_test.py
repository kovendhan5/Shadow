# simple_test.py
"""
Simple test to verify Shadow AI basic functionality
"""

import os
import sys

# Set test environment variables
os.environ['OPENAI_API_KEY'] = 'test_key_not_real'
os.environ['GEMINI_API_KEY'] = 'test_key_not_real'
os.environ['OLLAMA_URL'] = 'http://localhost:11434'

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from brain.gpt_agent import process_command
        print("✅ GPT Agent import successful")
        
        from control.desktop import DesktopController
        print("✅ Desktop Controller import successful")
        
        from control.documents import DocumentController
        print("✅ Document Controller import successful")
        
        from utils.confirm import ConfirmationManager
        print("✅ Confirmation Manager import successful")
        
        from task_manager import TaskManager
        print("✅ Task Manager import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_command_processing():
    """Test basic command processing"""
    try:
        from brain.gpt_agent import process_command
        
        # Test simple commands
        result = process_command("open notepad")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'open_notepad'
        print("✅ Basic command processing works")
        
        result = process_command("type: Hello World")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'type_text'
        assert result['parameters']['text'] == 'Hello World'
        print("✅ Type command processing works")
        
        return True
    except Exception as e:
        print(f"❌ Command processing error: {e}")
        return False

def test_desktop_controller():
    """Test desktop controller"""
    try:
        from control.desktop import DesktopController
        
        controller = DesktopController()
        print(f"✅ Desktop Controller initialized - Screen: {controller.screen_width}x{controller.screen_height}")
        
        return True
    except Exception as e:
        print(f"❌ Desktop Controller error: {e}")
        return False

def test_document_controller():
    """Test document controller"""
    try:
        from control.documents import DocumentController
        
        controller = DocumentController()
        print("✅ Document Controller initialized")
        
        return True
    except Exception as e:
        print(f"❌ Document Controller error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Shadow AI - Simple Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Command Processing", test_basic_command_processing),
        ("Desktop Controller", test_desktop_controller),
        ("Document Controller", test_document_controller)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Shadow AI is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
