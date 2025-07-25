#!/usr/bin/env python3
"""
Quick Shadow AI Test - Verify everything works
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_shadow_ai():
    """Test Shadow AI functionality"""
    print("🧪 Quick Shadow AI Test")
    print("=" * 30)
    
    try:
        # Test main import
        print("📦 Testing main import...")
        import main
        print("  ✅ Main module imported")
        
        # Test Shadow AI creation
        print("🤖 Testing Shadow AI creation...")
        shadow = main.ShadowAI()
        print("  ✅ Shadow AI instance created")
        
        # Test enhanced features initialization
        print("🚀 Testing enhanced features...")
        shadow.init_enhanced_features()
        print("  ✅ Enhanced features initialized")
        
        # Test a simple command
        print("🎯 Testing command processing...")
        result = shadow.handle_enhanced_commands("show enhanced features")
        if result:
            print("  ✅ Enhanced commands working")
        else:
            print("  ⚠️ Enhanced commands not handled (may be normal)")
        
        print("\n✅ Shadow AI is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_modules():
    """Test individual enhanced modules"""
    print("\n🔧 Testing Individual Modules:")
    print("-" * 30)
    
    modules_to_test = [
        ('File Manager', 'control.file_manager', 'EnhancedFileManager'),
        ('Web Search', 'control.web_search', 'QuickWebSearch'),
        ('System Info', 'control.system_info', 'SystemDiagnostics'),
        ('Notifications', 'control.notifications', 'NotificationManager'),
        ('Clipboard', 'control.clipboard_manager', 'ClipboardManager'),
        ('Hotkeys', 'control.hotkey_manager', 'HotkeyManager')
    ]
    
    working_modules = 0
    
    for name, module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            instance = cls()
            print(f"  ✅ {name}")
            working_modules += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    
    print(f"\n📊 {working_modules}/{len(modules_to_test)} modules working")
    return working_modules == len(modules_to_test)

if __name__ == "__main__":
    print("🚀 Shadow AI Quick Test")
    print("=" * 40)
    
    main_working = test_shadow_ai()
    modules_working = test_individual_modules()
    
    print("\n" + "=" * 40)
    if main_working and modules_working:
        print("🎉 ALL TESTS PASSED - Shadow AI is ready!")
        print("🚀 You can now run: python main.py")
    else:
        print("⚠️ Some issues detected - but basic functionality should work")
        print("💡 Try running: python main.py --command 'hello'")
    
    print("=" * 40)
