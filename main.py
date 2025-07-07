# main.py
import logging
import sys
import os
import argparse
import time
import pyautogui
from typing import Dict, Any
from datetime import datetime

# Import all modules
from utils.logging import setup_logging
from utils.confirm import confirm_action, confirm_sensitive_action
from brain.gpt_agent import process_command
from control.desktop import desktop_controller
from control.browser import get_browser_controller, close_browser
from control.documents import document_controller
from input.text_input import get_text_input, show_message
from input.voice_input import get_voice_input, speak_response
from config import VOICE_ENABLED, REQUIRE_CONFIRMATION

class ShadowAI:
    def __init__(self):
        self.running = False
        self.voice_mode = False
        self.setup()
    
    def setup(self):
        """Initialize Shadow AI"""
        setup_logging()
        logging.info("🧠 Shadow AI Agent starting up...")
        
        # Welcome message
        welcome_msg = """
        ┌─────────────────────────────────────────────────────────────┐
        │                    🧠 Shadow AI Agent                       │
        │                Your Personal AI Assistant                   │
        │                                                             │
        │  Available commands:                                        │
        │  • Voice: Say your command naturally                       │
        │  • Text: Type your command                                  │
        │  • Examples:                                                │
        │    - "Open notepad and type hello world"                   │
        │    - "Write a leave letter for tomorrow"                   │
        │    - "Search for iPhone on Flipkart"                       │
        │    - "Take a screenshot"                                    │
        │                                                             │
        │  Commands: help, quit, voice, text, demo                   │
        └─────────────────────────────────────────────────────────────┘
        """
        print(welcome_msg)
        speak_response("Shadow AI is ready. How can I help you today?")
    
    def run_interactive(self):
        """Run Shadow AI in interactive mode"""
        self.running = True
        
        while self.running:
            try:
                # Get user input
                if self.voice_mode and VOICE_ENABLED:
                    command = get_voice_input("What would you like me to do?")
                else:
                    command = get_text_input("🤖 What would you like me to do? (type 'help' for commands)")
                
                if not command:
                    continue
                
                # Process built-in commands
                if self.handle_builtin_commands(command):
                    continue
                
                # Process AI command
                self.process_ai_command(command)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logging.error(f"Error in interactive mode: {e}")
                print(f"❌ Error: {e}")
    
    def handle_builtin_commands(self, command: str) -> bool:
        """Handle built-in commands"""
        command_lower = command.lower().strip()
        
        if command_lower in ['quit', 'exit', 'bye', 'goodbye']:
            self.running = False
            speak_response("Goodbye! Have a great day!")
            return True
        
        elif command_lower == 'help':
            self.show_help()
            return True
        
        elif command_lower == 'voice':
            self.voice_mode = True
            speak_response("Voice mode enabled. I'm listening for your commands.")
            print("🎤 Voice mode enabled")
            return True
        
        elif command_lower == 'text':
            self.voice_mode = False
            speak_response("Text mode enabled. Please type your commands.")
            print("⌨️ Text mode enabled")
            return True
        
        elif command_lower == 'demo':
            self.run_demo()
            return True
        
        elif command_lower == 'status':
            self.show_status()
            return True
        
        return False
    
    def show_help(self):
        """Show help information"""
        help_text = """
        🧠 Shadow AI Agent - Help
        
        BASIC COMMANDS:
        • help - Show this help message
        • quit/exit - Exit the program
        • voice - Switch to voice input mode
        • text - Switch to text input mode
        • demo - Run a demonstration
        • status - Show current status
        
        EXAMPLE TASKS:
        • "Open notepad" - Opens Notepad application
        • "Type: Hello World" - Types the specified text
        • "Write a leave letter" - Generates and creates a leave letter
        • "Search for iPhone on Flipkart" - Opens Flipkart and searches
        • "Take a screenshot" - Captures screen and saves to desktop
        • "Open calculator" - Opens Calculator app
        • "Create a resume template" - Generates a resume template
        
        DOCUMENT TASKS:
        • "Write a document about [topic]"
        • "Create a leave letter for [date] due to [reason]"
        • "Generate a resume template"
        • "Save this as PDF"
        
        BROWSER TASKS:
        • "Search for [product] on [website]"
        • "Open [website]"
        • "Buy [product] on Flipkart"
        • "Open Gmail"
        
        DESKTOP TASKS:
        • "Open [application]"
        • "Click at [x], [y]"
        • "Type [text]"
        • "Press [key]"
        • "Take screenshot"
        """
        print(help_text)
        speak_response("Help information displayed. Is there anything specific you'd like to know?")
    
    def show_status(self):
        """Show current status"""
        status = f"""
        🧠 Shadow AI Agent Status:
        
        • Mode: {'Voice' if self.voice_mode else 'Text'}
        • Voice Enabled: {'Yes' if VOICE_ENABLED else 'No'}
        • Confirmation Required: {'Yes' if REQUIRE_CONFIRMATION else 'No'}
        • Running: {'Yes' if self.running else 'No'}
        """
        print(status)
        speak_response(f"Currently in {'voice' if self.voice_mode else 'text'} mode and ready to help.")
    
    def run_demo(self):
        """Run a demonstration of capabilities"""
        speak_response("Let me demonstrate some of my capabilities.")
        
        demo_tasks = [
            "I'll open Notepad for you",
            "Now I'll type a welcome message",
            "And I'll take a screenshot to show what we accomplished"
        ]
        
        try:
            # Demo 1: Open Notepad
            speak_response(demo_tasks[0])
            desktop_controller.open_notepad()
            time.sleep(2)
            
            # Demo 2: Type text
            speak_response(demo_tasks[1])
            demo_text = "Hello! This is Shadow AI demonstrating my capabilities.\n\nI can:\n- Open applications\n- Type text\n- Control your desktop\n- Create documents\n- Browse the web\n- And much more!"
            desktop_controller.type_text(demo_text)
            time.sleep(2)
            
            # Demo 3: Take screenshot
            speak_response(demo_tasks[2])
            screenshot_path = desktop_controller.take_screenshot("shadow_demo.png")
            
            if screenshot_path:
                speak_response("Demo completed! I've opened Notepad, typed a message, and saved a screenshot to your desktop.")
            else:
                speak_response("Demo completed! I've opened Notepad and typed a message.")
            
        except Exception as e:
            logging.error(f"Error in demo: {e}")
            speak_response("I encountered an error during the demonstration, but I'm still ready to help with your tasks.")
    
    def process_ai_command(self, command: str):
        """Process AI command using GPT agent"""
        try:
            logging.info(f"Processing AI command: {command}")
            
            # Get action data from GPT agent
            action_data = process_command(command)
            
            if not action_data:
                speak_response("I couldn't understand that command. Please try again.")
                return
            
            # Execute the action
            success = self.execute_action(action_data)
            
            if success:
                response = f"✅ Task completed: {action_data.get('description', 'Unknown task')}"
                logging.info(response)
                print(response)
                speak_response("Task completed successfully!")
            else:
                response = f"❌ Task failed: {action_data.get('description', 'Unknown task')}"
                logging.error(response)
                print(response)
                speak_response("I encountered an error while performing that task.")
        
        except Exception as e:
            logging.error(f"Error processing AI command: {e}")
            speak_response("I encountered an error while processing your command.")
    
    def execute_action(self, action_data: Dict[str, Any]) -> bool:
        """Execute the action based on action data"""
        try:
            task_type = action_data.get('task_type')
            action = action_data.get('action')
            parameters = action_data.get('parameters', {})
            confirmation_required = action_data.get('confirmation_required', False)
            description = action_data.get('description', 'Unknown action')
            
            # Check for confirmation if required
            if confirmation_required:
                if not confirm_action(description):
                    speak_response("Action cancelled by user.")
                    return False
            
            # Execute based on task type
            if task_type == 'desktop_control':
                return self.execute_desktop_action(action, parameters)
            elif task_type == 'document_creation':
                return self.execute_document_action(action, parameters)
            elif task_type == 'web_automation':
                return self.execute_web_action(action, parameters)
            elif task_type == 'file_operation':
                return self.execute_file_action(action, parameters)
            else:
                logging.warning(f"Unknown task type: {task_type}")
                return False
        
        except Exception as e:
            logging.error(f"Error executing action: {e}")
            return False
    
    def execute_desktop_action(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Execute desktop control actions"""
        try:
            if action == 'open_notepad':
                return desktop_controller.open_notepad()
            elif action == 'open_notepad_and_type':
                # Open notepad (or activate if already open) and type text
                success = desktop_controller.open_or_activate_notepad()
                if success:
                    time.sleep(1.5)  # Wait for notepad to be ready
                    text = parameters.get('text', '')
                    return desktop_controller.type_text(text)
                return False
            elif action == 'write_article_to_active_window':
                # Write article to the currently active window
                topic = parameters.get('topic', 'AI')
                article_content = self.generate_article_content(topic)
                return desktop_controller.type_text(article_content)
            elif action == 'type_text':
                text = parameters.get('text', '')
                return desktop_controller.type_text(text)
            elif action == 'click_at':
                x = parameters.get('x', 0)
                y = parameters.get('y', 0)
                return desktop_controller.click_at(x, y)
            elif action == 'take_screenshot':
                filename = parameters.get('filename')
                result = desktop_controller.take_screenshot(filename)
                return result is not None
            elif action == 'open_application':
                app_name = parameters.get('app_name', '')
                return desktop_controller.open_application(app_name)
            elif action == 'press_key':
                key = parameters.get('key', '')
                return desktop_controller.press_key(key)
            elif action == 'append_text':
                # Move to end of document and add text
                pyautogui.keyDown('ctrl')
                pyautogui.press('end')
                pyautogui.keyUp('ctrl')
                time.sleep(0.5)
                text = parameters.get('text', '')
                return desktop_controller.type_text(text)
            else:
                logging.warning(f"Unknown desktop action: {action}")
                return False
        except Exception as e:
            logging.error(f"Error in desktop action: {e}")
            return False
    
    def execute_document_action(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Execute document creation actions"""
        try:
            if action == 'create_document':
                content = parameters.get('content', '')
                filename = parameters.get('filename', 'Document')
                format = parameters.get('format', 'docx')
                result = document_controller.create_document(content, filename, format)
                return result is not None
            elif action == 'create_article':
                topic = parameters.get('topic', 'AI')
                format = parameters.get('format', 'docx')
                open_in_notepad = parameters.get('open_in_notepad', False)
                
                # Generate article content
                article_content = self.generate_article_content(topic)
                
                if open_in_notepad:
                    # Use existing notepad window or open new one
                    success = desktop_controller.open_or_activate_notepad()
                    if success:
                        time.sleep(1.5)  # Wait for notepad to be ready
                        # Clear existing content and add new content
                        desktop_controller.select_all()
                        time.sleep(0.5)
                        return desktop_controller.type_text(article_content)
                    return False
                else:
                    # Create document file
                    filename = f"Article_about_{topic.replace(' ', '_')}"
                    result = document_controller.create_document(article_content, filename, format)
                    return result is not None
            elif action == 'create_leave_letter':
                reason = parameters.get('reason', 'health reasons')
                date = parameters.get('date')
                result = document_controller.generate_leave_letter(reason, date)
                return result is not None
            elif action == 'create_resume':
                name = parameters.get('name', '[Your Name]')
                result = document_controller.generate_resume_template(name)
                return result is not None
            elif action == 'open_word':
                filepath = parameters.get('filepath')
                return document_controller.open_word(filepath)
            else:
                logging.warning(f"Unknown document action: {action}")
                return False
        except Exception as e:
            logging.error(f"Error in document action: {e}")
            return False
    
    def execute_web_action(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Execute web automation actions"""
        try:
            browser = get_browser_controller()
            
            if action == 'open_browser':
                url = parameters.get('url')
                return browser.navigate_to(url) if url else True
            elif action == 'search_product':
                site = parameters.get('site', 'google')
                product = parameters.get('product', '')
                if site.lower() == 'flipkart':
                    return browser.search_flipkart(product)
                else:
                    return browser.search_google(product)
            elif action == 'navigate_to':
                url = parameters.get('url', '')
                return browser.navigate_to(url)
            elif action == 'take_screenshot':
                filename = parameters.get('filename')
                result = browser.take_screenshot(filename)
                return result is not None
            else:
                logging.warning(f"Unknown web action: {action}")
                return False
        except Exception as e:
            logging.error(f"Error in web action: {e}")
            return False
    
    def execute_file_action(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Execute file operation actions"""
        try:
            # Basic file operations
            if action == 'save_file':
                filepath = parameters.get('filepath', '')
                content = parameters.get('content', '')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            else:
                logging.warning(f"Unknown file action: {action}")
                return False
        except Exception as e:
            logging.error(f"Error in file action: {e}")
            return False
    
    def run_single_command(self, command: str) -> bool:
        """Run a single command (for CLI usage)"""
        try:
            logging.info(f"Running single command: {command}")
            self.process_ai_command(command)
            return True
        except Exception as e:
            logging.error(f"Error running single command: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            close_browser()
            logging.info("Shadow AI cleanup completed")
        except Exception as e:
            logging.error(f"Error in cleanup: {e}")
    
    def generate_article_content(self, topic: str) -> str:
        """Generate article content about a given topic"""
        article_template = f"""# Article: {topic.title()}

## Introduction

{topic.title()} is a fascinating subject that has gained significant attention in recent years. This article explores the key aspects and implications of {topic}.

## Main Content

### What is {topic.title()}?

{topic.title()} refers to the concept and applications related to {topic}. It encompasses various techniques, methodologies, and practices that have evolved over time.

### Key Features

1. **Innovation**: {topic.title()} represents cutting-edge developments in its field
2. **Impact**: It has significant implications for various industries and sectors
3. **Future Potential**: The possibilities for future development are extensive

### Applications

{topic.title()} has numerous applications across different domains:

- Technology and computing
- Business and industry
- Research and development
- Education and training

### Benefits

The adoption of {topic} brings several benefits:

- Improved efficiency and productivity
- Enhanced decision-making capabilities
- Better resource utilization
- Increased innovation potential

### Challenges

Despite its advantages, {topic} also presents certain challenges:

- Technical complexity
- Implementation costs
- Skill requirements
- Ethical considerations

## Conclusion

{topic.title()} continues to evolve and shape our world. Understanding its principles and applications is crucial for staying competitive in today's rapidly changing landscape.

As we move forward, it will be important to address the challenges while maximizing the benefits that {topic} can provide.

## References

- Industry reports and research papers
- Expert opinions and case studies
- Real-world applications and examples

---
Generated by Shadow AI Agent
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        return article_template

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Shadow AI - Your Personal AI Assistant')
    parser.add_argument('command', nargs='*', help='Command to execute')
    parser.add_argument('--voice', action='store_true', help='Enable voice mode')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Create Shadow AI instance
    shadow = ShadowAI()
    
    try:
        if args.demo:
            shadow.run_demo()
        elif args.command:
            # Single command mode
            command = ' '.join(args.command)
            shadow.run_single_command(command)
        else:
            # Interactive mode
            if args.voice:
                shadow.voice_mode = True
            shadow.run_interactive()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logging.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")
    finally:
        shadow.cleanup()

if __name__ == "__main__":
    main()

