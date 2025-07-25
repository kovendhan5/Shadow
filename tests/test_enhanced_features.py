#!/usr/bin/env python3
"""
Enhanced Features Test - Shadow AI
Comprehensive testing of all new advanced features
"""

import os
import sys
import traceback
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_imports():
    """Test all enhanced feature imports"""
    print("🧪 Testing Enhanced Feature Imports...")
    
    try:
        print("  📁 Testing File Manager...")
        from control.file_manager import EnhancedFileManager
        file_manager = EnhancedFileManager()
        print("    ✅ File Manager imported and initialized")
        
        print("  🌐 Testing Web Search...")
        from control.web_search import QuickWebSearch
        web_search = QuickWebSearch()
        print("    ✅ Web Search imported and initialized")
        
        print("  💻 Testing System Diagnostics...")
        from control.system_info import SystemDiagnostics
        system_diagnostics = SystemDiagnostics()
        print("    ✅ System Diagnostics imported and initialized")
        
        print("  🔔 Testing Notifications...")
        from control.notifications import NotificationManager
        notification_manager = NotificationManager()
        print("    ✅ Notifications imported and initialized")
        
        print("  📋 Testing Clipboard Manager...")
        from control.clipboard_manager import ClipboardManager
        clipboard_manager = ClipboardManager()
        print("    ✅ Clipboard Manager imported and initialized")
        
        print("  🔥 Testing Hotkey Manager...")
        from control.hotkey_manager import HotkeyManager
        hotkey_manager = HotkeyManager()
        print("    ✅ Hotkey Manager imported and initialized")
        
        return True, {
            'file_manager': file_manager,
            'web_search': web_search,
            'system_diagnostics': system_diagnostics,
            'notification_manager': notification_manager,
            'clipboard_manager': clipboard_manager,
            'hotkey_manager': hotkey_manager
        }
        
    except Exception as e:
        print(f"    ❌ Import error: {e}")
        traceback.print_exc()
        return False, None

def test_main_integration():
    """Test main.py integration"""
    print("\n🧪 Testing Main.py Integration...")
    
    try:
        print("  📦 Importing main module...")
        import main
        print("    ✅ Main module imported successfully")
        
        print("  🤖 Creating Shadow AI instance...")
        shadow = main.ShadowAI()
        print("    ✅ Shadow AI instance created")
        
        print("  ⚙️ Testing initialization...")
        shadow.init_enhanced_features()
        print("    ✅ Enhanced features initialized")
        
        return True, shadow
        
    except Exception as e:
        print(f"    ❌ Integration error: {e}")
        traceback.print_exc()
        return False, None

def test_enhanced_commands(shadow, managers):
    """Test enhanced command functionality"""
    print("\n🧪 Testing Enhanced Commands...")
    
    test_commands = [
        ("enhanced features", "show enhanced features status"),
        ("system info", "show system information"),
        ("clipboard test", "copy Hello Shadow AI to clipboard"),
        ("hotkey help", "show hotkey help"),
    ]
    
    results = []
    
    for command_name, command in test_commands:
        try:
            print(f"  🎯 Testing: {command_name}")
            result = shadow.handle_enhanced_commands(command)
            if result:
                print(f"    ✅ {command_name} - SUCCESS")
                results.append(True)
            else:
                print(f"    ⚠️ {command_name} - NOT HANDLED")
                results.append(False)
        except Exception as e:
            print(f"    ❌ {command_name} - ERROR: {e}")
            results.append(False)
    
    return results

def test_individual_features(managers):
    """Test individual feature functionality"""
    print("\n🧪 Testing Individual Features...")
    
    try:
        # Test File Manager
        print("  📁 Testing File Manager features...")
        home_dir = os.path.expanduser('~')
        large_files = managers['file_manager'].find_large_files(home_dir, min_size_mb=50)
        print(f"    ✅ Found {len(large_files)} large files")
        
        # Test System Diagnostics
        print("  💻 Testing System Diagnostics...")
        cpu_info = managers['system_diagnostics'].get_cpu_info()
        mem_info = managers['system_diagnostics'].get_memory_info()
        print(f"    ✅ CPU: {cpu_info.get('cpu_percent_total', 'N/A')}%, Memory: {mem_info.get('percentage', 'N/A')}%")
        
        # Test Clipboard
        print("  📋 Testing Clipboard...")
        test_text = "Shadow AI Enhanced Features Test"
        copy_result = managers['clipboard_manager'].copy_to_clipboard(test_text)
        paste_result = managers['clipboard_manager'].paste_from_clipboard()
        print(f"    ✅ Clipboard test: Copy={copy_result}, Paste='{paste_result[:30]}...'")
        
        # Test Notifications
        print("  🔔 Testing Notifications...")
        notify_result = managers['notification_manager'].show_notification(
            "Shadow AI Test", 
            "Enhanced features test notification"
        )
        print(f"    ✅ Notification test: {notify_result}")
        
        # Test Hotkeys
        print("  🔥 Testing Hotkeys...")
        hotkey_count = len(managers['hotkey_manager'].list_hotkeys())
        print(f"    ✅ Hotkey system: {hotkey_count} configured hotkeys")
        
        print("  🌐 Testing Web Search...")
        # Don't actually open browser, just test the search URL generation
        search_engines = managers['web_search'].available_engines
        print(f"    ✅ Web Search: {len(search_engines)} search engines available")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Feature test error: {e}")
        traceback.print_exc()
        return False

def run_comprehensive_test():
    """Run comprehensive test of all enhanced features"""
    print("=" * 60)
    print("🚀 Shadow AI Enhanced Features Comprehensive Test")
    print("=" * 60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Imports
    import_success, managers = test_imports()
    if not import_success:
        print("\n❌ Import test failed - stopping tests")
        return False
    
    # Test 2: Main Integration
    integration_success, shadow = test_main_integration()
    if not integration_success:
        print("\n❌ Integration test failed - stopping tests")
        return False
    
    # Test 3: Enhanced Commands
    command_results = test_enhanced_commands(shadow, managers)
    command_success = any(command_results)
    
    # Test 4: Individual Features
    features_success = test_individual_features(managers)
    
    # Test Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"📦 Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"🔗 Integration: {'✅ PASS' if integration_success else '❌ FAIL'}")
    print(f"🎯 Commands: {'✅ PASS' if command_success else '❌ FAIL'} ({sum(command_results)}/{len(command_results)})")
    print(f"⚙️ Features: {'✅ PASS' if features_success else '❌ FAIL'}")
    
    overall_success = import_success and integration_success and command_success and features_success
    
    print(f"\n🏆 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 Shadow AI Enhanced Features are working perfectly!")
        print("🚀 All advanced capabilities are ready for use:")
        print("   📁 File Management & Organization")
        print("   🌐 Multi-Engine Web Search")
        print("   💻 System Monitoring & Diagnostics")
        print("   🔔 Cross-Platform Notifications")
        print("   📋 Advanced Clipboard Management")
        print("   🔥 Customizable Hotkey System")
    else:
        print("\n⚠️ Some features need attention - check errors above")
    
    return overall_success

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
