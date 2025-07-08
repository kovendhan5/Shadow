#!/usr/bin/env python3
"""
Demo: Orpheus Emotional AI Conversations
Demonstrates the emotional AI capabilities using Gemini API
"""

import sys
import os
import time
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from brain.orpheus_ai import (
        EmotionalAI, 
        chat_with_orpheus, 
        get_orpheus_emotional_state, 
        get_orpheus_greeting, 
        reset_orpheus_conversation,
        get_conversation_summary
    )
    from config import GEMINI_API_KEY
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def print_header():
    """Print the demo header"""
    print("=" * 70)
    print("🎭 ORPHEUS EMOTIONAL AI DEMONSTRATION")
    print("=" * 70)
    print("💡 Orpheus is an emotionally intelligent AI that:")
    print("   • Recognizes and responds to emotions")
    print("   • Adapts its emotional state based on conversation")
    print("   • Provides empathetic and contextual responses")
    print("   • Uses advanced Gemini AI for natural conversations")
    print("=" * 70)
    print()

def demo_emotional_conversation():
    """Demo the emotional conversation capabilities"""
    print("🚀 Starting Orpheus Emotional AI Demo...")
    print()
    
    # Check API key
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key_here":
        print("❌ Error: Gemini API key not configured!")
        print("Please set your GEMINI_API_KEY in the .env file")
        return
    
    try:
        # Initialize Orpheus
        ai = EmotionalAI()
        print("✅ Orpheus initialized successfully!")
        print(f"📊 Current emotional state: {ai.get_emotional_state_description()}")
        print()
        
        # Get greeting
        greeting = get_orpheus_greeting()
        print("🎭 Orpheus:", greeting)
        print()
        
        # Demo conversation scenarios
        demo_scenarios = [
            ("I'm feeling really excited about my new job!", "excited"),
            ("I'm worried about my presentation tomorrow", "worried"),
            ("I just had the most amazing day!", "happy"),
            ("I'm feeling a bit overwhelmed with everything", "overwhelmed"),
            ("Thank you for being so understanding", "grateful")
        ]
        
        print("🎬 Demo Conversation Scenarios:")
        print("-" * 40)
        
        for i, (message, emotion_type) in enumerate(demo_scenarios, 1):
            print(f"Scenario {i}: {emotion_type.title()} User")
            print(f"👤 User: {message}")
            
            # Get Orpheus response
            response = chat_with_orpheus(message)
            print(f"🎭 Orpheus: {response}")
            
            # Show emotional state change
            current_state = get_orpheus_emotional_state()
            print(f"📊 Orpheus is now: {current_state}")
            print("-" * 40)
            
            # Small delay for readability
            time.sleep(1)
        
        # Show conversation summary
        print("\n📈 Conversation Summary:")
        summary = get_conversation_summary()
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        print("\n✨ Demo completed successfully!")
        print("🎯 To try Orpheus interactively, run: python gui_orpheus.py")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

def interactive_chat():
    """Interactive chat with Orpheus"""
    print("\n🗣️  Interactive Chat Mode")
    print("Type 'quit' to exit, 'reset' to reset conversation, 'state' to see emotional state")
    print("-" * 70)
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye! Thanks for chatting with Orpheus!")
                break
            elif user_input.lower() == 'reset':
                reset_orpheus_conversation()
                print("🔄 Conversation reset!")
                continue
            elif user_input.lower() == 'state':
                state = get_orpheus_emotional_state()
                print(f"📊 Orpheus emotional state: {state}")
                continue
            elif not user_input:
                continue
            
            # Get response from Orpheus
            response = chat_with_orpheus(user_input)
            print(f"🎭 Orpheus: {response}")
            
            # Show current emotional state
            state = get_orpheus_emotional_state()
            print(f"📊 Current state: {state}")
            
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Error in interactive chat: {e}")

def main():
    """Main demo function"""
    print_header()
    
    print("Choose demo mode:")
    print("1. Automated Demo (shows various emotional scenarios)")
    print("2. Interactive Chat (chat directly with Orpheus)")
    print("3. Both (automated demo followed by interactive chat)")
    print()
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            demo_emotional_conversation()
        elif choice == "2":
            interactive_chat()
        elif choice == "3":
            demo_emotional_conversation()
            print("\n" + "=" * 70)
            interactive_chat()
        else:
            print("Invalid choice. Running automated demo...")
            demo_emotional_conversation()
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
