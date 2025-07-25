#!/usr/bin/env python3
"""
Enhanced Shadow AI Main Interface
Improved UI and command processing with article generation
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enhanced imports with fallbacks
try:
    import colorama
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Create dummy color objects
    class DummyColor:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    Fore = Back = Style = DummyColor()

# Import Shadow AI components
try:
    from control.enhanced_desktop import enhanced_controller
    ENHANCED_DESKTOP_AVAILABLE = True
except ImportError:
    try:
        from control.desktop import desktop_controller as enhanced_controller
        ENHANCED_DESKTOP_AVAILABLE = False
    except ImportError:
        enhanced_controller = None

try:
    from brain.gpt_agent import process_command
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class EnhancedShadowAI:
    """Enhanced Shadow AI with improved UI and functionality"""
    
    def __init__(self):
        self.running = True
        self.commands_processed = 0
        self.setup_logging()
        self.print_banner()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "shadow_ai.log"),
                logging.StreamHandler()
            ]
        )
        
    def print_banner(self):
        """Print enhanced startup banner"""
        if COLORAMA_AVAILABLE:
            print(f"\n{Fore.CYAN}{'='*60}")
            print(f"{Fore.MAGENTA}   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗")
            print(f"{Fore.MAGENTA}   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║")
            print(f"{Fore.MAGENTA}   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║")
            print(f"{Fore.MAGENTA}   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║")
            print(f"{Fore.MAGENTA}   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝")
            print(f"{Fore.MAGENTA}   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ")
            print(f"{Fore.CYAN}{'='*60}")
            print(f"{Fore.YELLOW}            🤖 ENHANCED AI ASSISTANT 🤖")
            print(f"{Fore.GREEN}               Version 2.0 - Enhanced")
            print(f"{Fore.CYAN}{'='*60}\n")
        else:
            print("\n" + "="*60)
            print("          SHADOW AI - ENHANCED ASSISTANT")
            print("               Version 2.0 - Enhanced")
            print("="*60 + "\n")
    
    def print_status(self):
        """Print current system status"""
        status_color = Fore.GREEN if COLORAMA_AVAILABLE else ""
        warning_color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
        error_color = Fore.RED if COLORAMA_AVAILABLE else ""
        
        print(f"\n{status_color}🔍 SYSTEM STATUS:")
        print(f"{'─'*40}")
        
        # Check AI capabilities
        if AI_AVAILABLE:
            print(f"{status_color}✅ AI Brain: Advanced AI processing available")
        else:
            print(f"{warning_color}⚠️  AI Brain: Basic mode (install openai for full features)")
        
        # Check desktop control
        if enhanced_controller:
            if ENHANCED_DESKTOP_AVAILABLE:
                print(f"{status_color}✅ Desktop Control: Enhanced with article generation")
            else:
                print(f"{status_color}✅ Desktop Control: Basic functionality available")
        else:
            print(f"{error_color}❌ Desktop Control: Not available")
        
        # Check color support
        if COLORAMA_AVAILABLE:
            print(f"{status_color}✅ UI Enhancement: Colored output enabled")
        else:
            print(f"{warning_color}⚠️  UI Enhancement: Basic text mode")
        
        print(f"{'─'*40}")
        print(f"{status_color}📊 Commands processed this session: {self.commands_processed}")
        
    def print_help(self):
        """Print enhanced help information"""
        help_color = Fore.CYAN if COLORAMA_AVAILABLE else ""
        cmd_color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
        
        print(f"\n{help_color}📚 SHADOW AI COMMAND REFERENCE")
        print(f"{'═'*50}")
        
        print(f"\n{help_color}🖥️  DESKTOP AUTOMATION:")
        print(f"{cmd_color}  • open notepad                    {help_color}- Open Notepad application")
        print(f"{cmd_color}  • open notepad and write [text]   {help_color}- Open Notepad and type text")
        print(f"{cmd_color}  • write an article about [topic]  {help_color}- Generate and write article")
        print(f"{cmd_color}  • open [app name]                 {help_color}- Open any application")
        print(f"{cmd_color}  • take a screenshot               {help_color}- Capture screen")
        print(f"{cmd_color}  • type: [your text]               {help_color}- Type specific text")
        print(f"{cmd_color}  • click at [x,y]                  {help_color}- Click at coordinates")
        
        print(f"\n{help_color}🎯 ARTICLE GENERATION:")
        print(f"{cmd_color}  • write an article about ai       {help_color}- Comprehensive AI article")
        print(f"{cmd_color}  • write an article about asi      {help_color}- Artificial Super Intelligence")
        print(f"{cmd_color}  • write an article about ml       {help_color}- Machine Learning article")
        print(f"{cmd_color}  • write an article about tech     {help_color}- Technology overview")
        print(f"{cmd_color}  • [topic] and save it as [file]   {help_color}- Write and save with filename")
        
        print(f"\n{help_color}🔧 SYSTEM COMMANDS:")
        print(f"{cmd_color}  • help                            {help_color}- Show this help")
        print(f"{cmd_color}  • status                          {help_color}- Show system status")
        print(f"{cmd_color}  • demo                            {help_color}- Run demonstration")
        print(f"{cmd_color}  • clear                           {help_color}- Clear screen")
        print(f"{cmd_color}  • quit / exit                     {help_color}- Exit Shadow AI")
        
        print(f"\n{help_color}💡 EXAMPLES:")
        print(f"{cmd_color}  Shadow AI > open notepad and write hello world")
        print(f"{cmd_color}  Shadow AI > write an article about artificial intelligence")
        print(f"{cmd_color}  Shadow AI > take a screenshot")
        print(f"{cmd_color}  Shadow AI > open calculator")
        
        print(f"\n{help_color}{'═'*50}")
    
    def process_enhanced_command(self, user_input: str) -> bool:
        """Process user command with enhanced functionality"""
        user_input = user_input.strip()
        command_lower = user_input.lower()
        
        # System commands
        if command_lower in ['quit', 'exit', 'q']:
            return False
        elif command_lower == 'help':
            self.print_help()
            return True
        elif command_lower == 'status':
            self.print_status()
            return True
        elif command_lower == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            return True
        elif command_lower == 'demo':
            self.run_demo()
            return True
        
        # Enhanced command processing
        if enhanced_controller:
            success = self.execute_desktop_command(user_input, command_lower)
            if success:
                return True
        
        # Try AI processing if available
        if AI_AVAILABLE:
            try:
                action_data = process_command(user_input)
                success = self.execute_ai_command(action_data)
                if success:
                    return True
            except Exception as e:
                logging.error(f"AI processing error: {e}")
        
        # Fallback response
        self.print_response("I'm not sure how to handle that command. Try 'help' for available commands.", "warning")
        return True
    
    def execute_desktop_command(self, user_input: str, command_lower: str) -> bool:
        """Execute desktop automation commands"""
        try:
            # Article generation commands
            if "write an article about" in command_lower:
                topic = command_lower.split("write an article about")[1].strip()
                self.print_response(f"📝 Writing article about {topic}... Opening Notepad.", "info")
                
                if hasattr(enhanced_controller, 'open_notepad_and_write_article'):
                    success = enhanced_controller.open_notepad_and_write_article(topic)
                else:
                    # Fallback to basic method
                    success = enhanced_controller.open_notepad()
                    if success:
                        time.sleep(2)
                        article_content = self.generate_basic_article(topic)
                        success = enhanced_controller.type_text(article_content, interval=0.02)
                
                if success:
                    self.print_response(f"✅ Article about {topic} written!", "success")
                else:
                    self.print_response("❌ Enhanced desktop controller not available", "error")
                return True
            
            # Article generation with save
            elif "write an article about" in command_lower and "save" in command_lower:
                parts = command_lower.split("and save it as")
                if len(parts) == 2:
                    topic = parts[0].split("write an article about")[1].strip()
                    filename = parts[1].strip()
                    self.print_response(f"📝 Writing article about {topic} and saving as {filename}...", "info")
                    
                    if hasattr(enhanced_controller, 'open_notepad_and_write_article_save_as'):
                        success = enhanced_controller.open_notepad_and_write_article_save_as(topic, filename)
                    else:
                        # Fallback method
                        success = enhanced_controller.open_notepad()
                        if success:
                            time.sleep(2)
                            article_content = self.generate_basic_article(topic)
                            success = enhanced_controller.type_text(article_content, interval=0.02)
                            if success:
                                # Try to save
                                enhanced_controller.key_combination(['ctrl', 's'])
                                time.sleep(1)
                                enhanced_controller.type_text(filename)
                                enhanced_controller.press_key('enter')
                    
                    if success:
                        self.print_response(f"✅ Article about {topic} written and saved as {filename}!", "success")
                    else:
                        self.print_response("❌ Enhanced desktop controller not available", "error")
                    return True
            
            # Notepad commands
            elif "open notepad and write" in command_lower:
                text_to_write = command_lower.split("open notepad and write")[1].strip()
                self.print_response("📝 Opening Notepad and writing text...", "info")
                
                success = enhanced_controller.open_or_activate_notepad() if hasattr(enhanced_controller, 'open_or_activate_notepad') else enhanced_controller.open_notepad()
                if success:
                    time.sleep(2)
                    success = enhanced_controller.type_text(text_to_write)
                
                if success:
                    self.print_response("✅ Text written successfully!", "success")
                else:
                    self.print_response("❌ Failed to write text.", "error")
                return True
            
            elif "open notepad" in command_lower:
                self.print_response("📝 Opening Notepad...", "info")
                success = enhanced_controller.open_notepad()
                if success:
                    self.print_response("✅ Notepad opened successfully!", "success")
                else:
                    self.print_response("❌ Failed to open Notepad.", "error")
                return True
            
            # Application commands
            elif command_lower.startswith("open "):
                app_name = command_lower.split("open ")[1].strip()
                self.print_response(f"🚀 Opening {app_name}...", "info")
                success = enhanced_controller.open_application(app_name)
                if success:
                    self.print_response(f"✅ {app_name} opened successfully!", "success")
                else:
                    self.print_response(f"❌ Failed to open {app_name}.", "error")
                return True
            
            # Screenshot command
            elif "take a screenshot" in command_lower or "screenshot" in command_lower:
                self.print_response("📸 Taking screenshot...", "info")
                screenshot_path = enhanced_controller.take_screenshot()
                if screenshot_path:
                    self.print_response(f"✅ Screenshot saved: {screenshot_path}", "success")
                else:
                    self.print_response("❌ Failed to take screenshot.", "error")
                return True
            
            # Type command
            elif command_lower.startswith("type:"):
                text_to_type = user_input.split(":", 1)[1].strip()
                self.print_response(f"⌨️  Typing: {text_to_type[:50]}...", "info")
                success = enhanced_controller.type_text(text_to_type)
                if success:
                    self.print_response("✅ Text typed successfully!", "success")
                else:
                    self.print_response("❌ Failed to type text.", "error")
                return True
            
            # Click command
            elif command_lower.startswith("click at"):
                try:
                    coords = command_lower.split("click at")[1].strip().split(",")
                    x, y = int(coords[0]), int(coords[1])
                    self.print_response(f"🖱️  Clicking at ({x}, {y})...", "info")
                    success = enhanced_controller.click_at(x, y)
                    if success:
                        self.print_response("✅ Click executed successfully!", "success")
                    else:
                        self.print_response("❌ Failed to execute click.", "error")
                    return True
                except (ValueError, IndexError):
                    self.print_response("❌ Invalid coordinates. Use format: click at x,y", "error")
                    return True
            
        except Exception as e:
            logging.error(f"Desktop command error: {e}")
            self.print_response(f"❌ Error executing command: {e}", "error")
            return True
        
        return False
    
    def execute_ai_command(self, action_data: dict) -> bool:
        """Execute AI-processed commands"""
        try:
            task_type = action_data.get("task_type", "unknown")
            action = action_data.get("action", "unknown")
            description = action_data.get("description", "Processing command...")
            
            self.print_response(f"🧠 AI Processing: {description}", "info")
            
            # Handle different task types
            if task_type == "document_creation" and action == "create_article":
                topic = action_data.get("parameters", {}).get("topic", "technology")
                return self.execute_desktop_command(f"write an article about {topic}", f"write an article about {topic}")
            
            elif task_type == "desktop_control":
                if action == "open_notepad_and_type":
                    text = action_data.get("parameters", {}).get("text", "")
                    return self.execute_desktop_command(f"open notepad and write {text}", f"open notepad and write {text}")
                elif action == "open_notepad":
                    return self.execute_desktop_command("open notepad", "open notepad")
                elif action == "type_text":
                    text = action_data.get("parameters", {}).get("text", "")
                    return self.execute_desktop_command(f"type: {text}", f"type: {text}")
                elif action == "take_screenshot":
                    return self.execute_desktop_command("take a screenshot", "take a screenshot")
            
            # If we get here, the command was recognized but not handled
            self.print_response("🤖 Command understood but execution not implemented yet.", "warning")
            return True
            
        except Exception as e:
            logging.error(f"AI command execution error: {e}")
            self.print_response(f"❌ Error executing AI command: {e}", "error")
            return True
    
    def generate_basic_article(self, topic: str) -> str:
        """Generate a basic article when enhanced controller is not available"""
        return f"""Article: {topic.title()}
{'='*30}

