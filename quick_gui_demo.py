#!/usr/bin/env python3
"""
Quick GUI Demo - Showcases Shadow AI Modern GUI
"""

import sys
import os
import time
import threading

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_scenario():
    """Run a demo scenario"""
    print("\n🎬 Demo Scenario: Article Writing")
    print("=" * 50)
    
    try:
        from gui_modern import ModernShadowGUI
        
        print("🚀 Creating GUI...")
        app = ModernShadowGUI()
        
        # Schedule a demo command after GUI loads
        def auto_demo():
            time.sleep(3)  # Wait for GUI to fully load
            print("📝 Auto-filling demo command...")
            
            # Fill in example command
            demo_command = "Write an article about artificial intelligence and its impact on society"
            app.command_entry.delete(1.0, 'end')
            app.command_entry.insert(1.0, demo_command)
            
            # Add demo log entry
            app.add_log_entry("🎬 Demo mode: Ready to execute article writing task", "info")
            app.add_log_entry("💡 Click 'Execute' to see the AI in action!", "success")
        
        # Start demo in background
        threading.Thread(target=auto_demo, daemon=True).start()
        
        print("✨ GUI is now running!")
        print("💡 Demo command will be auto-filled in 3 seconds")
        print("💡 Try clicking 'Execute' to see the AI animation")
        print("💡 Or try voice input with the microphone button")
        print("💡 Double-click examples to try different commands")
        
        app.run()
        
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎨 Shadow AI Modern GUI - Demo Mode")
    print("=" * 40)
    print("✨ This demo showcases the beautiful animated interface")
    print("🎯 Watch the AI process tasks with visual feedback")
    print("🎤 Test voice commands and text input")
    print("📊 Monitor real-time progress and activity logs")
    
    demo_scenario()
