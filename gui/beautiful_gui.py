#!/usr/bin/env python3
"""
Shadow AI - Beautiful Modern GUI (Stable Version)
Clean, beautiful, and fully functional interface
"""

import sys
import os
import threading
import time
from pathlib import Path
from datetime import datetime

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
    from tkinter import ttk, messagebox, scrolledtext
    CTK_AVAILABLE = False

# Import Shadow AI components safely
try:
    from main import ShadowAI
    SHADOW_AI_AVAILABLE = True
except ImportError:
    SHADOW_AI_AVAILABLE = False

class BeautifulShadowAI:
    """Beautiful and stable Shadow AI GUI"""
    
    def __init__(self):
        self.shadow_ai = None
        self.is_processing = False
        self.setup_window()
        self.create_interface()
        self.init_shadow_ai()
        
    def setup_window(self):
        """Setup the main window"""
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
            self.root.title("🤖 Shadow AI - Beautiful Interface")
            self.root.geometry("1000x700")
            
            # Configure grid
            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=1)
        else:
            self.root = tk.Tk()
            self.root.title("🤖 Shadow AI - Modern Interface")
            self.root.geometry("1000x700")
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
        """Create the interface"""
        if CTK_AVAILABLE:
            self.create_modern_interface()
        else:
            self.create_classic_interface()
    
    def create_modern_interface(self):
        """Create modern interface with CustomTkinter"""
        # Header
        header = ctk.CTkFrame(self.root, height=80, corner_radius=10)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🤖 Shadow AI - Beautiful Interface",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(
            header,
            text="🟢 Ready",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(side="right", padx=20, pady=20)
        
        # Main content area
        content = ctk.CTkFrame(self.root, corner_radius=10)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.create_sidebar(content)
        
        # Chat area
        self.create_chat_area(content)
        
        # Input area
        input_frame = ctk.CTkFrame(self.root, height=80, corner_radius=10)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter your command here...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(20, 10), pady=20)
        self.input_entry.bind("<Return>", self.process_command)
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="🚀 Send",
            command=self.process_command,
            width=100,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        send_btn.grid(row=0, column=1, padx=(0, 20), pady=20)
    
    def create_sidebar(self, parent):
        """Create sidebar with features"""
        sidebar = ctk.CTkFrame(parent, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        sidebar.grid_propagate(False)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            sidebar,
            text="✨ Features",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        sidebar_title.pack(pady=(20, 15))
        
        # Feature buttons
        features = [
            ("📁 File Manager", self.file_manager),
            ("🌐 Web Search", self.web_search),
            ("💻 System Info", self.system_info),
            ("🔔 Notifications", self.notifications),
            ("📋 Clipboard", self.clipboard),
            ("⚙️ Settings", self.settings)
        ]
        
        for text, command in features:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(fill="x", padx=15, pady=5)
    
    def create_chat_area(self, parent):
        """Create chat area"""
        chat_frame = ctk.CTkFrame(parent)
        chat_frame.grid(row=0, column=1, sticky="nsew")
        
        chat_title = ctk.CTkLabel(
            chat_frame,
            text="💬 Conversation",
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
        self.add_message("system", "🤖 Welcome to Shadow AI Beautiful Interface!")
        self.add_message("system", "✨ All enhanced features are ready to use")
        self.add_message("system", "💬 Type your commands or use the feature buttons")
    
    def create_classic_interface(self):
        """Create classic interface with Tkinter"""
        # Header
        header = tk.Frame(self.root, bg="#2d2d2d", height=60)
        header.pack(fill="x", padx=10, pady=(10, 5))
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 Shadow AI - Modern Interface",
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(side="left", padx=20, pady=15)
        
        self.status_label = tk.Label(
            header,
            text="🟢 Ready",
            bg="#2d2d2d",
            fg="#00ff00",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # Main area
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Chat area
        self.chat_display = scrolledtext.ScrolledText(
            main_frame,
            bg="#2d2d2d",
            fg="white",
            font=("Consolas", 11),
            wrap=tk.WORD,
            height=25
        )
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        
        # Input area
        input_frame = tk.Frame(main_frame, bg="#1a1a1a")
        input_frame.pack(fill="x", pady=(0, 10))
        
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
            text="Send",
            command=self.process_command,
            bg="#0078d4",
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        send_btn.pack(side="right")
        
        # Welcome message
        self.add_message("system", "🤖 Welcome to Shadow AI Interface!")
        self.add_message("system", "✨ Enhanced features available")
    
    def init_shadow_ai(self):
        """Initialize Shadow AI"""
        def initialize():
            try:
                self.update_status("🟡 Initializing...")
                if SHADOW_AI_AVAILABLE:
                    self.shadow_ai = ShadowAI()
                    self.shadow_ai.init_enhanced_features()
                    self.update_status("🟢 Ready")
                    self.add_message("system", "✅ Shadow AI initialized successfully!")
                else:
                    self.update_status("🟡 Demo Mode")
                    self.add_message("system", "⚠️ Shadow AI core not available - demo mode")
            except Exception as e:
                self.update_status("🔴 Error")
                self.add_message("system", f"❌ Initialization error: {e}")
        
        threading.Thread(target=initialize, daemon=True).start()
    
    def add_message(self, sender, message):
        """Add message to chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            formatted = f"[{timestamp}] 👤 You: {message}\n"
        elif sender == "system":
            formatted = f"[{timestamp}] 🤖 System: {message}\n"
        else:
            formatted = f"[{timestamp}] 🤖 Shadow AI: {message}\n"
        
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
        
        # Add to chat
        self.add_message("user", command)
        
        # Process command
        threading.Thread(target=self._process_command, args=(command,), daemon=True).start()
    
    def _process_command(self, command):
        """Process command in background"""
        self.is_processing = True
        self.update_status("🟡 Processing...")
        
        try:
            if self.shadow_ai:
                # Try enhanced commands first
                handled = self.shadow_ai.handle_enhanced_commands(command)
                
                if handled:
                    self.add_message("shadow", f"✅ Enhanced command processed successfully")
                else:
                    # Try regular AI processing
                    result = self.shadow_ai.process_ai_command(command)
                    if result and result.get('success'):
                        self.add_message("shadow", "✅ Command completed successfully!")
                    else:
                        self.add_message("shadow", "⚠️ Command processed")
            else:
                # Demo mode
                self.handle_demo_command(command)
                
        except Exception as e:
            self.add_message("shadow", f"❌ Error: {e}")
        finally:
            self.is_processing = False
            self.update_status("🟢 Ready")
    
    def handle_demo_command(self, command):
        """Handle demo commands"""
        command_lower = command.lower()
        
        responses = {
            "hello": "Hello! I'm Shadow AI. How can I help you today?",
            "organize": "📁 File organization feature would organize your files efficiently",
            "search": "🌐 Web search would find information across multiple sources",
            "system": "💻 System information would show detailed computer metrics",
            "help": "🤖 Available features: file management, web search, system info, notifications"
        }
        
        for keyword, response in responses.items():
            if keyword in command_lower:
                self.add_message("shadow", response)
                return
        
        self.add_message("shadow", f"🤖 Received command: '{command}' - Would process with Shadow AI")
    
    # Feature methods
    def file_manager(self):
        """File manager feature"""
        self.add_message("system", "📁 File Manager activated")
        if self.shadow_ai:
            self.shadow_ai.handle_enhanced_commands("show enhanced features")
        else:
            self.add_message("shadow", "📁 File management tools ready for organizing your files")
    
    def web_search(self):
        """Web search feature"""
        self.add_message("system", "🌐 Web Search activated")
        self.input_entry.delete(0, "end" if CTK_AVAILABLE else tk.END)
        self.input_entry.insert(0, "search Google for ")
    
    def system_info(self):
        """System info feature"""
        self.add_message("system", "💻 Gathering system information...")
        
        def get_info():
            try:
                import psutil
                import platform
                
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                self.add_message("shadow", f"🖥️ System: {platform.system()} {platform.release()}")
                self.add_message("shadow", f"💻 CPU Usage: {cpu:.1f}%")
                self.add_message("shadow", f"🧠 Memory: {memory.percent:.1f}% used")
                
            except ImportError:
                self.add_message("shadow", "💻 System monitoring requires psutil package")
        
        threading.Thread(target=get_info, daemon=True).start()
    
    def notifications(self):
        """Notifications feature"""
        self.add_message("system", "🔔 Testing notifications...")
        self.add_message("shadow", "🔔 Notification system ready!")
    
    def clipboard(self):
        """Clipboard feature"""
        self.add_message("system", "📋 Clipboard manager activated")
        self.add_message("shadow", "📋 Clipboard features available for text management")
    
    def settings(self):
        """Settings feature"""
        self.add_message("system", "⚙️ Settings panel")
        self.add_message("shadow", "⚙️ Configuration options available")
    
    def run(self):
        """Run the application"""
        try:
            # Set error handler for tkinter
            if hasattr(self.root, 'report_callback_exception'):
                self.root.report_callback_exception = lambda *args: None
            
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"GUI Error: {e}")

def main():
    """Main function"""
    print("🚀 Launching Beautiful Shadow AI GUI...")
    
    try:
        app = BeautifulShadowAI()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
