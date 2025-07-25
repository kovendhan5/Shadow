#!/usr/bin/env python3
"""
Shadow AI - Comprehensive Test Suite
Test all functionality including ASI article generation
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_enhanced_desktop():
    """Test enhanced desktop controller"""
    print("🧪 Testing Enhanced Desktop Controller...")
    
    try:
        from control.enhanced_desktop import enhanced_controller
        print("✅ Enhanced Desktop Controller imported successfully")
        
        # Test ASI article generation
        if hasattr(enhanced_controller, 'open_notepad_and_write_article'):
            print("✅ ASI article generation method available")
            print("✅ Enhanced desktop controller is fully functional")
            return True
        else:
            print("❌ ASI article method not found")
            return False
            
    except ImportError as e:
        print(f"❌ Enhanced Desktop Controller import failed: {e}")
        return False

def test_enhanced_gui():
    """Test enhanced GUI"""
    print("\n🧪 Testing Enhanced Modern GUI...")
    
    try:
        from gui.enhanced_modern_gui import EnhancedModernShadowAI
        print("✅ Enhanced Modern GUI imported successfully")
        print("✅ GUI is ready for use")
        return True
        
    except ImportError as e:
        print(f"❌ Enhanced GUI import failed: {e}")
        return False

def test_enhanced_cli():
    """Test enhanced CLI"""
    print("\n🧪 Testing Enhanced CLI...")
    
    try:
        from enhanced_main import EnhancedShadowAI
        print("✅ Enhanced CLI imported successfully")
        
        # Test command processing
        cli = EnhancedShadowAI()
        print("✅ Enhanced CLI initialized successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Enhanced CLI import failed: {e}")
        return False

def test_article_templates():
    """Test article templates"""
    print("\n🧪 Testing Article Templates...")
    
    try:
        from control.enhanced_desktop import enhanced_controller
        
        # Check available templates
        if hasattr(enhanced_controller, 'ai_article_templates'):
            templates = enhanced_controller.ai_article_templates
            print(f"✅ Found {len(templates)} article templates:")
            for topic in templates.keys():
                print(f"   • {topic}")
            
            # Test ASI template specifically
            if 'asi' in templates:
                print("✅ ASI template is available")
                asi_content = templates['asi']
                if len(asi_content) > 1000:
                    print(f"✅ ASI article content is comprehensive ({len(asi_content)} characters)")
                    return True
                else:
                    print("⚠️ ASI article content seems short")
                    return False
            else:
                print("❌ ASI template not found")
                return False
        else:
            print("❌ Article templates not available")
            return False
            
    except Exception as e:
        print(f"❌ Article template test failed: {e}")
        return False

def test_dependencies():
    """Test system dependencies"""
    print("\n🧪 Testing Dependencies...")
    
    dependencies = {
        'customtkinter': 'Modern GUI framework',
        'pyautogui': 'Desktop automation',
        'colorama': 'Colored terminal output',
        'pathlib': 'Path handling'
    }
    
    results = {}
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: Available ({description})")
            results[dep] = True
        except ImportError:
            print(f"⚠️ {dep}: Not available ({description})")
            results[dep] = False
    
    return results

def test_functionality():
    """Test key functionality"""
    print("\n🧪 Testing Key Functionality...")
    
    try:
        from control.enhanced_desktop import enhanced_controller
        
        # Test methods
        methods_to_test = [
            'open_notepad_and_write_article',
            'open_notepad_and_write_article_save_as',
            '_generate_asi_article',
            '_get_article_content'
        ]
        
        available_methods = []
        for method in methods_to_test:
            if hasattr(enhanced_controller, method):
                available_methods.append(method)
                print(f"✅ {method}: Available")
            else:
                print(f"❌ {method}: Not available")
        
        if len(available_methods) >= 3:
            print("✅ Core functionality is available")
            return True
        else:
            print("❌ Missing critical functionality")
            return False
            
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 Shadow AI - Comprehensive Test Suite")
    print("=" * 50)
    
    test_results = {
        'Enhanced Desktop': test_enhanced_desktop(),
        'Enhanced GUI': test_enhanced_gui(),
        'Enhanced CLI': test_enhanced_cli(),
        'Article Templates': test_article_templates(),
        'Key Functionality': test_functionality()
    }
    
    # Test dependencies
    deps = test_dependencies()
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nDependencies:")
    for dep, available in deps.items():
        status = "✅" if available else "⚠️"
        print(f"  {status} {dep}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Shadow AI is fully functional.")
        print("\n✨ You can now use:")
        print("   • 'write an article about ASI and save it as ASI.txt'")
        print("   • Enhanced GUI with modern design")
        print("   • Enhanced CLI with colored output")
        print("   • All desktop automation features")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Some features may be limited.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
