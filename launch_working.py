#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shadow AI Working Launcher
Guaranteed to work launcher with proper setup
"""

import sys
import os

def setup_environment():
    """Setup proper environment for Shadow AI"""
    # Add project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Set working directory
    os.chdir(project_root)
    
    print(f"✅ Environment setup complete")
    print(f"📁 Working directory: {project_root}")

def launch_shadow_ai():
    """Launch Shadow AI with proper error handling"""
    try:
        print("🚀 Launching Shadow AI...")
        
        # Import main module
        import main
        
        # Create Shadow AI instance
        shadow = main.ShadowAI()
        
        # Initialize enhanced features
        try:
            shadow.init_enhanced_features()
            print("✅ Enhanced features loaded")
        except Exception as e:
            print(f"⚠️ Enhanced features issue: {e}")
            print("📝 Basic functionality will still work")
        
        print("\n" + "=" * 50)
        print("🤖 Shadow AI is now ready!")
        print("=" * 50)
        
        # Show available commands
        print("\n🎯 Try these commands:")
        print("• 'show enhanced features' - See what's available")
        print("• 'organize Downloads folder' - Organize files")
        print("• 'show system information' - System stats")
        print("• 'search Google for Python' - Web search")
        print("• 'take a screenshot' - Capture screen")
        print("• 'quit' or 'exit' - Stop Shadow AI")
        
        # Start interactive mode
        print("\n💬 Enter commands (or 'quit' to exit):")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("🎯 Command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input:
                    print(f"\n🔄 Processing: {user_input}")
                    
                    # Try enhanced commands first
                    handled = shadow.handle_enhanced_commands(user_input)
                    
                    if not handled:
                        # Fall back to regular AI processing
                        try:
                            shadow.process_ai_command(user_input)
                        except Exception as e:
                            print(f"⚠️ Command processing issue: {e}")
                            print("💡 Try another command or 'quit' to exit")
                    
                    print("-" * 40)
                
            except KeyboardInterrupt:
                print("\n👋 Shadow AI stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Try another command or 'quit' to exit")
        
    except Exception as e:
        print(f"💥 Failed to launch Shadow AI: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 Shadow AI Working Launcher")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Launch Shadow AI
    success = launch_shadow_ai()
    
    if not success:
        print("\n💡 Try these troubleshooting steps:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Run: python verify_working.py")
        print("3. Check the README.md for setup instructions")

if __name__ == "__main__":
    main()
