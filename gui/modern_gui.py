#!/usr/bin/env python3
"""
Shadow AI - Modern GUI Interface
Advanced desktop AI assistant with beautiful modern design
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

try:
    from control.enhanced_desktop import enhanced_controller
    ENHANCED_DESKTOP = True
except ImportError:
    try:
        from control.desktop import desktop_controller as enhanced_controller
        ENHANCED_DESKTOP = False
    except ImportError:
        enhanced_controller = None

try:
    from brain.gpt_agent import process_command
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class ModernShadowAI:
    """Modern Shadow AI GUI with advanced design"""
    
    def __init__(self):
        self.setup_appearance()
        self.create_main_window()
        self.create_widgets()
        self.status_messages = []
        
    def setup_appearance(self):
        """Setup modern appearance theme"""
        if CTK_AVAILABLE:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            self.use_ctk = True
        else:
            self.use_ctk = False
            
    def create_main_window(self):
        """Create main application window"""
        if self.use_ctk:
            self.root = ctk.CTk()
            self.root.title("Shadow AI - Modern Desktop Assistant")
            self.root.geometry("1200x800")
            self.root.minsize(900, 600)
            
            # Set modern styling
            self.root._set_appearance_mode("dark")
        else:
            self.root = tk.Tk()
            self.root.title("Shadow AI - Modern Desktop Assistant")
            self.root.geometry("1200x800")
            self.root.minsize(900, 600)
            self.root.configure(bg="#1a1a1a")
            
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def create_widgets(self):
        """Create all GUI widgets with modern design"""
        # Main container
        if self.use_ctk:
            main_frame = ctk.CTkFrame(self.root)
        else:
            main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        self.create_content_area(main_frame)
        
        # Footer
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Create header with title and status"""
        if self.use_ctk:
            header_frame = ctk.CTkFrame(parent)
            header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
            
            # Title
            title_label = ctk.CTkLabel(
                header_frame, 
                text="🤖 SHADOW AI", 
                font=ctk.CTkFont(size=28, weight="bold")
            )
            title_label.grid(row=0, column=0, padx=20, pady=15)
            
            # Subtitle
            subtitle_label = ctk.CTkLabel(
                header_frame,
                text="Advanced Desktop AI Assistant",
                font=ctk.CTkFont(size=14)
            )
            subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15))
            
            # Status indicator
            self.status_label = ctk.CTkLabel(
                header_frame,
                text="🟢 Ready",
                font=ctk.CTkFont(size=12),
                text_color="#00ff00"
            )
            self.status_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
            
        else:
            header_frame = tk.Frame(parent, bg="#2d2d2d", relief="raised", bd=2)
            header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
            
            # Title
            title_label = tk.Label(
                header_frame,
                text="🤖 SHADOW AI",
                font=("Arial", 28, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
            title_label.grid(row=0, column=0, padx=20, pady=15)
            
            # Subtitle
            subtitle_label = tk.Label(
                header_frame,
                text="Advanced Desktop AI Assistant",
                font=("Arial", 14),
                bg="#2d2d2d",
                fg="#cccccc"
            )
            subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15))
            
            # Status indicator
            self.status_label = tk.Label(
                header_frame,
                text="🟢 Ready",
                font=("Arial", 12),
                bg="#2d2d2d",
                fg="#00ff00"
            )
            self.status_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
            
    def create_content_area(self, parent):
        """Create main content area with tabs"""
        # Left sidebar
        self.create_sidebar(parent)
        
        # Main content with tabs
        self.create_main_content(parent)
        
        # Right panel
        self.create_right_panel(parent)
        
    def create_sidebar(self, parent):
        """Create left sidebar with quick actions"""
        if self.use_ctk:
            sidebar = ctk.CTkFrame(parent, width=200)
            sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 10))
            sidebar.grid_propagate(False)
            
            # Quick Actions
            quick_label = ctk.CTkLabel(sidebar, text="Quick Actions", font=ctk.CTkFont(size=16, weight="bold"))
            quick_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            # Action buttons
            actions = [
                ("📝 Open Notepad", self.open_notepad),
                ("🧠 Write AI Article", self.write_ai_article),
                ("📸 Take Screenshot", self.take_screenshot),
                ("🧮 Open Calculator", self.open_calculator),
                ("🌐 Open Browser", self.open_browser),
                ("📁 Open Explorer", self.open_explorer)
            ]
            
            for i, (text, command) in enumerate(actions, 1):
                btn = ctk.CTkButton(
                    sidebar,
                    text=text,
                    command=command,
                    width=160,
                    height=35
                )
                btn.grid(row=i, column=0, padx=20, pady=5)
                
        else:
            sidebar = tk.Frame(parent, bg="#2d2d2d", width=200, relief="sunken", bd=2)
            sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 10))
            sidebar.grid_propagate(False)
            
            # Quick Actions
            quick_label = tk.Label(sidebar, text="Quick Actions", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="#ffffff")
            quick_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            # Action buttons
            actions = [
                ("📝 Open Notepad", self.open_notepad),
                ("🧠 Write AI Article", self.write_ai_article),
                ("📸 Take Screenshot", self.take_screenshot),
                ("🧮 Open Calculator", self.open_calculator),
                ("🌐 Open Browser", self.open_browser),
                ("📁 Open Explorer", self.open_explorer)
            ]
            
            for i, (text, command) in enumerate(actions, 1):
                btn = tk.Button(
                    sidebar,
                    text=text,
                    command=command,
                    width=18,
                    height=2,
                    bg="#0078d4",
                    fg="white",
                    font=("Arial", 10),
                    relief="flat",
                    cursor="hand2"
                )
                btn.grid(row=i, column=0, padx=20, pady=5)
                
    def create_main_content(self, parent):
        """Create main content area with tabs"""
        if self.use_ctk:
            # Notebook for tabs
            self.notebook = ctk.CTkTabview(parent)
            self.notebook.grid(row=1, column=1, sticky="nsew", padx=5)
            
            # Chat tab
            self.chat_tab = self.notebook.add("💬 Chat")
            self.create_chat_interface(self.chat_tab)
            
            # Commands tab
            self.commands_tab = self.notebook.add("⚡ Commands")
            self.create_commands_interface(self.commands_tab)
            
            # Settings tab
            self.settings_tab = self.notebook.add("⚙️ Settings")
            self.create_settings_interface(self.settings_tab)
            
        else:
            # Create notebook manually for older tkinter
            notebook_frame = tk.Frame(parent, bg="#1a1a1a")
            notebook_frame.grid(row=1, column=1, sticky="nsew", padx=5)
            notebook_frame.grid_columnconfigure(0, weight=1)
            notebook_frame.grid_rowconfigure(1, weight=1)
            
            # Tab buttons
            tab_frame = tk.Frame(notebook_frame, bg="#2d2d2d")
            tab_frame.grid(row=0, column=0, sticky="ew")
            
            self.tab_buttons = {}
            self.tab_frames = {}
            
            tabs = [("💬 Chat", "chat"), ("⚡ Commands", "commands"), ("⚙️ Settings", "settings")]
            
            for i, (text, key) in enumerate(tabs):
                btn = tk.Button(
                    tab_frame,
                    text=text,
                    command=lambda k=key: self.switch_tab(k),
                    bg="#0078d4" if i == 0 else "#2d2d2d",
                    fg="white",
                    font=("Arial", 10),
                    relief="flat",
                    padx=20,
                    pady=10
                )
                btn.grid(row=0, column=i, padx=2)
                self.tab_buttons[key] = btn
                
            # Tab content area
            content_frame = tk.Frame(notebook_frame, bg="#1a1a1a")
            content_frame.grid(row=1, column=0, sticky="nsew")
            content_frame.grid_columnconfigure(0, weight=1)
            content_frame.grid_rowconfigure(0, weight=1)
            
            # Create tab frames
            for _, key in tabs:
                frame = tk.Frame(content_frame, bg="#1a1a1a")
                self.tab_frames[key] = frame
                
            # Create interfaces
            self.create_chat_interface(self.tab_frames["chat"])
            self.create_commands_interface(self.tab_frames["commands"])
            self.create_settings_interface(self.tab_frames["settings"])
            
            # Show first tab
            self.current_tab = "chat"
            self.tab_frames["chat"].grid(row=0, column=0, sticky="nsew")
            
    def switch_tab(self, tab_key):
        """Switch between tabs in manual notebook"""
        if hasattr(self, 'current_tab'):
            self.tab_frames[self.current_tab].grid_remove()
            self.tab_buttons[self.current_tab].configure(bg="#2d2d2d")
            
        self.tab_frames[tab_key].grid(row=0, column=0, sticky="nsew")
        self.tab_buttons[tab_key].configure(bg="#0078d4")
        self.current_tab = tab_key
        
    def create_chat_interface(self, parent):
        """Create chat interface"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        if self.use_ctk:
            # Chat display area
            self.chat_display = ctk.CTkTextbox(
                parent,
                wrap="word",
                height=400,
                font=ctk.CTkFont(size=12)
            )
            self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))
            
            # Input frame
            input_frame = ctk.CTkFrame(parent)
            input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
            input_frame.grid_columnconfigure(0, weight=1)
            
            # Command input
            self.command_entry = ctk.CTkEntry(
                input_frame,
                placeholder_text="Type your command here... (e.g., 'open notepad and write hello')",
                height=40,
                font=ctk.CTkFont(size=12)
            )
            self.command_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
            self.command_entry.bind("<Return>", self.process_command)
            
            # Send button
            send_btn = ctk.CTkButton(
                input_frame,
                text="Send",
                command=self.process_command,
                width=80,
                height=40
            )
            send_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
            
        else:
            # Chat display area
            self.chat_display = scrolledtext.ScrolledText(
                parent,
                wrap=tk.WORD,
                height=20,
                font=("Consolas", 11),
                bg="#1e1e1e",
                fg="#ffffff",
                insertbackground="#ffffff"
            )
            self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))
            
            # Input frame
            input_frame = tk.Frame(parent, bg="#1a1a1a")
            input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
            input_frame.grid_columnconfigure(0, weight=1)
            
            # Command input
            self.command_entry = tk.Entry(
                input_frame,
                font=("Arial", 12),
                bg="#2d2d2d",
                fg="#ffffff",
                insertbackground="#ffffff",
                relief="flat",
                bd=5
            )
            self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)
            self.command_entry.bind("<Return>", self.process_command)
            
            # Send button
            send_btn = tk.Button(
                input_frame,
                text="Send",
                command=self.process_command,
                bg="#0078d4",
                fg="white",
                font=("Arial", 10),
                relief="flat",
                padx=20,
                cursor="hand2"
            )
            send_btn.grid(row=0, column=1, padx=(5, 0), pady=5)
            
        # Add welcome message
        self.add_chat_message("🤖 Shadow AI", "Welcome! I'm your AI desktop assistant. Try commands like:\n• 'open notepad and write an article about AI'\n• 'take a screenshot'\n• 'open calculator'")
        
    def create_commands_interface(self, parent):
        """Create commands reference interface"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        if self.use_ctk:
            commands_text = ctk.CTkTextbox(parent, wrap="word")
            commands_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        else:
            commands_text = scrolledtext.ScrolledText(
                parent,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            commands_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            
        # Commands reference
        commands_ref = """🔧 SHADOW AI COMMAND REFERENCE

📝 DOCUMENT & TEXT COMMANDS:
• "open notepad" - Open Notepad application
• "open notepad and write [text]" - Open Notepad and type text
• "write an article about [topic]" - Generate and write comprehensive article
• "type: [your text]" - Type specific text

🖥️ DESKTOP AUTOMATION:
• "open [application]" - Open any application (calculator, chrome, etc.)
• "take a screenshot" - Capture current screen
• "click at [x,y]" - Click at specific coordinates

🧠 AI ARTICLE GENERATION:
• "write an article about ai" - Comprehensive AI article (850+ words)
• "write an article about machine learning" - ML article
• "write an article about technology" - Tech overview
• "write an article about deep learning" - DL article

🎯 EXAMPLES:
Shadow AI > open notepad and write hello world
Shadow AI > write an article about artificial intelligence
Shadow AI > take a screenshot
Shadow AI > open calculator
Shadow AI > type: This is a test message

🔍 SYSTEM COMMANDS:
• "help" - Show command help
• "status" - Display system status
• "clear" - Clear chat history

💡 TIP: You can use natural language! Shadow AI understands various ways to express commands."""

        commands_text.insert("1.0", commands_ref)
        commands_text.configure(state="disabled")
        
    def create_settings_interface(self, parent):
        """Create settings interface"""
        parent.grid_columnconfigure(0, weight=1)
        
        if self.use_ctk:
            # System info
            info_frame = ctk.CTkFrame(parent)
            info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
            
            info_label = ctk.CTkLabel(info_frame, text="System Information", font=ctk.CTkFont(size=16, weight="bold"))
            info_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            # Status indicators
            status_info = f"""Python: {sys.version.split()[0]}
Enhanced Desktop: {'✓' if ENHANCED_DESKTOP else '✗'}
AI Integration: {'✓' if AI_AVAILABLE else '✗'}
CustomTkinter: {'✓' if CTK_AVAILABLE else '✗'}
Project Path: {Path(__file__).parent.parent}"""

            status_text = ctk.CTkTextbox(info_frame, height=150)
            status_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
            status_text.insert("1.0", status_info)
            status_text.configure(state="disabled")
            
        else:
            # System info
            info_frame = tk.Frame(parent, bg="#2d2d2d", relief="raised", bd=2)
            info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
            info_frame.grid_columnconfigure(0, weight=1)
            
            info_label = tk.Label(info_frame, text="System Information", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="#ffffff")
            info_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            status_info = f"""Python: {sys.version.split()[0]}
Enhanced Desktop: {'✓' if ENHANCED_DESKTOP else '✗'}
AI Integration: {'✓' if AI_AVAILABLE else '✗'}
CustomTkinter: {'✓' if CTK_AVAILABLE else '✗'}
Project Path: {Path(__file__).parent.parent}"""

            status_text = tk.Text(
                info_frame,
                height=8,
                font=("Consolas", 10),
                bg="#1e1e1e",
                fg="#ffffff",
                relief="flat"
            )
            status_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
            status_text.insert("1.0", status_info)
            status_text.configure(state="disabled")
            
    def create_right_panel(self, parent):
        """Create right panel with activity log"""
        if self.use_ctk:
            right_panel = ctk.CTkFrame(parent, width=250)
            right_panel.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
            right_panel.grid_propagate(False)
            
            # Activity log
            log_label = ctk.CTkLabel(right_panel, text="Activity Log", font=ctk.CTkFont(size=16, weight="bold"))
            log_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            self.activity_log = ctk.CTkTextbox(
                right_panel,
                wrap="word",
                height=300,
                font=ctk.CTkFont(size=10)
            )
            self.activity_log.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
            
        else:
            right_panel = tk.Frame(parent, bg="#2d2d2d", width=250, relief="sunken", bd=2)
            right_panel.grid(row=1, column=2, sticky="nsew", padx=(10, 0))
            right_panel.grid_propagate(False)
            
            # Activity log
            log_label = tk.Label(right_panel, text="Activity Log", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="#ffffff")
            log_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            self.activity_log = scrolledtext.ScrolledText(
                right_panel,
                wrap=tk.WORD,
                height=15,
                width=30,
                font=("Consolas", 9),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            self.activity_log.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
            
        # Add initial log entry
        self.add_activity_log("System started successfully")
        
    def create_footer(self, parent):
        """Create footer with copyright and version"""
        if self.use_ctk:
            footer_frame = ctk.CTkFrame(parent)
            footer_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
            
            footer_label = ctk.CTkLabel(
                footer_frame,
                text="Shadow AI v2.0 Enhanced | Modern Desktop Assistant | 2025",
                font=ctk.CTkFont(size=10)
            )
            footer_label.grid(row=0, column=0, padx=20, pady=10)
            
        else:
            footer_frame = tk.Frame(parent, bg="#2d2d2d", relief="raised", bd=1)
            footer_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
            
            footer_label = tk.Label(
                footer_frame,
                text="Shadow AI v2.0 Enhanced | Modern Desktop Assistant | 2025",
                font=("Arial", 10),
                bg="#2d2d2d",
                fg="#cccccc"
            )
            footer_label.grid(row=0, column=0, padx=20, pady=10)
            
    def add_chat_message(self, sender, message):
        """Add message to chat display"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        self.chat_display.insert("end", formatted_message)
        self.chat_display.see("end")
        
    def add_activity_log(self, message):
        """Add entry to activity log"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.activity_log.insert("end", formatted_message)
        self.activity_log.see("end")
        
    def update_status(self, message, color="#00ff00"):
        """Update status indicator"""
        if self.use_ctk:
            self.status_label.configure(text=message, text_color=color)
        else:
            self.status_label.configure(text=message, fg=color)
            
    def process_command(self, event=None):
        """Process user command"""
        command = self.command_entry.get().strip()
        if not command:
            return
            
        # Clear input
        self.command_entry.delete(0, "end")
        
        # Add to chat
        self.add_chat_message("You", command)
        self.add_activity_log(f"Command: {command}")
        
        # Update status
        self.update_status("🟡 Processing...", "#ffff00")
        
        # Process in thread to avoid blocking UI
        threading.Thread(target=self._execute_command, args=(command,), daemon=True).start()
        
    def _execute_command(self, command):
        """Execute command in background thread"""
        try:
            success = False
            response = "Command processed."
            
            command_lower = command.lower()
            
            # Handle specific commands
            if "open notepad and write an article about" in command_lower:
                topic = command_lower.split("write an article about")[1].strip()
                if enhanced_controller and hasattr(enhanced_controller, 'open_notepad_and_write_article'):
                    success = enhanced_controller.open_notepad_and_write_article(topic)
                    response = f"✅ Article about {topic} written to Notepad!" if success else f"❌ Failed to write article about {topic}"
                else:
                    response = "❌ Enhanced desktop controller not available"
                    
            elif "write an article about" in command_lower:
                topic = command_lower.split("write an article about")[1].strip()
                if enhanced_controller:
                    success = enhanced_controller.open_notepad()
                    if success:
                        time.sleep(2)
                        article = self.generate_simple_article(topic)
                        success = enhanced_controller.type_text(article, interval=0.02)
                    response = f"✅ Article about {topic} written!" if success else f"❌ Failed to write article"
                else:
                    response = "❌ Desktop controller not available"
                    
            elif "take a screenshot" in command_lower or "screenshot" in command_lower:
                if enhanced_controller:
                    screenshot_path = enhanced_controller.take_screenshot()
                    success = bool(screenshot_path)
                    response = f"✅ Screenshot saved!" if success else "❌ Failed to take screenshot"
                else:
                    response = "❌ Desktop controller not available"
                    
            elif command_lower.startswith("open "):
                app_name = command_lower.split("open ")[1].strip()
                if enhanced_controller:
                    success = enhanced_controller.open_application(app_name)
                    response = f"✅ Opened {app_name}!" if success else f"❌ Failed to open {app_name}"
                else:
                    response = "❌ Desktop controller not available"
                    
            elif command_lower == "help":
                response = "📚 Check the Commands tab for full command reference!"
                success = True
                
            elif command_lower == "status":
                response = f"🔍 System Status:\n• Desktop: {'✓' if enhanced_controller else '✗'}\n• AI: {'✓' if AI_AVAILABLE else '✗'}\n• Enhanced: {'✓' if ENHANCED_DESKTOP else '✗'}"
                success = True
                
            else:
                # Try AI processing if available
                if AI_AVAILABLE:
                    try:
                        action_data = process_command(command)
                        response = f"🧠 AI processed: {action_data.get('description', 'Command understood')}"
                        success = True
                    except Exception as e:
                        response = f"🤖 I understand you want: {command}\nBut I need more specific commands. Try 'help' for examples."
                        success = False
                else:
                    response = "🤖 I didn't understand that command. Try 'help' for available commands."
                    success = False
                    
            # Update UI in main thread
            self.root.after(0, self._update_ui_after_command, response, success)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.root.after(0, self._update_ui_after_command, error_msg, False)
            
    def _update_ui_after_command(self, response, success):
        """Update UI after command execution"""
        self.add_chat_message("🤖 Shadow AI", response)
        self.add_activity_log(f"Result: {'Success' if success else 'Failed'}")
        
        # Update status
        if success:
            self.update_status("🟢 Ready", "#00ff00")
        else:
            self.update_status("🔴 Error", "#ff0000")
            
    def generate_simple_article(self, topic):
        """Generate a simple article for topics"""
        return f"""Article: {topic.title()}
{'='*50}

Introduction
------------
This article explores the fascinating topic of {topic}.

Key Points
----------
• {topic.title()} is an important subject in today's world
• Understanding {topic} helps us make better decisions
• Research in {topic} continues to evolve rapidly

Current Applications
-------------------
{topic.title()} has many practical applications:
- Technology and innovation
- Business and industry
- Education and research
- Social and cultural impact

Future Prospects
---------------
The future of {topic} looks promising with:
- Continued research and development
- New technologies and methodologies
- Increasing adoption across sectors
- Enhanced understanding and applications

Conclusion
----------
{topic.title()} remains a crucial area of study and application.
As we continue to explore and understand {topic}, we can expect
significant advances that will benefit society as a whole.

---
Generated by Shadow AI
Date: {time.strftime('%B %d, %Y')}
"""

    # Quick action methods
    def open_notepad(self):
        self._execute_quick_action("open notepad")
        
    def write_ai_article(self):
        self._execute_quick_action("write an article about artificial intelligence")
        
    def take_screenshot(self):
        self._execute_quick_action("take a screenshot")
        
    def open_calculator(self):
        self._execute_quick_action("open calculator")
        
    def open_browser(self):
        self._execute_quick_action("open chrome")
        
    def open_explorer(self):
        self._execute_quick_action("open explorer")
        
    def _execute_quick_action(self, command):
        """Execute quick action command"""
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, command)
        self.process_command()
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = ModernShadowAI()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Shadow AI GUI: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
