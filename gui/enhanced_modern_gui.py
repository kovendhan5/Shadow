#!/usr/bin/env python3
"""
Shadow AI - Enhanced Modern GUI Interface
Advanced desktop AI assistant with beautiful design and comprehensive functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

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

class EnhancedModernShadowAI:
    """Enhanced Modern Shadow AI GUI with comprehensive functionality"""
    
    def __init__(self):
        self.setup_appearance()
        self.create_main_window()
        self.create_widgets()
        self.status_messages = []
        self.command_history = []
        self.current_task = None
        
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
            self.root.title("Shadow AI - Enhanced Desktop Assistant")
            self.root.geometry("1400x900")
            self.root.minsize(1000, 700)
            
        else:
            self.root = tk.Tk()
            self.root.title("Shadow AI - Enhanced Desktop Assistant")
            self.root.geometry("1400x900")
            self.root.minsize(1000, 700)
            self.root.configure(bg="#1a1a1a")
            
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Center window on screen
        self.center_window()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
    def create_widgets(self):
        """Create all GUI widgets with modern design"""
        # Main container
        if self.use_ctk:
            main_frame = ctk.CTkFrame(self.root)
        else:
            main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
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
            header_frame = ctk.CTkFrame(parent, height=100)
            header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
            header_frame.grid_propagate(False)
            
            # Title section
            title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
            
            title_label = ctk.CTkLabel(
                title_frame, 
                text="🤖 SHADOW AI", 
                font=ctk.CTkFont(size=32, weight="bold")
            )
            title_label.grid(row=0, column=0, sticky="w")
            
            subtitle_label = ctk.CTkLabel(
                title_frame,
                text="Enhanced Desktop AI Assistant",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            subtitle_label.grid(row=1, column=0, sticky="w")
            
            # Status section
            status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            status_frame.grid(row=0, column=2, sticky="e", padx=20, pady=15)
            
            self.status_label = ctk.CTkLabel(
                status_frame,
                text="🟢 Ready",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#00ff00"
            )
            self.status_label.grid(row=0, column=0, sticky="e")
            
            # System info
            system_info = f"Enhanced: {'✅' if ENHANCED_DESKTOP else '❌'} | AI: {'✅' if AI_AVAILABLE else '❌'}"
            self.system_info_label = ctk.CTkLabel(
                status_frame,
                text=system_info,
                font=ctk.CTkFont(size=12),
                text_color="#666666"
            )
            self.system_info_label.grid(row=1, column=0, sticky="e")
            
        else:
            header_frame = tk.Frame(parent, bg="#2d2d2d", relief="raised", bd=2)
            header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 15))
            
            # Title
            title_label = tk.Label(
                header_frame,
                text="🤖 SHADOW AI - Enhanced",
                font=("Arial", 32, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
            title_label.grid(row=0, column=0, padx=20, pady=15)
            
            # Status indicator
            self.status_label = tk.Label(
                header_frame,
                text="🟢 Ready",
                font=("Arial", 14),
                bg="#2d2d2d",
                fg="#00ff00"
            )
            self.status_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
            
    def create_content_area(self, parent):
        """Create main content area with enhanced layout"""
        # Left sidebar
        self.create_sidebar(parent)
        
        # Main content with tabs
        self.create_main_content(parent)
        
        # Right panel
        self.create_right_panel(parent)
        
    def create_sidebar(self, parent):
        """Create enhanced left sidebar with quick actions"""
        if self.use_ctk:
            sidebar = ctk.CTkFrame(parent, width=250)
            sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 15))
            sidebar.grid_propagate(False)
            
            # Quick Actions Header
            quick_label = ctk.CTkLabel(
                sidebar, 
                text="🚀 Quick Actions", 
                font=ctk.CTkFont(size=18, weight="bold")
            )
            quick_label.grid(row=0, column=0, padx=20, pady=(20, 15))
            
            # Enhanced Action buttons
            actions = [
                ("📝 Open Notepad", self.open_notepad, "#3498db"),
                ("📄 Write AI Article", self.write_ai_article, "#2ecc71"),
                ("🧠 Write ASI Article", self.write_asi_article, "#9b59b6"),
                ("💾 Save Article", self.save_current_article, "#e67e22"),
                ("📸 Take Screenshot", self.take_screenshot, "#34495e"),
                ("🗂️ Open File Manager", self.open_file_manager, "#16a085"),
                ("⚙️ System Settings", self.open_settings, "#95a5a6"),
                ("🧪 Run Demo", self.run_demo, "#f39c12")
            ]
            
            for i, (text, command, color) in enumerate(actions):
                btn = ctk.CTkButton(
                    sidebar,
                    text=text,
                    command=command,
                    width=200,
                    height=35,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=color,
                    hover_color=self.darken_color(color)
                )
                btn.grid(row=i+1, column=0, padx=20, pady=5)
                
        else:
            sidebar = tk.Frame(parent, bg="#2d2d2d", width=250)
            sidebar.grid(row=1, column=0, sticky="nsw", padx=(0, 15))
            sidebar.grid_propagate(False)
            
            # Quick Actions
            quick_label = tk.Label(
                sidebar, 
                text="🚀 Quick Actions", 
                font=("Arial", 16, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
            quick_label.grid(row=0, column=0, padx=20, pady=(20, 15))
            
    def create_main_content(self, parent):
        """Create enhanced main content area with tabs"""
        if self.use_ctk:
            # Create tabview
            self.tabview = ctk.CTkTabview(parent)
            self.tabview.grid(row=1, column=1, sticky="nsew", padx=(0, 15))
            
            # Chat Tab
            self.create_chat_tab()
            
            # Commands Tab
            self.create_commands_tab()
            
            # Articles Tab  
            self.create_articles_tab()
            
            # Settings Tab
            self.create_settings_tab()
            
        else:
            # Fallback for regular tkinter
            self.notebook = ttk.Notebook(parent)
            self.notebook.grid(row=1, column=1, sticky="nsew", padx=(0, 15))
            
    def create_chat_tab(self):
        """Create enhanced chat interface tab"""
        chat_tab = self.tabview.add("💬 Chat")
        chat_tab.grid_columnconfigure(0, weight=1)
        chat_tab.grid_rowconfigure(0, weight=1)
        
        # Chat display area
        if self.use_ctk:
            self.chat_display = ctk.CTkTextbox(
                chat_tab,
                font=ctk.CTkFont(size=12),
                wrap="word"
            )
        else:
            self.chat_display = scrolledtext.ScrolledText(
                chat_tab,
                font=("Consolas", 12),
                wrap="word",
                bg="#1a1a1a",
                fg="#ffffff"
            )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 10))
        
        # Input frame
        if self.use_ctk:
            input_frame = ctk.CTkFrame(chat_tab, fg_color="transparent")
        else:
            input_frame = tk.Frame(chat_tab, bg="#2d2d2d")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 15))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Command input
        if self.use_ctk:
            self.command_input = ctk.CTkEntry(
                input_frame,
                placeholder_text="Enter your command here...",
                font=ctk.CTkFont(size=12),
                height=40
            )
        else:
            self.command_input = tk.Entry(
                input_frame,
                font=("Arial", 12),
                bg="#3d3d3d",
                fg="#ffffff",
                insertbackground="#ffffff"
            )
        self.command_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.command_input.bind("<Return>", self.execute_command)
        
        # Send button
        if self.use_ctk:
            send_btn = ctk.CTkButton(
                input_frame,
                text="Send 🚀",
                command=self.execute_command,
                width=100,
                height=40,
                font=ctk.CTkFont(size=12, weight="bold")
            )
        else:
            send_btn = tk.Button(
                input_frame,
                text="Send 🚀",
                command=self.execute_command,
                bg="#3498db",
                fg="#ffffff",
                font=("Arial", 12, "bold")
            )
        send_btn.grid(row=0, column=1)
        
        # Initial welcome message
        self.add_chat_message("🤖 Shadow AI", "Welcome! I'm your enhanced desktop assistant. I can write articles, control applications, and help with various tasks. Try commands like:\n\n• 'write an article about AI'\n• 'write an article about ASI and save it as ASI.txt'\n• 'open notepad'\n• 'take a screenshot'\n\nWhat can I help you with today?", "assistant")
        
    def create_commands_tab(self):
        """Create commands reference tab"""
        commands_tab = self.tabview.add("📋 Commands")
        commands_tab.grid_columnconfigure(0, weight=1)
        commands_tab.grid_rowconfigure(0, weight=1)
        
        if self.use_ctk:
            commands_text = ctk.CTkTextbox(
                commands_tab,
                font=ctk.CTkFont(size=11, family="Consolas")
            )
        else:
            commands_text = scrolledtext.ScrolledText(
                commands_tab,
                font=("Consolas", 11),
                bg="#1a1a1a",
                fg="#ffffff"
            )
        commands_text.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # Add comprehensive command reference
        command_reference = """
