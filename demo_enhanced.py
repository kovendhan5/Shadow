#!/usr/bin/env python3
"""
Shadow AI Enhanced Features Demo
Showcase all the new advanced capabilities
"""

import os
import sys
import time
from datetime import datetime

def demo_enhanced_features():
    """Demo all enhanced features"""
    print("🎬 Shadow AI Enhanced Features Demo")
    print("=" * 50)
    
    try:
        # Import main Shadow AI
        import main
        shadow = main.ShadowAI()
        
        print("🚀 Initializing enhanced features...")
        shadow.init_enhanced_features()
        
        print("\n🎯 Demo Commands to Try:")
        print("-" * 30)
        
        demo_commands = [
            "show enhanced features",
            "show system information", 
            "find large files over 50MB",
            "organize Downloads folder by type",
            "search Google for Python tutorials",
            "copy Hello from Shadow AI to clipboard",
            "show clipboard history",
            "show hotkey help",
            "test notification"
        ]
        
        for i, cmd in enumerate(demo_commands, 1):
            print(f"{i}. {cmd}")
        
        print("\n" + "=" * 50)
        print("🤖 Interactive Demo Mode")
        print("Type any command above or 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🎯 Enter command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Demo completed!")
                    break
                
                if user_input:
                    print(f"\n🔄 Processing: {user_input}")
                    print("-" * 40)
                    
                    # Try enhanced commands first
                    handled = shadow.handle_enhanced_commands(user_input)
                    
                    if not handled:
                        # Fall back to regular AI processing
                        print("🤖 Processing with AI agent...")
                        shadow.process_ai_command(user_input)
                    
                    print("-" * 40)
                    print("✅ Command completed")
                else:
                    print("Please enter a command")
                    
            except KeyboardInterrupt:
                print("\n👋 Demo interrupted - goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try another command")
        
    except Exception as e:
        print(f"💥 Demo error: {e}")
        import traceback
        traceback.print_exc()

def quick_feature_showcase():
    """Quick showcase of key features"""
    print("⚡ Quick Feature Showcase")
    print("=" * 30)
    
    try:
        import main
        shadow = main.ShadowAI()
        shadow.init_enhanced_features()
        
        # 1. Show enhanced features
        print("\n1. 🚀 Enhanced Features Status:")
        shadow.show_enhanced_features()
        
        # 2. System info
        print("\n2. 💻 System Information:")
        shadow.handle_system_info("show system information")
        
        # 3. Clipboard test
        print("\n3. 📋 Clipboard Test:")
        shadow.handle_clipboard_copy("copy Shadow AI Enhanced Features Demo to clipboard")
        
        # 4. Hotkey help
        print("\n4. 🔥 Hotkey System:")
        shadow.handle_hotkey_command("show hotkey help")
        
        print("\n✨ Showcase completed - all features working!")
        
    except Exception as e:
        print(f"💥 Showcase error: {e}")

if __name__ == "__main__":
    print("🎭 Shadow AI Enhanced Features")
    print("Choose demo mode:")
    print("1. Quick Showcase (automated)")
    print("2. Interactive Demo")
    print("3. Exit")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            quick_feature_showcase()
        elif choice == "2":
            demo_enhanced_features()
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("Invalid choice - running quick showcase")
            quick_feature_showcase()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
    except Exception as e:
        print(f"💥 Error: {e}")
