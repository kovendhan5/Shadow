# main.py
import logging
import sys
import os
import argparse
import time
import traceback
from typing import Dict, Any
from datetime import datetime

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add colorama for a better CLI experience
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class DummyColor:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    Fore = Style = DummyColor()

# Enhanced error handling for imports
def safe_import_with_fallback(module_name, fallback_value=None, required=False):
    """Safely import modules with fallback handling"""
    try:
        return __import__(module_name)
    except ImportError as e:
        if required:
            print(f"❌ Required module '{module_name}' not found: {e}")
            print("   Please run: pip install -r requirements.txt")
            sys.exit(1)
        else:
            if fallback_value is not None:
                print(f"⚠️  Module '{module_name}' not available, using fallback")
                return fallback_value
            else:
                print(f"⚠️  Module '{module_name}' not available, some features may be limited")
                return None

# Try to import pyautogui with fallback
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    # Configure pyautogui if available
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
except ImportError:
    print("⚠️  pyautogui not available - desktop automation will be limited")
    PYAUTOGUI_AVAILABLE = False
    # Create a mock pyautogui for basic functionality
    class MockPyAutoGUI:
        @staticmethod
        def typewrite(text, interval=0.1):
            print(f"[MOCK] Would type: {text[:50]}...")
        @staticmethod
        def click(x, y):
            print(f"[MOCK] Would click at ({x}, {y})")
        @staticmethod
        def screenshot():
            print("[MOCK] Would take screenshot")
            return None
        @staticmethod
        def hotkey(*keys):
            print(f"[MOCK] Would press: {' + '.join(keys)}")
        @staticmethod
        def press(key):
            print(f"[MOCK] Would press: {key}")
    pyautogui = MockPyAutoGUI()

# Ensure .env is loaded for API keys
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("[Warning] python-dotenv not installed. .env loading skipped.")

# Force Orpheus TTS and torch to use CPU if no GPU is present
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Try to load robust handler
try:
    from utils.robust_handler import get_robust_shadow, check_and_report_dependencies
    ROBUST_HANDLER_AVAILABLE = True
except ImportError:
    print("⚠️  Robust handler not available, using basic functionality")
    ROBUST_HANDLER_AVAILABLE = False

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
from utils.rag import search_knowledge_base
from automation.whatsapp_automation import WhatsAppAutomator
from utils.orpheus_tts import speak as orpheus_speak

# Import new enhanced modules
try:
    from control.file_manager import file_manager
    FILE_MANAGER_AVAILABLE = True
except ImportError:
    FILE_MANAGER_AVAILABLE = False

try:
    from control.web_search import web_search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    from control.system_info import system_diagnostics
    SYSTEM_INFO_AVAILABLE = True
except ImportError:
    SYSTEM_INFO_AVAILABLE = False

try:
    from control.notifications import notification_manager, notify_success, notify_error, notify_info
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

try:
    from control.clipboard_manager import clipboard_manager, copy_text, paste_text
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    from control.hotkey_manager import hotkey_manager, start_hotkeys
    HOTKEYS_AVAILABLE = True
except ImportError:
    HOTKEYS_AVAILABLE = False