This is a comprehensive article about {topic}.

Introduction
------------
{topic.title()} is an important topic in today's world.

Key Points
----------
• Point 1 about {topic}
• Point 2 about {topic}
• Point 3 about {topic}

Conclusion
----------
In conclusion, {topic} plays a significant role in our modern society.

---
Generated by Shadow AI
Date: {time.strftime('%B %d, %Y')}
"""
    
    def print_response(self, message: str, msg_type: str = "info"):
        """Print colored response message"""
        timestamp = time.strftime("%H:%M:%S")
        
        if COLORAMA_AVAILABLE:
            if msg_type == "success":
                color = Fore.GREEN
                icon = "✅"
            elif msg_type == "error":
                color = Fore.RED
                icon = "❌"
            elif msg_type == "warning":
                color = Fore.YELLOW
                icon = "⚠️ "
            else:  # info
                color = Fore.CYAN
                icon = "ℹ️ "
            
            print(f"{Fore.WHITE}[{timestamp}] {color}{icon} {message}")
        else:
            print(f"[{timestamp}] {message}")
    
    def run_demo(self):
        """Run a demonstration of Shadow AI capabilities"""
        demo_color = Fore.MAGENTA if COLORAMA_AVAILABLE else ""
        
        print(f"\n{demo_color}🎬 SHADOW AI DEMONSTRATION")
        print(f"{'─'*40}")
        
        demo_commands = [
            "Taking a screenshot...",
            "Opening Notepad...",
            "Writing sample text...",
            "Demonstrating AI capabilities..."
        ]
        
        for i, command in enumerate(demo_commands, 1):
            self.print_response(f"Demo {i}/4: {command}", "info")
            time.sleep(1)
        
        self.print_response("✅ Demo completed! Try 'help' to see all available commands.", "success")
    
    def run(self):
        """Main application loop"""
        self.print_response("🚀 Shadow AI Enhanced started successfully!", "success")
        self.print_response("Type 'help' for commands or 'status' for system information.", "info")
        
        while self.running:
            try:
                # Get user input with colored prompt
                if COLORAMA_AVAILABLE:
                    prompt = f"\n{Fore.YELLOW}🤖 Shadow AI > {Style.RESET_ALL}"
                else:
                    prompt = "\n🤖 Shadow AI > "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Process command
                self.commands_processed += 1
                self.running = self.process_enhanced_command(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW if COLORAMA_AVAILABLE else ''}👋 Goodbye!")
                break
            except Exception as e:
                logging.error(f"Main loop error: {e}")
                self.print_response(f"❌ Unexpected error: {e}", "error")

def main():
    """Main entry point with GUI option"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Shadow AI Enhanced")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("--cli", action="store_true", help="Launch CLI interface")
    
    args = parser.parse_args()
    
    try:
        if args.gui:
            # Launch GUI
            try:
                from gui.modern_gui import ModernShadowAI
                app = ModernShadowAI()
                app.run()
            except ImportError as e:
                print(f"GUI not available: {e}")
                print("Falling back to CLI interface...")
                shadow_ai = EnhancedShadowAI()
                shadow_ai.run()
        else:
            # Default to CLI
            shadow_ai = EnhancedShadowAI()
            shadow_ai.run()
            
    except Exception as e:
        print(f"Failed to start Shadow AI: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
