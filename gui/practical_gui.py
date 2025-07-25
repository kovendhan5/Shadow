#!/usr/bin/env python3
"""
Shadow AI - Practical Features GUI
Real working features: Notepad, article writing, file operations, and more!
"""

import sys
import os
import threading
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Import GUI modules
try:
    from tkinter import filedialog, messagebox, simpledialog
except ImportError:
    pass

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import UI framework
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    CTK_AVAILABLE = True
except ImportError:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    CTK_AVAILABLE = False

# Import Shadow AI
try:
    from main import ShadowAI
    SHADOW_AI_AVAILABLE = True
except ImportError:
    SHADOW_AI_AVAILABLE = False

class PracticalShadowAI:
    """Shadow AI GUI with practical, working features"""
    
    def __init__(self):
        self.shadow_ai = None
        self.is_processing = False
        self.setup_window()
        self.create_interface()
        self.init_shadow_ai()
        
    def setup_window(self):
        """Setup main window"""
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
            self.root.title("🚀 Shadow AI - Practical Features")
            self.root.geometry("1200x800")
        else:
            self.root = tk.Tk()
            self.root.title("🚀 Shadow AI - Practical Features")
            self.root.geometry("1200x800")
            self.root.configure(bg="#1a1a1a")
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Create the main interface"""
        if CTK_AVAILABLE:
            self.create_modern_interface()
        else:
            self.create_classic_interface()
    
    def create_modern_interface(self):
        """Create modern interface"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self.root, height=80)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🚀 Shadow AI - Practical Features",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(
            header,
            text="🟢 Ready for Action",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff00"
        )
        self.status_label.pack(side="right", padx=20, pady=20)
        
        # Main content
        content = ctk.CTkFrame(self.root)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content.grid_columnconfigure(2, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Feature panels
        self.create_feature_panels(content)
        
        # Chat area
        self.create_chat_area(content)
        
        # Input area
        self.create_input_area()
    
    def create_feature_panels(self, parent):
        """Create feature panels"""
        # Notepad & Writing Panel
        notepad_panel = ctk.CTkFrame(parent, width=200)
        notepad_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        notepad_panel.grid_propagate(False)
        
        panel_title = ctk.CTkLabel(
            notepad_panel,
            text="📝 Notepad & Writing",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        panel_title.pack(pady=(15, 10))
        
        # Notepad buttons
        notepad_features = [
            ("📝 Open Notepad", self.open_notepad),
            ("📄 Write Article", self.write_article_dialog),
            ("💡 Write AI Article", self.write_ai_article),
            ("📋 Write to Active", self.write_to_active),
            ("📚 Article Templates", self.show_templates)
        ]
        
        for text, command in notepad_features:
            btn = ctk.CTkButton(
                notepad_panel,
                text=text,
                command=command,
                height=35,
                font=ctk.CTkFont(size=12)
            )
            btn.pack(fill="x", padx=10, pady=3)
        
        # Applications Panel
        apps_panel = ctk.CTkFrame(parent, width=200)
        apps_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        apps_panel.grid_propagate(False)
        
        apps_title = ctk.CTkLabel(
            apps_panel,
            text="🚀 Applications",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        apps_title.pack(pady=(15, 10))
        
        # Application buttons
        app_features = [
            ("📝 Notepad", lambda: self.open_application("notepad")),
            ("🌐 Browser", lambda: self.open_application("browser")),
            ("📁 Explorer", lambda: self.open_application("explorer")),
            ("⚙️ Calculator", lambda: self.open_application("calc")),
            ("🎨 Paint", lambda: self.open_application("mspaint")),
            ("📊 Excel", lambda: self.open_application("excel")),
            ("📄 Word", lambda: self.open_application("winword")),
            ("🔧 Control Panel", lambda: self.open_application("control"))
        ]
        
        for text, command in app_features:
            btn = ctk.CTkButton(
                apps_panel,
                text=text,
                command=command,
                height=30,
                font=ctk.CTkFont(size=11)
            )
            btn.pack(fill="x", padx=10, pady=2)
    
    def create_chat_area(self, parent):
        """Create chat area"""
        chat_frame = ctk.CTkFrame(parent)
        chat_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        chat_title = ctk.CTkLabel(
            chat_frame,
            text="💬 Activity Log",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chat_title.pack(pady=(20, 10))
        
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Welcome message
        self.add_message("system", "🚀 Shadow AI Practical Features Ready!")
        self.add_message("system", "📝 Click buttons to perform real actions")
        self.add_message("system", "💡 Try 'Write AI Article' or 'Open Notepad'")
    
    def create_input_area(self):
        """Create input area"""
        input_frame = ctk.CTkFrame(self.root, height=100)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Command examples
        examples_label = ctk.CTkLabel(
            input_frame,
            text="💡 Try: 'open notepad and write about Python' or 'write article about AI'",
            font=ctk.CTkFont(size=12)
        )
        examples_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter command (e.g., 'open notepad and write about space exploration')",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.input_entry.grid(row=1, column=0, sticky="ew", padx=(20, 10), pady=(0, 15))
        self.input_entry.bind("<Return>", self.process_command)
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="🚀 Execute",
            command=self.process_command,
            width=100,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        send_btn.grid(row=1, column=1, padx=(0, 10), pady=(0, 15))
        
        help_btn = ctk.CTkButton(
            input_frame,
            text="❓ Help",
            command=self.show_help,
            width=80,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        help_btn.grid(row=1, column=2, padx=(0, 20), pady=(0, 15))
    
    def create_classic_interface(self):
        """Create classic Tkinter interface"""
        # Header
        header = tk.Frame(self.root, bg="#2d2d2d", height=60)
        header.pack(fill="x", padx=10, pady=(10, 5))
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🚀 Shadow AI - Practical Features",
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Feature buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#2d2d2d")
        buttons_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Quick action buttons
        actions = [
            ("📝 Open Notepad", self.open_notepad),
            ("📄 Write Article", self.write_article_dialog),
            ("🌐 Open Browser", lambda: self.open_application("browser")),
            ("📁 File Explorer", lambda: self.open_application("explorer")),
            ("⚙️ Calculator", lambda: self.open_application("calc"))
        ]
        
        for text, command in actions:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                bg="#0078d4",
                fg="white",
                font=("Arial", 10),
                padx=10,
                pady=5
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # Chat area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            bg="#2d2d2d",
            fg="white",
            font=("Consolas", 11),
            wrap=tk.WORD
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input area
        input_frame = tk.Frame(main_frame, bg="#1a1a1a")
        input_frame.pack(fill="x", pady=(10, 0))
        
        self.input_entry = tk.Entry(
            input_frame,
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 12),
            insertbackground="white"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.process_command)
        
        send_btn = tk.Button(
            input_frame,
            text="Execute",
            command=self.process_command,
            bg="#0078d4",
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        send_btn.pack(side="right")
        
        # Welcome message
        self.add_message("system", "🚀 Shadow AI Ready! Click buttons for real actions.")
    
    def init_shadow_ai(self):
        """Initialize Shadow AI"""
        def initialize():
            try:
                self.update_status("🟡 Loading...")
                if SHADOW_AI_AVAILABLE:
                    self.shadow_ai = ShadowAI()
                    self.shadow_ai.init_enhanced_features()
                    self.update_status("🟢 Ready for Action")
                    self.add_message("system", "✅ Shadow AI loaded with practical features!")
                else:
                    self.update_status("🟡 Demo Mode")
                    self.add_message("system", "⚠️ Demo mode - features will be simulated")
            except Exception as e:
                self.update_status("🔴 Error")
                self.add_message("system", f"❌ Error: {e}")
        
        threading.Thread(target=initialize, daemon=True).start()
    
    # Core functionality methods
    def add_message(self, sender, message):
        """Add message to chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        
        if CTK_AVAILABLE:
            self.chat_display.insert("end", formatted)
            self.chat_display.see("end")
        else:
            self.chat_display.insert(tk.END, formatted)
            self.chat_display.see(tk.END)
    
    def update_status(self, status):
        """Update status"""
        if hasattr(self, 'status_label'):
            if CTK_AVAILABLE:
                self.status_label.configure(text=status)
            else:
                self.status_label.configure(text=status)
    
    def process_command(self, event=None):
        """Process user command"""
        if self.is_processing:
            return
        
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.input_entry.delete(0, "end" if CTK_AVAILABLE else tk.END)
        
        # Add to log
        self.add_message("user", f"👤 Command: {command}")
        
        # Process command
        threading.Thread(target=self._process_command, args=(command,), daemon=True).start()
    
    def _process_command(self, command):
        """Process command in background"""
        self.is_processing = True
        self.update_status("🟡 Processing...")
        
        try:
            command_lower = command.lower()
            
            # Handle specific commands
            if "open notepad" in command_lower and "write" in command_lower:
                self.handle_notepad_write_command(command)
            elif "write article" in command_lower:
                topic = self.extract_topic_from_command(command)
                self.write_article_about(topic)
            elif "open" in command_lower and any(app in command_lower for app in ["notepad", "calculator", "paint", "browser"]):
                self.handle_open_command(command)
            elif self.shadow_ai:
                # Use Shadow AI for other commands
                result = self.shadow_ai.handle_enhanced_commands(command)
                if result:
                    self.add_message("system", "✅ Command executed successfully")
                else:
                    self.add_message("system", "⚠️ Command processed")
            else:
                self.add_message("system", f"🤖 Demo: Would execute '{command}'")
                
        except Exception as e:
            self.add_message("system", f"❌ Error: {e}")
        finally:
            self.is_processing = False
            self.update_status("🟢 Ready for Action")
    
    # Feature implementation methods
    def open_notepad(self):
        """Open Notepad"""
        self.add_message("system", "📝 Opening Notepad...")
        try:
            if self.shadow_ai:
                result = self.shadow_ai.execute_desktop_action('open_notepad', {})
                if result:
                    self.add_message("system", "✅ Notepad opened successfully!")
                else:
                    raise Exception("Shadow AI failed")
            else:
                # Fallback: direct subprocess
                subprocess.Popen(['notepad.exe'])
                self.add_message("system", "✅ Notepad opened!")
        except Exception as e:
            self.add_message("system", f"❌ Error opening Notepad: {e}")
    
    def write_article_dialog(self):
        """Show dialog to write article"""
        if CTK_AVAILABLE:
            dialog = ctk.CTkInputDialog(text="Enter article topic:", title="Write Article")
            topic = dialog.get_input()
        else:
            try:
                topic = simpledialog.askstring("Write Article", "Enter article topic:")
            except:
                topic = input("Enter article topic: ") if hasattr(sys, 'ps1') else "Technology"
        
        if topic:
            self.write_article_about(topic)
    
    def write_ai_article(self):
        """Write an article about AI"""
        self.write_article_about("Artificial Intelligence")
    
    def write_article_about(self, topic):
        """Write an article about the specified topic"""
        self.add_message("system", f"📄 Writing article about '{topic}'...")
        
        def write_article():
            try:
                if self.shadow_ai:
                    # Use Shadow AI to open notepad and write article
                    result = self.shadow_ai.execute_desktop_action('open_notepad_and_write_article', {'topic': topic})
                    if result:
                        self.add_message("system", f"✅ Article about '{topic}' written to Notepad!")
                    else:
                        self.fallback_write_article(topic)
                else:
                    self.fallback_write_article(topic)
            except Exception as e:
                self.add_message("system", f"❌ Error writing article: {e}")
        
        threading.Thread(target=write_article, daemon=True).start()
    
    def fallback_write_article(self, topic):
        """Fallback method to write article"""
        try:
            # Open notepad
            subprocess.Popen(['notepad.exe'])
            time.sleep(2)  # Wait for notepad to open
            
            # Generate article content
            article = self.generate_simple_article(topic)
            
            # Type the article (simple automation)
            import pyautogui
            pyautogui.typewrite(article, interval=0.01)
            
            self.add_message("system", f"✅ Article about '{topic}' written!")
        except Exception as e:
            self.add_message("system", f"❌ Fallback write failed: {e}")
    
    def generate_simple_article(self, topic):
        """Generate a simple article"""
        return f"""# Article: {topic.title()}

## Introduction

{topic.title()} is an important topic that deserves our attention. This article provides an overview of the key concepts and implications.

## What is {topic.title()}?

{topic.title()} refers to the study and application of concepts related to {topic.lower()}. It has become increasingly relevant in today's world.

## Key Points

1. **Definition**: {topic.title()} encompasses various aspects and applications
2. **Importance**: It plays a crucial role in modern society
3. **Applications**: Used across multiple industries and domains
4. **Future**: Continued development and innovation expected

## Benefits

- Improved understanding of the subject
- Enhanced capabilities and efficiency
- Better decision-making processes
- Increased innovation potential

## Conclusion

{topic.title()} continues to evolve and impact our daily lives. Understanding its principles and applications is essential for future progress.

---
Generated by Shadow AI on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    def write_to_active(self):
        """Write to currently active window"""
        if CTK_AVAILABLE:
            dialog = ctk.CTkInputDialog(text="Enter text to type:", title="Write to Active Window")
            text = dialog.get_input()
        else:
            try:
                text = simpledialog.askstring("Write to Active", "Enter text to type:")
            except:
                text = input("Enter text to type: ") if hasattr(sys, 'ps1') else "Hello from Shadow AI!"
        
        if text:
            self.add_message("system", f"⌨️ Typing text to active window...")
            try:
                time.sleep(1)  # Give user time to switch windows
                import pyautogui
                pyautogui.typewrite(text, interval=0.05)
                self.add_message("system", "✅ Text typed successfully!")
            except Exception as e:
                self.add_message("system", f"❌ Error typing text: {e}")
    
    def show_templates(self):
        """Show article templates"""
        templates = [
            "Artificial Intelligence",
            "Climate Change",
            "Space Exploration", 
            "Technology Trends",
            "Health and Wellness",
            "Business Strategy",
            "Education Innovation",
            "Environmental Conservation"
        ]
        
        self.add_message("system", "📚 Available Article Templates:")
        for i, template in enumerate(templates, 1):
            self.add_message("system", f"  {i}. {template}")
        self.add_message("system", "💡 Type 'write article about [topic]' to use any template")
    
    def open_application(self, app_name):
        """Open specified application"""
        self.add_message("system", f"🚀 Opening {app_name}...")
        
        app_commands = {
            "notepad": "notepad.exe",
            "browser": "start microsoft-edge:",
            "explorer": "explorer.exe",
            "calc": "calc.exe",
            "calculator": "calc.exe",
            "mspaint": "mspaint.exe",
            "paint": "mspaint.exe",
            "excel": "excel.exe",
            "winword": "winword.exe",
            "word": "winword.exe",
            "control": "control.exe"
        }
        
        command = app_commands.get(app_name.lower(), app_name)
        
        try:
            if command.startswith("start "):
                os.system(command)
            else:
                subprocess.Popen([command])
            self.add_message("system", f"✅ {app_name.title()} opened successfully!")
        except Exception as e:
            self.add_message("system", f"❌ Error opening {app_name}: {e}")
    
    def handle_notepad_write_command(self, command):
        """Handle 'open notepad and write' commands"""
        topic = self.extract_topic_from_command(command)
        self.add_message("system", f"📝 Opening Notepad and writing about '{topic}'...")
        
        def execute():
            try:
                if self.shadow_ai:
                    result = self.shadow_ai.execute_desktop_action('open_notepad_and_write_article', {'topic': topic})
                    if result:
                        self.add_message("system", f"✅ Notepad opened and article about '{topic}' written!")
                        return
                
                # Fallback
                self.fallback_write_article(topic)
            except Exception as e:
                self.add_message("system", f"❌ Error: {e}")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def handle_open_command(self, command):
        """Handle 'open' commands"""
        command_lower = command.lower()
        
        if "notepad" in command_lower:
            self.open_notepad()
        elif "calculator" in command_lower or "calc" in command_lower:
            self.open_application("calc")
        elif "paint" in command_lower:
            self.open_application("mspaint")
        elif "browser" in command_lower:
            self.open_application("browser")
        elif "explorer" in command_lower:
            self.open_application("explorer")
    
    def extract_topic_from_command(self, command):
        """Extract topic from command"""
        command_lower = command.lower()
        
        # Look for "about X" pattern
        if " about " in command_lower:
            topic = command_lower.split(" about ", 1)[1]
            return topic.strip()
        
        # Look for "on X" pattern  
        if " on " in command_lower:
            topic = command_lower.split(" on ", 1)[1]
            return topic.strip()
        
        # Default topics based on keywords
        keywords = {
            "ai": "Artificial Intelligence",
            "artificial intelligence": "Artificial Intelligence", 
            "python": "Python Programming",
            "space": "Space Exploration",
            "climate": "Climate Change",
            "technology": "Technology Trends",
            "health": "Health and Wellness"
        }
        
        for keyword, topic in keywords.items():
            if keyword in command_lower:
                return topic
        
        return "Technology and Innovation"
    
    def show_help(self):
        """Show help information"""
        help_text = """
🚀 Shadow AI Practical Features - Help

📝 NOTEPAD & WRITING:
• Click 'Open Notepad' to launch Notepad
• Click 'Write Article' to write about any topic
• Type: "open notepad and write about space exploration"
• Type: "write article about artificial intelligence"

🚀 APPLICATIONS:
• Click app buttons to launch applications
• Type: "open calculator" or "open browser"

⌨️ TEXT AUTOMATION:
• Click 'Write to Active' to type in current window
• Articles are automatically generated and typed

💡 EXAMPLE COMMANDS:
• "open notepad and write about Python programming"
• "write article about climate change"  
• "open calculator"
• "open browser"

✨ FEATURES:
• Real applications actually open
• Articles are automatically written to Notepad
• Text automation works with any application
• All features work without internet connection
        """
        
        if CTK_AVAILABLE:
            help_window = ctk.CTkToplevel(self.root)
            help_window.title("Help - Shadow AI")
            help_window.geometry("600x500")
            
            text_widget = ctk.CTkTextbox(help_window, wrap="word")
            text_widget.pack(fill="both", expand=True, padx=20, pady=20)
            text_widget.insert("0.0", help_text)
        else:
            messagebox.showinfo("Help - Shadow AI", help_text)
    
    def run(self):
        """Run the application"""
        try:
            if hasattr(self.root, 'report_callback_exception'):
                self.root.report_callback_exception = lambda *args: None
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

def main():
    """Main function"""
    print("🚀 Launching Shadow AI Practical Features GUI...")
    
    try:
        app = PracticalShadowAI()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