SHADOW AI - ENHANCED COMMAND REFERENCE
=====================================

🖥️  DESKTOP AUTOMATION:
────────────────────────
• open notepad                     - Open Notepad application
• open notepad and write [text]    - Open Notepad and type text
• open [app name]                  - Open any application
• take a screenshot                - Capture screen
• type: [your text]                - Type specific text
• click at [x,y]                   - Click at coordinates

🎯 ARTICLE GENERATION:
──────────────────────
• write an article about ai        - Comprehensive AI article
• write an article about asi       - Artificial Super Intelligence
• write an article about ml        - Machine Learning article
• write an article about tech      - Technology overview
• [topic] and save it as [file]    - Write and save with filename

💾 FILE OPERATIONS:
──────────────────
• save current article             - Save the currently open article
• open file manager                - Open Windows File Explorer
• create folder [name]             - Create a new folder

🔧 SYSTEM COMMANDS:
──────────────────
• help                            - Show command help
• status                          - Show system status
• demo                            - Run demonstration
• clear                           - Clear chat/screen
• quit / exit                     - Exit Shadow AI

💡 EXAMPLE COMMANDS:
───────────────────
Shadow AI > open notepad and write hello world
Shadow AI > write an article about artificial intelligence
Shadow AI > write an article about ASI and save it as ASI.txt
Shadow AI > take a screenshot
Shadow AI > open calculator
Shadow AI > type: This is automated typing

