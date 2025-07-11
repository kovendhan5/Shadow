#!/usr/bin/env python3
"""
Shadow AI - Simple Launcher
Quick launcher to get Shadow AI working immediately
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def launch_shadow_ai():
    """Launch Shadow AI with best available interface"""
    print("🚀 Shadow AI - Simple Launcher")
    print("=" * 40)
    
    # Try to launch the Working GUI first
    print("🎯 Attempting to launch Working GUI...")
    try:
        from gui.gui_working import ShadowWorkingGUI
        print("✅ Working GUI imported successfully")
        
        app = ShadowWorkingGUI()
        print("✅ Working GUI initialized")
        print("🎉 Launching Shadow AI Working Interface...")
        app.run()
        return True
        
    except Exception as e:
        print(f"❌ Working GUI failed: {e}")
    
    # Fallback to Premium GUI
    print("🎯 Attempting to launch Premium GUI...")
    try:
        from gui.gui_premium import ShadowPremiumGUI
        print("✅ Premium GUI imported successfully")
        
        app = ShadowPremiumGUI()
        print("✅ Premium GUI initialized")
        print("🎉 Launching Shadow AI Premium Interface...")
        app.run()
        return True
        
    except Exception as e:
        print(f"❌ Premium GUI failed: {e}")
    
    # Fallback to command line
    print("🎯 Attempting to launch Command Line Interface...")
    try:
        from main import ShadowAI
        print("✅ Main ShadowAI imported successfully")
        
        app = ShadowAI()
        print("✅ ShadowAI initialized")
        print("🎉 Launching Shadow AI Command Line Interface...")
        app.run_interactive()
        return True
        
    except Exception as e:
        print(f"❌ Command line failed: {e}")
    
    print("❌ All launch attempts failed. Please check your installation.")
    return False

if __name__ == "__main__":
    try:
        success = launch_shadow_ai()
        if not success:
            print("\n💡 Troubleshooting Tips:")
            print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
            print("2. Configure your API key in .env file")
            print("3. Check Python version (3.8+ required)")
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Launcher crashed: {e}")
        input("\nPress Enter to exit...")
