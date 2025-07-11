#!/usr/bin/env python3
"""
Comprehensive Shadow AI System Test
Tests all core functionality after cleanup and reorganization
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing Module Imports...")
    
    try:
        import config
        print("✅ Config module")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    try:
        from brain import GPTAgent, process_command
        print("✅ Brain module (GPTAgent)")
    except Exception as e:
        print(f"❌ Brain module error: {e}")
        return False
    
    try:
        from control import desktop_controller
        print("✅ Control module")
    except Exception as e:
        print(f"❌ Control module error: {e}")
        return False
    
    try:
        from input import get_text_input
        print("✅ Input module")
    except Exception as e:
        print(f"❌ Input module error: {e}")
        return False
    
    try:
        from utils import setup_logging
        print("✅ Utils module")
    except Exception as e:
        print(f"❌ Utils module error: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        import config
        
        # Check API key
        if config.GEMINI_API_KEY and len(config.GEMINI_API_KEY) > 20:
            print("✅ Gemini API key configured")
        else:
            print("⚠️ Gemini API key not configured")
        
        # Check default provider
        print(f"✅ Default LLM provider: {config.DEFAULT_LLM_PROVIDER}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_ai_agent():
    """Test AI agent functionality"""
    print("\n🧠 Testing AI Agent...")
    
    try:
        from brain import GPTAgent, process_command
        
        # Initialize agent
        agent = GPTAgent()
        print(f"✅ Agent initialized (provider: {agent.provider})")
        
        # Test command processing
        result = process_command("open notepad")
        if result and 'action' in result:
            print(f"✅ Command processing works: {result['action']}")
        else:
            print("⚠️ Command processing returned unexpected result")
        
        return True
    except Exception as e:
        print(f"❌ AI Agent error: {e}")
        return False

def test_gui_files():
    """Test GUI files availability"""
    print("\n🎨 Testing GUI Files...")
    
    gui_files = [
        'gui/gui_working.py',
        'gui/gui_modern.py', 
        'gui/gui_premium.py',
        'gui/gui_ultra.py',
        'gui/gui_cyberpunk.py',
        'gui/gui_orpheus.py',
        'gui/gui_enhanced.py'
    ]
    
    available_guis = []
    for gui_file in gui_files:
        if os.path.exists(gui_file):
            available_guis.append(gui_file)
            print(f"✅ {gui_file}")
        else:
            print(f"❌ Missing: {gui_file}")
    
    print(f"📊 Available GUIs: {len(available_guis)}/7")
    return len(available_guis) >= 5  # At least 5 GUIs should be available

def test_launchers():
    """Test launcher files"""
    print("\n🚀 Testing Launchers...")
    
    launchers = ['launch.bat', 'start.bat', 'cleanup.bat']
    for launcher in launchers:
        if os.path.exists(launcher):
            print(f"✅ {launcher}")
        else:
            print(f"❌ Missing: {launcher}")
    
    return all(os.path.exists(launcher) for launcher in launchers)

def main():
    """Run all tests"""
    print("🧪 Shadow AI - Comprehensive System Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration), 
        ("AI Agent", test_ai_agent),
        ("GUI Files", test_gui_files),
        ("Launchers", test_launchers)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Shadow AI is ready to use!")
        print("\n🚀 Quick start:")
        print("• Run 'launch.bat' for GUI launcher")
        print("• Run 'start.bat' for command line")
        print("• Run 'python main.py' for direct launch")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
