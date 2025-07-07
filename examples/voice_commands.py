# examples/voice_commands.py
"""
Voice command examples for Shadow AI Agent
This script demonstrates voice-based interaction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input.voice_input import get_voice_input, speak_response
from main import ShadowAI
import time

def voice_interaction_demo():
    """Demonstrate voice interaction"""
    print("🎤 Voice Interaction Demo")
    print("=" * 40)
    
    shadow = ShadowAI()
    shadow.voice_mode = True
    
    speak_response("Hello! I'm Shadow AI. Let me demonstrate voice commands.")
    
    # Predefined voice commands for demo
    demo_commands = [
        "open notepad",
        "type hello world",
        "take a screenshot",
        "open calculator"
    ]
    
    for command in demo_commands:
        print(f"\n🎙️  Simulating voice command: '{command}'")
        speak_response(f"Executing command: {command}")
        
        try:
            shadow.run_single_command(command)
            speak_response("Command completed successfully!")
        except Exception as e:
            speak_response(f"Sorry, I encountered an error: {str(e)}")
        
        time.sleep(2)
    
    speak_response("Voice command demonstration completed!")

def interactive_voice_session():
    """Interactive voice session"""
    print("\n🎙️  Interactive Voice Session")
    print("=" * 40)
    
    shadow = ShadowAI()
    shadow.voice_mode = True
    
    speak_response("Starting interactive voice session. Say 'quit' to exit.")
    
    while True:
        try:
            command = get_voice_input("What would you like me to do?")
            
            if not command:
                speak_response("I didn't hear anything. Please try again.")
                continue
            
            if command.lower() in ['quit', 'exit', 'goodbye', 'stop']:
                speak_response("Goodbye! It was nice talking with you.")
                break
            
            print(f"🎙️  Voice command: {command}")
            
            # Process the command
            shadow.run_single_command(command)
            
        except KeyboardInterrupt:
            speak_response("Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            speak_response("Sorry, I encountered an error. Please try again.")

def voice_document_creation():
    """Voice-based document creation"""
    print("\n📝 Voice Document Creation")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    speak_response("Let's create a document using voice commands.")
    
    # Get document type
    speak_response("What type of document would you like to create?")
    print("Options: leave letter, resume, email, report")
    
    doc_type = get_voice_input("Document type")
    
    if doc_type and 'leave' in doc_type.lower():
        speak_response("Creating a leave letter for you.")
        shadow.run_single_command("write a leave letter for tomorrow due to personal reasons")
        speak_response("Leave letter created successfully!")
    
    elif doc_type and 'resume' in doc_type.lower():
        speak_response("Creating a resume template for you.")
        shadow.run_single_command("create a resume template")
        speak_response("Resume template created successfully!")
    
    else:
        speak_response("I'll create a general document for you.")
        shadow.run_single_command("create a new document")
        speak_response("Document created successfully!")

def voice_web_search():
    """Voice-based web search"""
    print("\n🔍 Voice Web Search")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    speak_response("Let's search the web using voice commands.")
    
    # Get search query
    query = get_voice_input("What would you like to search for?")
    
    if query:
        speak_response(f"Searching for {query} on Google.")
        shadow.run_single_command(f"search for {query} on google")
        speak_response("Search completed! Check your browser for results.")
    else:
        speak_response("I didn't catch that. Please try again.")

def main():
    """Main function"""
    print("🎤 Shadow AI Voice Commands Demo")
    print("=" * 50)
    
    print("\nThis demo shows how to use Shadow AI with voice commands.")
    print("Make sure your microphone is working and permissions are granted.")
    print("\nAvailable demos:")
    print("1. Voice Interaction Demo")
    print("2. Interactive Voice Session")
    print("3. Voice Document Creation")
    print("4. Voice Web Search")
    print("5. Run All Demos")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            voice_interaction_demo()
        elif choice == '2':
            interactive_voice_session()
        elif choice == '3':
            voice_document_creation()
        elif choice == '4':
            voice_web_search()
        elif choice == '5':
            voice_interaction_demo()
            time.sleep(3)
            voice_document_creation()
            time.sleep(3)
            voice_web_search()
        else:
            print("Invalid choice. Running voice interaction demo...")
            voice_interaction_demo()
        
        print("\n🎉 Voice commands demo completed!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your microphone settings and try again.")

if __name__ == "__main__":
    main()