class ShadowAI:
    def __init__(self):
        self.running = False
        self.voice_mode = False
        self.plugin_commands = []  # List of plugin command handlers
        self.load_plugins()
        self.setup()
    
    def load_plugins(self):
        """Auto-discover and load plugins from the plugins/ directory."""
        plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        if not os.path.isdir(plugins_dir):
            return
        for fname in os.listdir(plugins_dir):
            if fname.endswith('.py') and not fname.startswith('_'):
                try:
                    plugin_path = os.path.join(plugins_dir, fname)
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(fname[:-3], plugin_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, 'register'):
                        mod.register(self)
                        print(f"✅ Loaded plugin: {fname}")
                except Exception as e:
                    print(f"❌ Failed to load plugin {fname}: {e}")
    
    def print_banner(self):
        """Print enhanced startup banner"""
        if COLORAMA_AVAILABLE:
            print(f"\n{Fore.CYAN}{'='*77}")
            print(f"{Fore.MAGENTA}   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗  {Fore.CYAN}██╗ █████╗ ██╗")
            print(f"{Fore.MAGENTA}   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║  {Fore.CYAN}██║██╔══██╗██║")
            print(f"{Fore.MAGENTA}   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║  {Fore.CYAN}██║███████║██║")
            print(f"{Fore.MAGENTA}   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║  {Fore.CYAN}██║██╔══██║╚═╝")
            print(f"{Fore.MAGENTA}   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝  {Fore.CYAN}██║██║  ██║██╗")
            print(f"{Fore.MAGENTA}   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝  {Fore.CYAN}╚═╝╚═╝  ╚═╝╚═╝")
            print(f"{Fore.CYAN}{'='*77}")
            print(f"{Fore.YELLOW}                  Universal Personal Assistant")
            print(f"{Fore.GREEN}                         Version 3.0 - Universal")
            print(f"{Fore.CYAN}{'='*77}\n")
        else:
            print("\n" + "="*60)
            print("          SHADOW AI - UNIVERSAL ASSISTANT")
            print("="*60 + "\n")
    def setup(self):
        """Initialize Shadow AI"""
        setup_logging()
        logging.info("🧠 Shadow AI Agent starting up...")
        
        # Initialize enhanced modules
        self.init_enhanced_features()
        
        # Welcome message
        welcome_msg = """
        ┌─────────────────────────────────────────────────────────────┐
        │              🧠 Shadow AI Universal Assistant                │
        │           Your Intelligent Computer Companion               │
        │                                                             │
        │  🌟 NEW: Enhanced Features & Capabilities                   │
        │  I can now understand and execute ANY computer task!        │
        │                                                             │
        │  🚀 NEW FEATURES:                                           │
        │  • Advanced File Management & Organization                  │
        │  • Quick Web Search & Information Retrieval                │
        │  • System Diagnostics & Monitoring                         │
        │  • Desktop Notifications & Alerts                          │
        │  • Clipboard Management & History                          │
        │  • Customizable Hotkeys & Shortcuts                        │
        │                                                             │
        │  Examples of what I can do:                                 │
        │  • "Write an article about artificial intelligence"         │
        │  • "Organize my Downloads folder by file type"             │
        │  • "Search Google for Python tutorials"                    │
        │  • "Show system information and performance"               │
        │  • "Copy this text to clipboard and save history"          │
        │  • "Take a screenshot with Ctrl+Shift+S"                   │
        │  • "Find and delete large files over 100MB"                │
        │  • "Create a backup of my Documents folder"                │
        │                                                             │
        │  🎯 I understand context and can execute complex workflows  │
        │  🔐 I prioritize security and ask for confirmation          │
        │  🧠 I learn from your preferences and improve over time     │
        │                                                             │
        │  Commands: help, quit, voice, text, demo, status, features │
        └─────────────────────────────────────────────────────────────┘
        """
        print(welcome_msg)
        speak_response("Shadow AI Universal Assistant with enhanced features is ready. I can help you with any computer task. What would you like me to do?")
    
    def init_enhanced_features(self):
        """Initialize enhanced features"""
        try:
            # Start notifications
            if NOTIFICATIONS_AVAILABLE:
                notify_success("Shadow AI Enhanced Features Loaded")
            
            # Start hotkeys if available
            if HOTKEYS_AVAILABLE:
                hotkey_manager.start_listening()
                logging.info("Hotkey system activated")
            
            # Initialize file manager
            if FILE_MANAGER_AVAILABLE:
                logging.info("File management system ready")
            
            # Initialize web search
            if WEB_SEARCH_AVAILABLE:
                logging.info("Web search system ready")
            
            # Initialize system diagnostics
            if SYSTEM_INFO_AVAILABLE:
                logging.info("System diagnostics ready")
            
            # Initialize clipboard manager
            if CLIPBOARD_AVAILABLE:
                logging.info("Clipboard management ready")
            
        except Exception as e:
            logging.error(f"Error initializing enhanced features: {e}")
    
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
                
                # Process enhanced commands first
                if self.handle_enhanced_commands(command):
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
        """Handle built-in commands and plugin commands"""
        command_lower = command.lower().strip()
        # Built-in commands
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
        elif command_lower == 'features':
            self.show_enhanced_features()
            return True
        # Plugin commands
        for handler in self.plugin_commands:
            try:
                if handler(command):
                    return True
            except Exception as e:
                print(f"❌ Plugin command error: {e}")
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
    
    def process_command(self, command: str):
        """Public interface for command processing (for API/test compatibility)"""
        return self.process_ai_command(command)
    
    def process_ai_command(self, command: str):
        """Process AI command using Universal Processor and Executor, with RAG support"""
        try:
            logging.info(f"Processing universal command: {command}")
            # RAG: Search knowledge base for relevant info
            kb_results = search_knowledge_base(command)
            if kb_results:
                print("📚 Found relevant info in knowledge base:")
                for line in kb_results:
                    print(f"  • {line}")
            # Use Universal Processor to understand the command
            task = process_universal_command(command)
            if not task:
                speak_response("I couldn't understand that command. Please try again.")
                return {
                    "success": False,
                    "message": "Could not understand command",
                    "error": "Command parsing failed"
                }
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
                
                return {
                    "success": True,
                    "message": response,
                    "task_result": result,
                    "execution_time": result.execution_time,
                    "warnings": result.warnings
                }
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
                
                return {
                    "success": False,
                    "message": response,
                    "task_result": result,
                    "error": result.error_message
                }
        
        except Exception as e:
            logging.error(f"Error processing universal command: {e}")
            logging.error(traceback.format_exc())
            speak_response("I encountered an error while processing your command.")
            return {
                "success": False,
                "message": f"Error processing command: {str(e)}",
                "error": str(e)
            }
    
    def handle_enhanced_commands(self, command: str) -> bool:
        """Handle enhanced feature commands"""
        try:
            command_lower = command.lower().strip()
            
            # File management commands
            if FILE_MANAGER_AVAILABLE:
                if "organize" in command_lower and "folder" in command_lower:
                    return self.handle_file_organization(command)
                elif "find large files" in command_lower:
                    return self.handle_find_large_files(command)
                elif "backup" in command_lower:
                    return self.handle_backup_command(command)
                elif "clean temp files" in command_lower:
                    return self.handle_clean_temp(command)
            
            # Web search commands
            if WEB_SEARCH_AVAILABLE:
                if command_lower.startswith("search ") or "google" in command_lower:
                    return self.handle_web_search(command)
                elif "search news" in command_lower:
                    return self.handle_news_search(command)
                elif "search tutorial" in command_lower:
                    return self.handle_tutorial_search(command)
            
            # System info commands
            if SYSTEM_INFO_AVAILABLE:
                if "system info" in command_lower or "system status" in command_lower:
                    return self.handle_system_info(command)
                elif "system health" in command_lower:
                    return self.handle_system_health(command)
                elif "running processes" in command_lower:
                    return self.handle_process_list(command)
            
            # Clipboard commands
            if CLIPBOARD_AVAILABLE:
                if "copy to clipboard" in command_lower:
                    return self.handle_clipboard_copy(command)
                elif "paste from clipboard" in command_lower:
                    return self.handle_clipboard_paste(command)
                elif "clipboard history" in command_lower:
                    return self.handle_clipboard_history(command)
            
            # Notification commands
            if NOTIFICATIONS_AVAILABLE:
                if "notify" in command_lower or "notification" in command_lower:
                    return self.handle_notification_command(command)
            
            # Hotkey commands
            if HOTKEYS_AVAILABLE:
                if "hotkey" in command_lower or "shortcut" in command_lower:
                    return self.handle_hotkey_command(command)
            
            return False
            
        except Exception as e:
            logging.error(f"Error handling enhanced commands: {e}")
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
    
    def show_enhanced_features(self):
        """Show enhanced features status"""
        features_status = f"""
        🚀 Shadow AI Enhanced Features Status:
        
        📁 File Management: {'✅ Available' if FILE_MANAGER_AVAILABLE else '❌ Not Available'}
        🌐 Web Search: {'✅ Available' if WEB_SEARCH_AVAILABLE else '❌ Not Available'}
        💻 System Info: {'✅ Available' if SYSTEM_INFO_AVAILABLE else '❌ Not Available'}
        🔔 Notifications: {'✅ Available' if NOTIFICATIONS_AVAILABLE else '❌ Not Available'}
        📋 Clipboard: {'✅ Available' if CLIPBOARD_AVAILABLE else '❌ Not Available'}
        🔥 Hotkeys: {'✅ Available' if HOTKEYS_AVAILABLE else '❌ Not Available'}
        
        🎯 Enhanced Commands Available:
        • "organize Downloads folder by type"
        • "search Google for Python tutorials"
        • "show system information"
        • "copy this text to clipboard"
        • "find large files over 100MB"
        • "create backup of Documents"
        • "show hotkey help"
        """
        print(features_status)
        speak_response("Enhanced features status displayed. All advanced capabilities are ready to use.")
    
    # Enhanced Command Handlers
    def handle_file_organization(self, command: str) -> bool:
        """Handle file organization commands"""
        try:
            if "downloads" in command.lower():
                folder_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            elif "documents" in command.lower():
                folder_path = os.path.join(os.path.expanduser('~'), 'Documents')
            elif "desktop" in command.lower():
                folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:
                # Extract folder path from command
                words = command.split()
                folder_path = None
                for i, word in enumerate(words):
                    if word.lower() == "organize" and i + 1 < len(words):
                        folder_path = words[i + 1]
                        break
                
                if not folder_path:
                    speak_response("Please specify which folder to organize")
                    return True
            
            if folder_path and os.path.exists(folder_path):
                result = file_manager.organize_by_type(folder_path)
                if result:
                    message = f"Organized {sum(result.values())} files into {len(result)} categories"
                    speak_response(message)
                    if NOTIFICATIONS_AVAILABLE:
                        notify_success(message)
                else:
                    speak_response("Failed to organize folder")
                return True
            else:
                speak_response(f"Folder not found: {folder_path}")
                return True
                
        except Exception as e:
            logging.error(f"Error in file organization: {e}")
            speak_response("Error organizing files")
            return True
    
    def handle_find_large_files(self, command: str) -> bool:
        """Handle finding large files"""
        try:
            # Extract size from command
            import re
            size_match = re.search(r'(\d+)\s*mb', command.lower())
            min_size = int(size_match.group(1)) if size_match else 100
            
            # Extract path from command or use default
            folder_path = os.path.expanduser('~')
            
            large_files = file_manager.find_large_files(folder_path, min_size)
            
            if large_files:
                message = f"Found {len(large_files)} files larger than {min_size}MB"
                speak_response(message)
                
                # Show first few files
                for file_path, size_mb in large_files[:5]:
                    print(f"📁 {size_mb}MB: {file_path}")
                
                if NOTIFICATIONS_AVAILABLE:
                    notify_info(f"Found {len(large_files)} large files")
            else:
                speak_response(f"No files larger than {min_size}MB found")
            
            return True
            
        except Exception as e:
            logging.error(f"Error finding large files: {e}")
            speak_response("Error finding large files")
            return True
    
    def handle_backup_command(self, command: str) -> bool:
        """Handle backup commands"""
        try:
            # Extract source from command
            if "documents" in command.lower():
                source_path = os.path.join(os.path.expanduser('~'), 'Documents')
            elif "desktop" in command.lower():
                source_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            elif "pictures" in command.lower():
                source_path = os.path.join(os.path.expanduser('~'), 'Pictures')
            else:
                speak_response("Please specify what to backup (documents, desktop, pictures)")
                return True
            
            result = file_manager.create_backup(source_path)
            
            if result:
                message = f"Backup created successfully"
                speak_response(message)
                if NOTIFICATIONS_AVAILABLE:
                    notify_success(message)
            else:
                speak_response("Failed to create backup")
            
            return True
            
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            speak_response("Error creating backup")
            return True
    
    def handle_web_search(self, command: str) -> bool:
        """Handle web search commands"""
        try:
            # Extract search query
            command_lower = command.lower()
            
            if command_lower.startswith("search "):
                query = command[7:].strip()
            elif "google" in command_lower:
                # Extract query after "google" or "google for"
                parts = command_lower.split("google")
                if len(parts) > 1:
                    query = parts[1].replace("for", "").strip()
                else:
                    query = ""
            else:
                query = command.strip()
            
            if query:
                result = web_search.search_web(query)
                if result:
                    message = f"Web search opened for: {query}"
                    speak_response(message)
                    if NOTIFICATIONS_AVAILABLE:
                        notify_success(message)
                else:
                    speak_response("Failed to open web search")
            else:
                speak_response("Please specify what to search for")
            
            return True
            
        except Exception as e:
            logging.error(f"Error in web search: {e}")
            speak_response("Error performing web search")
            return True
    
    def handle_system_info(self, command: str) -> bool:
        """Handle system information commands"""
        try:
            if "report" in command.lower():
                # Generate full system report
                report = system_diagnostics.generate_system_report()
                print(report)
                
                # Save report to file
                report_file = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                message = f"System report generated and saved to {report_file}"
                speak_response(message)
                
                if NOTIFICATIONS_AVAILABLE:
                    notify_success(message)
            else:
                # Show basic system info
                cpu_info = system_diagnostics.get_cpu_info()
                mem_info = system_diagnostics.get_memory_info()
                
                info_text = f"""
                💻 System Information:
                CPU Usage: {cpu_info.get('cpu_percent_total', 'N/A')}%
                Memory Usage: {mem_info.get('percentage', 'N/A')}% ({mem_info.get('used_gb', 'N/A')}/{mem_info.get('total_gb', 'N/A')} GB)
                System Uptime: {system_diagnostics.get_system_uptime()}
                """
                print(info_text)
                speak_response("System information displayed")
                
                if NOTIFICATIONS_AVAILABLE:
                    notify_info(f"CPU: {cpu_info.get('cpu_percent_total', 'N/A')}%, Memory: {mem_info.get('percentage', 'N/A')}%")
            
            return True
            
        except Exception as e:
            logging.error(f"Error getting system info: {e}")
            speak_response("Error getting system information")
            return True
    
    def handle_clipboard_copy(self, command: str) -> bool:
        """Handle clipboard copy commands"""
        try:
            # Extract text to copy
            if "copy to clipboard" in command.lower():
                text = command.lower().replace("copy to clipboard", "").strip()
                text = command[command.lower().find("copy to clipboard") + len("copy to clipboard"):].strip()
            else:
                text = command.strip()
            
            if text:
                result = clipboard_manager.copy_to_clipboard(text)
                if result:
                    message = f"Copied to clipboard: {text[:30]}..."
                    speak_response(message)
                    if NOTIFICATIONS_AVAILABLE:
                        notify_success("Text copied to clipboard")
                else:
                    speak_response("Failed to copy to clipboard")
            else:
                speak_response("Please specify text to copy")
            
            return True
            
        except Exception as e:
            logging.error(f"Error copying to clipboard: {e}")
            speak_response("Error copying to clipboard")
            return True
    
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

    def send_whatsapp_message(self, contact, message):
        """Send a WhatsApp message to a contact using UI automation"""
        automator = WhatsAppAutomator()
        result = automator.send_message(contact, message)
        if result:
            orpheus_speak(f"Message sent to {contact} successfully.")
        else:
            orpheus_speak(f"Failed to send message to {contact}.")
        return result

    def run_conversation_mode(self):
        """Continuous conversation mode with real-time TTS and task execution"""
        self.running = True
        orpheus_speak("Conversation mode enabled. I am listening.")
        while self.running:
            try:
                command = get_voice_input("How can I help you?")
                if not command:
                    continue
                if self.handle_builtin_commands(command):
                    continue
                # WhatsApp message intent (simple example)
                if command.lower().startswith("send whatsapp message to"):
                    try:
                        parts = command.split("to",1)[1].strip().split(" ",1)
                        contact = parts[0]
                        message = parts[1] if len(parts)>1 else "Hello!"
                        self.send_whatsapp_message(contact, message)
                        continue
                    except Exception:
                        orpheus_speak("Sorry, I could not parse the WhatsApp command.")
                        continue
                # Fallback: normal AI command
                result = self.process_ai_command(command)
                if result and result.get("message"):
                    orpheus_speak(result["message"])
            except KeyboardInterrupt:
                orpheus_speak("Goodbye!")
                break
            except Exception as e:
                orpheus_speak(f"Error: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Shadow AI - Your Personal AI Assistant')
    parser.add_argument('command', nargs='*', help='Command to execute')
    parser.add_argument('--voice', action='store_true', help='Enable voice mode')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--conversation', action='store_true', help='Run in real-time conversation mode')
    
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
