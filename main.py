# main.py
import logging
import sys
import os
import argparse
import time
import traceback
import pyautogui
from typing import Dict, Any
from datetime import datetime

# Import all modules
from utils.logging import setup_logging
from utils.confirm import confirm_action, confirm_sensitive_action
from brain.gpt_agent import process_command
from brain.universal_processor import process_universal_command
from brain.universal_executor import execute_universal_task
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
        │              🧠 Shadow AI Universal Assistant                │
        │           Your Intelligent Computer Companion               │
        │                                                             │
        │  🌟 NEW: Universal Command Processing                       │
        │  I can now understand and execute ANY computer task!        │
        │                                                             │
        │  Examples of what I can do:                                 │
        │  • "Write an article about artificial intelligence"         │
        │  • "Create a leave letter for tomorrow"                     │
        │  • "Search for iPhone on Flipkart and compare prices"       │
        │  • "Open PowerPoint and create a presentation"             │
        │  • "Find all PDF files in Downloads and organize them"      │
        │  • "Send an email to my team about the project update"      │
        │  • "Create a backup of my important documents"              │
        │  • "Set up a meeting reminder for 3 PM"                     │
        │                                                             │
        │  🎯 I understand context and can execute complex workflows  │
        │  🔐 I prioritize security and ask for confirmation          │
        │  🧠 I learn from your preferences and improve over time     │
        │                                                             │
        │  Commands: help, quit, voice, text, demo, status           │
        └─────────────────────────────────────────────────────────────┘
        """
        print(welcome_msg)
        speak_response("Shadow AI Universal Assistant is ready. I can help you with any computer task. What would you like me to do?")
    
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
        🧠 Shadow AI Universal Assistant - Help
        
        ═══════════════════════════════════════════════════════════
        BASIC COMMANDS:
        • help - Show this help message
        • quit/exit - Exit the program
        • voice - Switch to voice input mode
        • text - Switch to text input mode
        • demo - Run a demonstration
        • status - Show current status
        
        ═══════════════════════════════════════════════════════════
        🌟 UNIVERSAL CAPABILITIES:
        
        I can understand and execute ANY computer task you describe
        in natural language. Just tell me what you want to do!
        
        DOCUMENT & CONTENT CREATION:
        • "Write an article about [topic]"
        • "Create a professional email about [subject]"
        • "Draft a business proposal for [project]"
        • "Generate a resume template"
        • "Write a leave letter for [date] due to [reason]"
        • "Create meeting notes from yesterday's discussion"
        
        WEB & RESEARCH TASKS:
        • "Search for the best laptops under $1000"
        • "Find flight prices from New York to London"
        • "Research the latest news about [topic]"
        • "Compare prices for [product] on different websites"
        • "Download the latest updates for [software]"
        
        FILE & SYSTEM MANAGEMENT:
        • "Organize my Downloads folder by file type"
        • "Find all photos from last month and create a folder"
        • "Backup my Documents folder to [location]"
        • "Delete temporary files to free up space"
        • "Create a folder structure for my new project"
        
        COMMUNICATION & PRODUCTIVITY:
        • "Send an email to [contact] about [subject]"
        • "Schedule a meeting reminder for [time]"
        • "Create a to-do list for today's tasks"
        • "Set up a calendar event for [event]"
        • "Draft a message to my team about [topic]"
        
        AUTOMATION & WORKFLOWS:
        • "Create a morning routine that opens my work apps"
        • "Set up automatic file organization"
        • "Create a backup schedule for important files"
        • "Automate my daily report generation"
        
        CREATIVE & DESIGN:
        • "Create a presentation about [topic]"
        • "Design a simple logo for my business"
        • "Generate ideas for [project]"
        • "Create a social media post about [event]"
        
        ═══════════════════════════════════════════════════════════
        🎯 HOW IT WORKS:
        
        1. Tell me what you want to do in natural language
        2. I'll understand your intent and break it into steps
        3. I'll show you what I plan to do and ask for confirmation
        4. I'll execute the task step by step
        5. I'll provide feedback on the results
        
        🔐 SECURITY: I always ask for permission before:
        • Accessing sensitive information
        • Making purchases or financial transactions
        • Deleting or modifying important files
        • Sending emails or messages
        
        💡 TIP: Be as specific as possible for better results!
        Instead of "help with work", try "create a project timeline 
        in Excel for the Q1 marketing campaign"
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
        """Process AI command using Universal Processor and Executor"""
        try:
            logging.info(f"Processing universal command: {command}")
            
            # Use Universal Processor to understand the command
            task = process_universal_command(command)
            
            if not task:
                speak_response("I couldn't understand that command. Please try again.")
                return
            
            # Show task summary to user
            print(f"\n🎯 Task: {task.description}")
            print(f"📊 Complexity: {task.complexity.value}")
            print(f"⚡ Estimated time: {task.estimated_duration} seconds")
            print(f"🔒 Risk level: {task.risk_level}")
            print(f"📝 Steps: {len(task.steps)}")
            
            # Execute the task using Universal Executor
            result = execute_universal_task(task)
            
            if result.success:
                response = f"✅ Task completed successfully in {result.execution_time:.1f} seconds"
                if result.warnings:
                    response += f" (with {len(result.warnings)} warnings)"
                logging.info(response)
                print(response)
                speak_response("Task completed successfully!")
                
                # Show any warnings
                if result.warnings:
                    print("\n⚠️ Warnings:")
                    for warning in result.warnings:
                        print(f"  • {warning}")
            else:
                response = f"❌ Task failed: {result.error_message or 'Unknown error'}"
                logging.error(response)
                print(response)
                speak_response("I encountered an error while performing that task.")
                
                # Show failed steps
                if result.step_results:
                    print("\n📋 Step Results:")
                    for step_result in result.step_results:
                        status = "✅" if step_result.get("success", False) else "❌"
                        step_num = step_result.get("step_number", "?")
                        action = step_result.get("action", "unknown")
                        print(f"  {status} Step {step_num}: {action}")
                        if not step_result.get("success", False) and step_result.get("error"):
                            print(f"      Error: {step_result['error']}")
        
        except Exception as e:
            logging.error(f"Error processing universal command: {e}")
            logging.error(traceback.format_exc())
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
            elif action == 'open_notepad_and_write_article':
                # Open notepad first, then write article
                success = desktop_controller.open_notepad()
                if success:
                    time.sleep(2)  # Wait for notepad to fully open
                    topic = parameters.get('topic', 'AI')
                    article_content = self.generate_article_content(topic)
                    return desktop_controller.type_text(article_content)
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