🚀 ENHANCED FEATURES:
────────────────────
• Smart command recognition
• Article templates for AI, ASI, ML, Technology
• Automatic file saving with custom names
• Screenshot management
• Application launcher
• Real-time status monitoring

⚙️ SYSTEM STATUS:
────────────────
Enhanced Desktop: """ + ("✅ Available" if ENHANCED_DESKTOP else "❌ Not Available") + """
AI Processing: """ + ("✅ Available" if AI_AVAILABLE else "❌ Not Available") + """
CustomTkinter: """ + ("✅ Available" if CTK_AVAILABLE else "❌ Not Available") + """

For more information, visit the Settings tab or check the documentation.
        """
        
        commands_text.insert("1.0", command_reference)
        if hasattr(commands_text, 'configure'):
            commands_text.configure(state="disabled")
        
    def create_articles_tab(self):
        """Create articles management tab"""
        articles_tab = self.tabview.add("📚 Articles")
        articles_tab.grid_columnconfigure(0, weight=1)
        articles_tab.grid_rowconfigure(1, weight=1)
        
        # Header
        if self.use_ctk:
            header_label = ctk.CTkLabel(
                articles_tab,
                text="📚 Article Generation & Management",
                font=ctk.CTkFont(size=20, weight="bold")
            )
        else:
            header_label = tk.Label(
                articles_tab,
                text="📚 Article Generation & Management",
                font=("Arial", 20, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
        header_label.grid(row=0, column=0, pady=(15, 20))
        
        # Article options frame
        if self.use_ctk:
            options_frame = ctk.CTkFrame(articles_tab)
        else:
            options_frame = tk.Frame(articles_tab, bg="#2d2d2d")
        options_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        options_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Article types
        article_types = [
            ("🤖 Artificial Intelligence", "ai", "Comprehensive overview of AI"),
            ("🧠 Artificial Super Intelligence", "asi", "Future of superintelligent systems"),
            ("🔬 Machine Learning", "ml", "Deep dive into ML concepts"),
            ("💻 Technology Overview", "tech", "Current technology trends"),
            ("🎯 Custom Topic", "custom", "Write about any topic")
        ]
        
        for i, (title, topic, description) in enumerate(article_types):
            if self.use_ctk:
                article_frame = ctk.CTkFrame(options_frame)
                article_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
                
                title_label = ctk.CTkLabel(
                    article_frame,
                    text=title,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                title_label.grid(row=0, column=0, padx=15, pady=(15, 5))
                
                desc_label = ctk.CTkLabel(
                    article_frame,
                    text=description,
                    font=ctk.CTkFont(size=11),
                    text_color="#888888"
                )
                desc_label.grid(row=1, column=0, padx=15, pady=(0, 10))
                
                generate_btn = ctk.CTkButton(
                    article_frame,
                    text="Generate Article",
                    command=lambda t=topic: self.generate_article_by_type(t),
                    width=150
                )
                generate_btn.grid(row=2, column=0, padx=15, pady=(0, 15))
        
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_tab = self.tabview.add("⚙️ Settings")
        settings_tab.grid_columnconfigure(0, weight=1)
        settings_tab.grid_rowconfigure(1, weight=1)
        
        # Settings content
        if self.use_ctk:
            settings_frame = ctk.CTkScrollableFrame(settings_tab)
        else:
            settings_frame = tk.Frame(settings_tab, bg="#2d2d2d")
        settings_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        # System Information
        if self.use_ctk:
            info_label = ctk.CTkLabel(
                settings_frame,
                text="🔧 System Information",
                font=ctk.CTkFont(size=18, weight="bold")
            )
        else:
            info_label = tk.Label(
                settings_frame,
                text="🔧 System Information",
                font=("Arial", 18, "bold"),
                bg="#2d2d2d",
                fg="#ffffff"
            )
        info_label.grid(row=0, column=0, sticky="w", pady=(0, 15))
        
        # Status indicators
        status_info = [
            ("Enhanced Desktop Controller", "✅ Available" if ENHANCED_DESKTOP else "❌ Not Available"),
            ("AI Processing", "✅ Available" if AI_AVAILABLE else "❌ Not Available"),
            ("CustomTkinter UI", "✅ Available" if CTK_AVAILABLE else "❌ Not Available"),
            ("Desktop Controller", "✅ Available" if enhanced_controller else "❌ Not Available")
        ]
        
        for i, (feature, status) in enumerate(status_info):
            if self.use_ctk:
                feature_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
                feature_frame.grid(row=i+1, column=0, sticky="ew", pady=2)
                
                ctk.CTkLabel(
                    feature_frame,
                    text=feature + ":",
                    font=ctk.CTkFont(size=12, weight="bold")
                ).grid(row=0, column=0, sticky="w")
                
                ctk.CTkLabel(
                    feature_frame,
                    text=status,
                    font=ctk.CTkFont(size=12),
                    text_color="#00ff00" if "✅" in status else "#ff0000"
                ).grid(row=0, column=1, sticky="w", padx=(10, 0))
                
    def create_right_panel(self, parent):
        """Create right panel with activity log"""
        if self.use_ctk:
            right_panel = ctk.CTkFrame(parent, width=300)
            right_panel.grid(row=1, column=2, sticky="nsew")
            right_panel.grid_propagate(False)
            
            # Activity log
            activity_label = ctk.CTkLabel(
                right_panel,
                text="📊 Activity Log",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            activity_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            
            self.activity_log = ctk.CTkTextbox(
                right_panel,
                font=ctk.CTkFont(size=10, family="Consolas"),
                wrap="word"
            )
            self.activity_log.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
            right_panel.grid_rowconfigure(1, weight=1)
            
        else:
            right_panel = tk.Frame(parent, bg="#2d2d2d", width=300)
            right_panel.grid(row=1, column=2, sticky="nsew")
            right_panel.grid_propagate(False)
            
        # Add initial activity
        self.log_activity("System started", "info")
        self.log_activity(f"Enhanced Desktop: {'Available' if ENHANCED_DESKTOP else 'Not Available'}", 
                          "success" if ENHANCED_DESKTOP else "warning")
        
    def create_footer(self, parent):
        """Create footer with status information"""
        if self.use_ctk:
            footer = ctk.CTkFrame(parent, height=50)
            footer.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(15, 0))
            footer.grid_propagate(False)
            
            # Status text
            self.footer_status = ctk.CTkLabel(
                footer,
                text="Ready to assist you!",
                font=ctk.CTkFont(size=12)
            )
            self.footer_status.grid(row=0, column=0, padx=20, pady=15)
            
            # Version info
            version_label = ctk.CTkLabel(
                footer,
                text="Shadow AI v2.0 Enhanced",
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            )
            version_label.grid(row=0, column=2, padx=20, pady=15, sticky="e")
        
    # Enhanced Action Methods
    def open_notepad(self):
        """Open Notepad application"""
        self.log_activity("Opening Notepad...", "info")
        try:
            if enhanced_controller:
                success = enhanced_controller.open_notepad()
                if success:
                    self.add_chat_message("🤖 Shadow AI", "✅ Notepad opened successfully!", "assistant")
                    self.log_activity("Notepad opened successfully", "success")
                else:
                    self.add_chat_message("🤖 Shadow AI", "❌ Failed to open Notepad", "assistant")
                    self.log_activity("Failed to open Notepad", "error")
            else:
                # Fallback
                subprocess.run(["notepad.exe"], check=False)
                self.add_chat_message("🤖 Shadow AI", "✅ Notepad opened (fallback method)", "assistant")
                self.log_activity("Notepad opened (fallback)", "success")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error opening Notepad: {e}", "assistant")
            self.log_activity(f"Error opening Notepad: {e}", "error")
            
    def write_ai_article(self):
        """Write an AI article"""
        self.log_activity("Writing AI article...", "info")
        try:
            if enhanced_controller and hasattr(enhanced_controller, 'open_notepad_and_write_article'):
                success = enhanced_controller.open_notepad_and_write_article("ai")
                if success:
                    self.add_chat_message("🤖 Shadow AI", "✅ AI article written successfully!", "assistant")
                    self.log_activity("AI article written successfully", "success")
                else:
                    self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                    self.log_activity("Enhanced desktop controller not available", "error")
            else:
                self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                self.log_activity("Enhanced desktop controller not available", "error")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error writing article: {e}", "assistant")
            self.log_activity(f"Error writing article: {e}", "error")
            
    def write_asi_article(self):
        """Write an ASI article"""
        self.log_activity("Writing ASI article...", "info")
        try:
            if enhanced_controller and hasattr(enhanced_controller, 'open_notepad_and_write_article'):
                success = enhanced_controller.open_notepad_and_write_article("asi")
                if success:
                    self.add_chat_message("🤖 Shadow AI", "✅ ASI article written successfully!", "assistant")
                    self.log_activity("ASI article written successfully", "success")
                else:
                    self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                    self.log_activity("Enhanced desktop controller not available", "error")
            else:
                self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                self.log_activity("Enhanced desktop controller not available", "error")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error writing ASI article: {e}", "assistant")
            self.log_activity(f"Error writing ASI article: {e}", "error")
            
    def save_current_article(self):
        """Save the currently open article"""
        self.log_activity("Attempting to save current article...", "info")
        try:
            if enhanced_controller:
                # Send Ctrl+S to save
                enhanced_controller.key_combination(['ctrl', 's'])
                self.add_chat_message("🤖 Shadow AI", "💾 Save dialog opened. Please specify filename.", "assistant")
                self.log_activity("Save dialog opened", "success")
            else:
                self.add_chat_message("🤖 Shadow AI", "❌ Desktop controller not available", "assistant")
                self.log_activity("Desktop controller not available", "error")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error saving: {e}", "assistant")
            self.log_activity(f"Error saving: {e}", "error")
            
    def take_screenshot(self):
        """Take a screenshot"""
        self.log_activity("Taking screenshot...", "info")
        try:
            if enhanced_controller:
                screenshot_path = enhanced_controller.take_screenshot()
                if screenshot_path:
                    self.add_chat_message("🤖 Shadow AI", f"📸 Screenshot saved: {screenshot_path}", "assistant")
                    self.log_activity(f"Screenshot saved: {screenshot_path}", "success")
                else:
                    self.add_chat_message("🤖 Shadow AI", "❌ Failed to take screenshot", "assistant")
                    self.log_activity("Failed to take screenshot", "error")
            else:
                self.add_chat_message("🤖 Shadow AI", "❌ Desktop controller not available", "assistant")
                self.log_activity("Desktop controller not available", "error")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error taking screenshot: {e}", "assistant")
            self.log_activity(f"Error taking screenshot: {e}", "error")
            
    def open_file_manager(self):
        """Open Windows File Manager"""
        self.log_activity("Opening File Manager...", "info")
        try:
            subprocess.run(["explorer.exe"], check=False)
            self.add_chat_message("🤖 Shadow AI", "🗂️ File Manager opened", "assistant")
            self.log_activity("File Manager opened", "success")
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error opening File Manager: {e}", "assistant")
            self.log_activity(f"Error opening File Manager: {e}", "error")
            
    def open_settings(self):
        """Switch to settings tab"""
        if hasattr(self, 'tabview'):
            self.tabview.set("⚙️ Settings")
            self.log_activity("Switched to Settings tab", "info")
            
    def run_demo(self):
        """Run a demonstration"""
        self.log_activity("Running demo...", "info")
        self.add_chat_message("🤖 Shadow AI", "🎬 Starting demonstration...", "assistant")
        
        # Run demo in separate thread to avoid blocking UI
        threading.Thread(target=self._demo_thread, daemon=True).start()
        
    def _demo_thread(self):
        """Demo execution thread"""
        demo_steps = [
            ("Taking screenshot...", self.take_screenshot),
            ("Opening Notepad...", self.open_notepad),
            ("Demo completed!", None)
        ]
        
        for step, action in demo_steps:
            self.add_chat_message("🤖 Shadow AI", f"Demo: {step}", "assistant")
            if action:
                action()
            time.sleep(2)
            
    def generate_article_by_type(self, article_type):
        """Generate article by type from Articles tab"""
        if article_type == "custom":
            # Show input dialog for custom topic
            topic = tk.simpledialog.askstring("Custom Topic", "Enter the topic for your article:")
            if topic:
                self.execute_command_text(f"write an article about {topic}")
        else:
            self.execute_command_text(f"write an article about {article_type}")
            
    def execute_command(self, event=None):
        """Execute command from input field"""
        command = self.command_input.get().strip()
        if command:
            self.execute_command_text(command)
            self.command_input.delete(0, 'end')
            
    def execute_command_text(self, command):
        """Execute a text command"""
        self.add_chat_message("You", command, "user")
        self.command_history.append(command)
        self.log_activity(f"Command: {command}", "info")
        
        # Execute in separate thread to avoid blocking UI
        threading.Thread(target=self._execute_command_thread, args=(command,), daemon=True).start()
        
    def _execute_command_thread(self, command):
        """Execute command in separate thread"""
        try:
            command_lower = command.lower()
            
            # Parse commands
            if "write an article about" in command_lower:
                if "save it as" in command_lower:
                    # Parse topic and filename
                    parts = command_lower.split("and save it as")
                    topic = parts[0].split("write an article about")[1].strip()
                    filename = parts[1].strip()
                    
                    self.add_chat_message("🤖 Shadow AI", f"📝 Writing article about {topic} and saving as {filename}...", "assistant")
                    
                    if enhanced_controller and hasattr(enhanced_controller, 'open_notepad_and_write_article_save_as'):
                        success = enhanced_controller.open_notepad_and_write_article_save_as(topic, filename)
                        if success:
                            self.add_chat_message("🤖 Shadow AI", f"✅ Article about {topic} written and saved as {filename}!", "assistant")
                            self.log_activity(f"Article saved as {filename}", "success")
                        else:
                            self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                    else:
                        self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                else:
                    # Just write article
                    topic = command_lower.split("write an article about")[1].strip()
                    self.add_chat_message("🤖 Shadow AI", f"📝 Writing article about {topic}...", "assistant")
                    
                    if enhanced_controller and hasattr(enhanced_controller, 'open_notepad_and_write_article'):
                        success = enhanced_controller.open_notepad_and_write_article(topic)
                        if success:
                            self.add_chat_message("🤖 Shadow AI", f"✅ Article about {topic} written!", "assistant")
                            self.log_activity(f"Article about {topic} written", "success")
                        else:
                            self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                    else:
                        self.add_chat_message("🤖 Shadow AI", "❌ Enhanced desktop controller not available", "assistant")
                        
            elif "open notepad" in command_lower:
                self.open_notepad()
                
            elif "take a screenshot" in command_lower or "screenshot" in command_lower:
                self.take_screenshot()
                
            elif command_lower.startswith("open "):
                app_name = command_lower.split("open ")[1].strip()
                self.add_chat_message("🤖 Shadow AI", f"🚀 Opening {app_name}...", "assistant")
                if enhanced_controller:
                    success = enhanced_controller.open_application(app_name)
                    if success:
                        self.add_chat_message("🤖 Shadow AI", f"✅ {app_name} opened successfully!", "assistant")
                        self.log_activity(f"{app_name} opened", "success")
                    else:
                        self.add_chat_message("🤖 Shadow AI", f"❌ Failed to open {app_name}", "assistant")
                        self.log_activity(f"Failed to open {app_name}", "error")
                else:
                    self.add_chat_message("🤖 Shadow AI", "❌ Desktop controller not available", "assistant")
                    
            else:
                self.add_chat_message("🤖 Shadow AI", "🤔 I'm not sure how to handle that command. Try:\n• 'write an article about AI'\n• 'write an article about ASI and save it as ASI.txt'\n• 'open notepad'\n• 'take a screenshot'", "assistant")
                
        except Exception as e:
            self.add_chat_message("🤖 Shadow AI", f"❌ Error executing command: {e}", "assistant")
            self.log_activity(f"Command error: {e}", "error")
            
    def add_chat_message(self, sender, message, msg_type):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if msg_type == "user":
            formatted_message = f"[{timestamp}] 👤 {sender}: {message}\n\n"
        else:
            formatted_message = f"[{timestamp}] {message}\n\n"
            
        self.chat_display.insert("end", formatted_message)
        self.chat_display.see("end")
        
    def log_activity(self, message, level="info"):
        """Log activity to the activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "success":
            icon = "✅"
        elif level == "error":
            icon = "❌"
        elif level == "warning":
            icon = "⚠️"
        else:
            icon = "ℹ️"
            
        log_message = f"[{timestamp}] {icon} {message}\n"
        
        if hasattr(self, 'activity_log'):
            self.activity_log.insert("end", log_message)
            self.activity_log.see("end")
            
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        # Simple color darkening
        color_map = {
            "#3498db": "#2980b9",
            "#2ecc71": "#27ae60", 
            "#9b59b6": "#8e44ad",
            "#e67e22": "#d35400",
            "#34495e": "#2c3e50",
            "#16a085": "#138d75",
            "#95a5a6": "#7f8c8d",
            "#f39c12": "#e67e22"
        }
        return color_map.get(color, color)
        
    def on_closing(self):
        """Handle window closing"""
        self.log_activity("Shutting down Shadow AI...", "info")
        self.root.destroy()
        
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = EnhancedModernShadowAI()
        app.run()
    except Exception as e:
        print(f"Error starting Enhanced Shadow AI GUI: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
