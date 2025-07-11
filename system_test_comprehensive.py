#!/usr/bin/env python3
"""
Shadow AI - Comprehensive System Test
Test all major components and functionality
"""

import sys
import os
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Comprehensive system test"""
    print("🧪 Shadow AI - Comprehensive System Test")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Configuration
    print("\n1. Testing Configuration...")
    try:
        import config
        print("   ✅ Config module imported")
        print(f"   ✅ Default LLM Provider: {config.DEFAULT_LLM_PROVIDER}")
        print(f"   ✅ Voice Enabled: {config.VOICE_ENABLED}")
        results['config'] = True
    except Exception as e:
        print(f"   ❌ Config test failed: {e}")
        results['config'] = False
    
    # Test 2: Brain modules
    print("\n2. Testing Brain Modules...")
    try:
        from brain.gpt_agent import GPTAgent, process_command
        print("   ✅ GPTAgent imported")
        
        from brain.universal_processor import UniversalProcessor
        print("   ✅ UniversalProcessor imported")
        
        from brain.universal_executor import UniversalExecutor
        print("   ✅ UniversalExecutor imported")
        
        results['brain'] = True
    except Exception as e:
        print(f"   ❌ Brain modules test failed: {e}")
        results['brain'] = False
    
    # Test 3: Control modules
    print("\n3. Testing Control Modules...")
    try:
        from control.desktop import desktop_controller
        print("   ✅ Desktop controller imported")
        
        from control.browser import get_browser_controller
        print("   ✅ Browser controller imported")
        
        from control.documents import document_controller
        print("   ✅ Document controller imported")
        
        results['control'] = True
    except Exception as e:
        print(f"   ❌ Control modules test failed: {e}")
        results['control'] = False
    
    # Test 4: Input modules
    print("\n4. Testing Input Modules...")
    try:
        from input.text_input import get_text_input
        print("   ✅ Text input imported")
        
        from input.voice_input import get_voice_input
        print("   ✅ Voice input imported")
        
        results['input'] = True
    except Exception as e:
        print(f"   ❌ Input modules test failed: {e}")
        results['input'] = False
    
    # Test 5: Utils modules
    print("\n5. Testing Utils Modules...")
    try:
        from utils.logging import setup_logging
        print("   ✅ Logging utils imported")
        
        from utils.confirm import confirm_action
        print("   ✅ Confirm utils imported")
        
        results['utils'] = True
    except Exception as e:
        print(f"   ❌ Utils modules test failed: {e}")
        results['utils'] = False
    
    # Test 6: GUI modules
    print("\n6. Testing GUI Modules...")
    try:
        from gui.gui_working import ShadowWorkingGUI
        print("   ✅ Working GUI imported")
        
        from gui.gui_premium import ShadowPremiumGUI
        print("   ✅ Premium GUI imported")
        
        from gui.gui_cyberpunk import ShadowCyberpunkGUI
        print("   ✅ Cyberpunk GUI imported")
        
        try:
            from gui.gui_modern import ShadowModernGUI
            print("   ✅ Modern GUI imported")
        except ImportError:
            print("   ⚠️ Modern GUI import failed (CustomTkinter not available)")
        
        results['gui'] = True
    except Exception as e:
        print(f"   ❌ GUI modules test failed: {e}")
        results['gui'] = False
    
    # Test 7: Main application
    print("\n7. Testing Main Application...")
    try:
        from main import ShadowAI
        print("   ✅ Main ShadowAI class imported")
        results['main'] = True
    except Exception as e:
        print(f"   ❌ Main application test failed: {e}")
        results['main'] = False
    
    # Test 8: AI Agent functionality
    print("\n8. Testing AI Agent...")
    try:
        agent = GPTAgent()
        print("   ✅ GPTAgent instance created")
        if agent.client_available:
            print("   ✅ AI client is available")
        else:
            print("   ⚠️ AI client not available (API key may not be configured)")
        results['ai_agent'] = True
    except Exception as e:
        print(f"   ❌ AI Agent test failed: {e}")
        results['ai_agent'] = False
    
    # Test 9: Launcher functionality
    print("\n9. Testing Launcher...")
    try:
        from launchers.launch_gui_new import test_gui_import
        print("   ✅ GUI launcher imported")
        results['launcher'] = True
    except Exception as e:
        print(f"   ❌ Launcher test failed: {e}")
        results['launcher'] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():15} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Shadow AI is ready to use.")
    elif passed >= total * 0.8:
        print("✅ Most tests passed. Shadow AI should work with minor issues.")
    else:
        print("⚠️ Several tests failed. Please check your installation.")
    
    return passed == total

if __name__ == "__main__":
    try:
        test_system()
    except Exception as e:
        print(f"❌ System test crashed: {e}")
        traceback.print_exc()
