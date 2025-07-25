#!/usr/bin/env python3
"""
Shadow AI Project Setup and Path Configuration
Ensures proper Python path and module imports
"""

import sys
import os
import subprocess

def setup_python_path():
    """Add project root to Python path"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print(f"✅ Added to Python path: {project_root}")

def test_imports():
    """Test critical imports"""
    print("🧪 Testing critical imports...")
    
    try:
        import main
        print("  ✅ main module")
    except ImportError as e:
        print(f"  ❌ main module: {e}")
        return False
    
    try:
        import brain
        print("  ✅ brain module")
    except ImportError as e:
        print(f"  ❌ brain module: {e}")
    
    try:
        import control
        print("  ✅ control module")
    except ImportError as e:
        print(f"  ❌ control module: {e}")
        return False
    
    # Test enhanced features
    try:
        from control.file_manager import EnhancedFileManager
        print("  ✅ file_manager")
    except ImportError as e:
        print(f"  ❌ file_manager: {e}")
    
    try:
        from control.web_search import QuickWebSearch
        print("  ✅ web_search")
    except ImportError as e:
        print(f"  ❌ web_search: {e}")
    
    try:
        from control.system_info import SystemDiagnostics
        print("  ✅ system_info")
    except ImportError as e:
        print(f"  ❌ system_info: {e}")
    
    try:
        from control.notifications import NotificationManager
        print("  ✅ notifications")
    except ImportError as e:
        print(f"  ❌ notifications: {e}")
    
    try:
        from control.clipboard_manager import ClipboardManager
        print("  ✅ clipboard_manager")
    except ImportError as e:
        print(f"  ❌ clipboard_manager: {e}")
    
    try:
        from control.hotkey_manager import HotkeyManager
        print("  ✅ hotkey_manager")
    except ImportError as e:
        print(f"  ❌ hotkey_manager: {e}")
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'psutil', 'requests', 'pyperclip', 'keyboard', 
        'pynput', 'pillow', 'pyautogui'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def create_startup_script():
    """Create a proper startup script"""
    startup_script = """#!/usr/bin/env python3
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run Shadow AI
if __name__ == "__main__":
    from main import main
    main()
"""
    
    with open('run_shadow.py', 'w') as f:
        f.write(startup_script)
    
    print("✅ Created run_shadow.py startup script")

def main():
    """Main setup function"""
    print("🚀 Shadow AI Project Setup")
    print("=" * 40)
    
    # Setup Python path
    setup_python_path()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test imports
    imports_ok = test_imports()
    
    # Create startup script
    create_startup_script()
    
    print("\n" + "=" * 40)
    if deps_ok and imports_ok:
        print("✅ Shadow AI setup complete!")
        print("🚀 Ready to run: python run_shadow.py")
    else:
        print("⚠️ Setup issues detected - check messages above")
        print("💡 Try: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
