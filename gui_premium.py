#!/usr/bin/env python3
"""
Shadow AI - Premium Modern GUI
A beautiful, animated, and professional AI assistant interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import logging
from datetime import datetime
import sys
import os
import json
from typing import Optional, Dict, Any

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import ShadowAI
    from config import VOICE_ENABLED
except ImportError as e:
    logging.error(f"Import error: {e}")
    ShadowAI = None
    VOICE_ENABLED = False

class AnimatedButton(tk.Button):
    """Custom animated button with hover effects"""
    
    def __init__(self, parent, **kwargs):
        self.hover_color = kwargs.pop('hover_color', '#4A90E2')
        self.original_color = kwargs.get('bg', '#3498DB')
        self.text_color = kwargs.get('fg', 'white')
        self.hover_text_color = kwargs.pop('hover_text_color', 'white')
        
        super().__init__(parent, **kwargs)
        
        # Bind hover events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
        # Configure relief and border
        self.configure(
            relief='flat',
            borderwidth=0,
            cursor='hand2'
        )
    
    def on_enter(self, event):
        """Handle mouse enter event"""
        self.configure(bg=self.hover_color, fg=self.hover_text_color)
        
    def on_leave(self, event):
        """Handle mouse leave event"""
        self.configure(bg=self.original_color, fg=self.text_color)
        
    def on_click(self, event):
        """Handle click animation"""
        # Brief color change on click
        original_bg = self.cget('bg')
        self.configure(bg='#2980B9')
        self.after(100, lambda: self.configure(bg=original_bg))

class StatusIndicator(tk.Frame):
    """Animated status indicator with pulsing effect"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.canvas = tk.Canvas(self, width=20, height=20, highlightthickness=0)
        self.canvas.pack()
        
        self.status = 'idle'  # idle, processing, success, error
        self.animation_running = False
        
        self.colors = {
            'idle': '#95A5A6',
            'processing': '#3498DB',
            'success': '#27AE60',
            'error': '#E74C3C'
        }
        
        self.draw_indicator()
    
    def draw_indicator(self):
        """Draw the status indicator"""
        self.canvas.delete("all")
        color = self.colors.get(self.status, '#95A5A6')
        
        # Draw circle
        self.canvas.create_oval(2, 2, 18, 18, fill=color, outline='')
        
        if self.status == 'processing' and not self.animation_running:
            self.start_pulse_animation()
    
    def set_status(self, status: str):
        """Set the status and update indicator"""
        self.status = status
        self.draw_indicator()
    
    def start_pulse_animation(self):
        """Start pulsing animation for processing status"""
        if self.animation_running:
            return
            
        self.animation_running = True
        self.pulse_step(0)
    
    def pulse_step(self, step):
        """Single step of pulse animation"""
        if self.status != 'processing':
            self.animation_running = False
            return
        
        # Calculate alpha for pulsing effect
        alpha = (step % 60) / 60.0
        if alpha > 0.5:
            alpha = 1.0 - alpha
        
        # Redraw with varying intensity
        self.canvas.delete("all")
        intensity = int(255 * (0.3 + 0.7 * alpha))
        color = f"#{intensity:02x}{intensity:02x}{255:02x}"
        
        self.canvas.create_oval(2, 2, 18, 18, fill=color, outline='')
        
        # Continue animation
        if self.animation_running:
            self.after(50, lambda: self.pulse_step(step + 1))

class ModernCard(tk.Frame):
    """Modern card component with shadow effect"""
    
    def __init__(self, parent, title="", **kwargs):
        # Extract card-specific options
        shadow_color = kwargs.pop('shadow_color', '#E8E8E8')
        card_bg = kwargs.pop('card_bg', 'white')
        
        super().__init__(parent, bg=shadow_color, **kwargs)
        
        # Create shadow effect
        self.shadow_frame = tk.Frame(self, bg=shadow_color, height=2)
        self.shadow_frame.pack(side='bottom', fill='x')
        
        # Main card content
        self.content_frame = tk.Frame(self, bg=card_bg, relief='flat', bd=1)
        self.content_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Title if provided
        if title:
            self.title_label = tk.Label(
                self.content_frame,
                text=title,
                font=('Segoe UI', 12, 'bold'),
                bg=card_bg,
                fg='#2C3E50'
            )
            self.title_label.pack(pady=(10, 5))
    
    def add_widget(self, widget_class, **kwargs):
        """Add a widget to the card content"""
        widget = widget_class(self.content_frame, **kwargs)
        widget.pack(pady=5, padx=10, fill='x')
        return widget

class ShadowAIPremiumGUI:
    """Premium Shadow AI GUI with modern design and animations"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.shadow_ai = None
        self.voice_available = False
        self.setup_window()
        self.create_widgets()
        self.setup_shadow_ai()
        self.start_status_updates()
    
    def setup_window(self):
        """Configure the main window with modern styling"""
        self.window.title("Shadow AI - Premium Assistant")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 700)
        
        # Set window icon and properties
        try:
            self.window.iconbitmap("icon.ico")
        except:
            pass
        
        # Modern color scheme
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#34495E',
            'accent': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'light': '#ECF0F1',
            'dark': '#2C3E50',
            'background': '#F8F9FA',
            'card': '#FFFFFF',
            'text': '#2C3E50',
            'text_light': '#7F8C8D'
        }
        
        # Configure window background
        self.window.configure(bg=self.colors['background'])
        
        # Configure ttk styles
        self.setup_styles()
    
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        
        # Configure notebook style
        style.theme_use('clam')
        
        style.configure(
            'Modern.TNotebook',
            background=self.colors['background'],
            borderwidth=0,
            focuscolor='none'
        )
        
        style.configure(
            'Modern.TNotebook.Tab',
            background=self.colors['light'],
            foreground=self.colors['text'],
            padding=[20, 10],
            focuscolor='none'
        )
        
        style.map(
            'Modern.TNotebook.Tab',
            background=[('selected', self.colors['accent'])],
            foreground=[('selected', 'white')]
        )
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Header
        self.create_header()
        
        # Main content area with notebook
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create the header section"""
        header = tk.Frame(self.window, bg=self.colors['primary'], height=80)
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(expand=True, fill='both')
        
        # Main title
        title_label = tk.Label(
            title_frame,
            text="🤖 Shadow AI",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        # Status indicators
        status_frame = tk.Frame(title_frame, bg=self.colors['primary'])
        status_frame.pack(side='right', padx=20, pady=20)
        
        # AI Status
        self.ai_status = StatusIndicator(status_frame, bg=self.colors['primary'])
        self.ai_status.pack(side='right', padx=(0, 10))
        
        ai_status_label = tk.Label(
            status_frame,
            text="AI Status",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        ai_status_label.pack(side='right', padx=(0, 5))
    
    def create_main_content(self):
        """Create the main content area with tabs"""
        # Main container
        main_container = tk.Frame(self.window, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Chat tab
        self.create_chat_tab()
        
        # Commands tab
        self.create_commands_tab()
        
        # Settings tab
        self.create_settings_tab()
        
        # Logs tab
        self.create_logs_tab()
    
    def create_chat_tab(self):
        """Create the main chat interface tab"""
        chat_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(chat_frame, text="💬 Chat")
        
        # Left panel - Chat history
        left_panel = ModernCard(
            chat_frame,
            title="Conversation",
            card_bg=self.colors['card']
        )
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            left_panel.content_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief='flat',
            borderwidth=0,
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Input area
        input_frame = tk.Frame(left_panel.content_frame, bg=self.colors['card'])
        input_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Text input
        self.text_input = tk.Text(
            input_frame,
            height=3,
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text'],
            relief='solid',
            borderwidth=1,
            wrap=tk.WORD
        )
        self.text_input.pack(fill='x', pady=(0, 10))
        self.text_input.bind('<Return>', self.on_enter_pressed)
        self.text_input.bind('<Control-Return>', lambda e: self.text_input.insert('insert', '\n'))
        
        # Input buttons
        button_frame = tk.Frame(input_frame, bg=self.colors['card'])
        button_frame.pack(fill='x')
        
        # Send button
        self.send_btn = AnimatedButton(
            button_frame,
            text="🚀 Send",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            hover_color='#2980B9',
            command=self.send_text_command,
            padx=20,
            pady=8
        )
        self.send_btn.pack(side='right', padx=(5, 0))
        
        # Voice button
        self.voice_btn = AnimatedButton(
            button_frame,
            text="🎤 Voice",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            hover_color='#229954',
            command=self.send_voice_command,
            padx=20,
            pady=8
        )
        self.voice_btn.pack(side='right', padx=(5, 0))
        
        # Clear button
        clear_btn = AnimatedButton(
            button_frame,
            text="🗑️ Clear",
            font=('Segoe UI', 10),
            bg=self.colors['text_light'],
            fg='white',
            hover_color='#6C7B7F',
            command=self.clear_chat,
            padx=15,
            pady=8
        )
        clear_btn.pack(side='left')
        
        # Right panel - Quick actions
        self.create_right_panel(chat_frame)
    
    def create_right_panel(self, parent):
        """Create the right panel with quick actions"""
        right_panel = tk.Frame(parent, bg=self.colors['background'], width=300)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Status card
        status_card = ModernCard(
            right_panel,
            title="System Status",
            card_bg=self.colors['card']
        )
        status_card.pack(fill='x', pady=(0, 10))
        
        # Status items
        self.create_status_items(status_card.content_frame)
        
        # Quick actions card
        actions_card = ModernCard(
            right_panel,
            title="Quick Actions",
            card_bg=self.colors['card']
        )
        actions_card.pack(fill='x', pady=(0, 10))
        
        # Quick action buttons
        self.create_quick_actions(actions_card.content_frame)
        
        # Activity log card
        activity_card = ModernCard(
            right_panel,
            title="Recent Activity",
            card_bg=self.colors['card']
        )
        activity_card.pack(fill='both', expand=True)
        
        # Activity log
        self.activity_log = scrolledtext.ScrolledText(
            activity_card.content_frame,
            height=8,
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_light'],
            relief='flat',
            borderwidth=0,
            state='disabled'
        )
        self.activity_log.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_status_items(self, parent):
        """Create status indicator items"""
        items = [
            ("AI Engine", "ai_engine_status"),
            ("Voice Recognition", "voice_status"),
            ("System Monitor", "system_status")
        ]
        
        for label, attr in items:
            item_frame = tk.Frame(parent, bg=self.colors['card'])
            item_frame.pack(fill='x', padx=10, pady=2)
            
            # Status indicator
            status_indicator = StatusIndicator(item_frame, bg=self.colors['card'])
            status_indicator.pack(side='left', padx=(0, 10))
            setattr(self, attr, status_indicator)
            
            # Label
            tk.Label(
                item_frame,
                text=label,
                font=('Segoe UI', 10),
                bg=self.colors['card'],
                fg=self.colors['text']
            ).pack(side='left')
    
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        actions = [
            ("📝 Open Notepad", self.quick_notepad),
            ("🌐 Open Browser", self.quick_browser),
            ("📊 Take Screenshot", self.quick_screenshot),
            ("🗂️ Open File Explorer", self.quick_explorer),
            ("⚙️ System Info", self.quick_system_info)
        ]
        
        for text, command in actions:
            btn = AnimatedButton(
                parent,
                text=text,
                font=('Segoe UI', 9),
                bg=self.colors['light'],
                fg=self.colors['text'],
                hover_color=self.colors['accent'],
                hover_text_color='white',
                command=command,
                pady=8
            )
            btn.pack(fill='x', padx=10, pady=2)
    
    def create_commands_tab(self):
        """Create the commands reference tab"""
        commands_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(commands_frame, text="📋 Commands")
        
        # Commands list
        commands_card = ModernCard(
            commands_frame,
            title="Available Commands",
            card_bg=self.colors['card']
        )
        commands_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create scrollable commands list
        commands_text = scrolledtext.ScrolledText(
            commands_card.content_frame,
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief='flat',
            borderwidth=0,
            state='disabled'
        )
        commands_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Populate commands
        self.populate_commands_list(commands_text)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings content
        settings_card = ModernCard(
            settings_frame,
            title="Configuration",
            card_bg=self.colors['card']
        )
        settings_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add settings controls here
        tk.Label(
            settings_card.content_frame,
            text="Settings panel coming soon...",
            font=('Segoe UI', 12),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(pady=50)
    
    def create_logs_tab(self):
        """Create the logs tab"""
        logs_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(logs_frame, text="📊 Logs")
        
        # Logs content
        logs_card = ModernCard(
            logs_frame,
            title="System Logs",
            card_bg=self.colors['card']
        )
        logs_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Log display
        self.log_display = scrolledtext.ScrolledText(
            logs_card.content_frame,
            font=('Consolas', 9),
            bg='#1E1E1E',
            fg='#D4D4D4',
            relief='flat',
            borderwidth=0,
            state='disabled'
        )
        self.log_display.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_footer(self):
        """Create the footer section"""
        footer = tk.Frame(self.window, bg=self.colors['secondary'], height=40)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        # Footer content
        footer_content = tk.Frame(footer, bg=self.colors['secondary'])
        footer_content.pack(expand=True, fill='both')
        
        # Status text
        self.status_label = tk.Label(
            footer_content,
            text="Ready",
            font=('Segoe UI', 10),
            bg=self.colors['secondary'],
            fg=self.colors['light']
        )
        self.status_label.pack(side='left', padx=20, pady=10)
        
        # Time display
        self.time_label = tk.Label(
            footer_content,
            text="",
            font=('Segoe UI', 10),
            bg=self.colors['secondary'],
            fg=self.colors['light']
        )
        self.time_label.pack(side='right', padx=20, pady=10)
        
        # Update time
        self.update_time()
    
    def setup_shadow_ai(self):
        """Initialize Shadow AI"""
        try:
            if ShadowAI:
                self.shadow_ai = ShadowAI()
                self.ai_engine_status.set_status('success')
                self.update_status("Shadow AI initialized successfully")
                self.log_activity("✅ AI Engine: Online")
            else:
                self.ai_engine_status.set_status('error')
                self.update_status("Shadow AI not available")
                self.log_activity("❌ AI Engine: Offline")
        except Exception as e:
            self.ai_engine_status.set_status('error')
            self.update_status(f"Error initializing AI: {e}")
            self.log_activity(f"❌ AI Engine Error: {e}")
        
        # Check voice availability
        try:
            if VOICE_ENABLED:
                self.voice_available = True
                self.voice_status.set_status('success')
                self.log_activity("✅ Voice Recognition: Available")
            else:
                self.voice_available = False
                self.voice_status.set_status('error')
                self.voice_btn.configure(state='disabled')
                self.log_activity("❌ Voice Recognition: Disabled")
        except Exception as e:
            self.voice_available = False
            self.voice_status.set_status('error')
            self.voice_btn.configure(state='disabled')
            self.log_activity(f"❌ Voice Error: {e}")
        
        # System status
        self.system_status.set_status('success')
        self.log_activity("✅ System Monitor: Active")
    
    def populate_commands_list(self, text_widget):
        """Populate the commands list"""
        commands = [
            "🎯 BASIC COMMANDS",
            "• 'open notepad' - Opens Notepad application",
            "• 'take screenshot' - Captures screen",
            "• 'open browser' - Launches default browser",
            "• 'type [text]' - Types the specified text",
            "",
            "🌐 WEB AUTOMATION",
            "• 'search for [query]' - Performs web search",
            "• 'go to [website]' - Navigates to website",
            "• 'download [url]' - Downloads file from URL",
            "",
            "📁 FILE OPERATIONS",
            "• 'create document [name]' - Creates new document",
            "• 'open file [path]' - Opens specified file",
            "• 'save file [path]' - Saves current file",
            "",
            "🖥️ SYSTEM CONTROL",
            "• 'minimize window' - Minimizes active window",
            "• 'maximize window' - Maximizes active window",
            "• 'close window' - Closes active window",
            "",
            "🎤 VOICE COMMANDS",
            "• Click the Voice button and speak naturally",
            "• Commands are processed in real-time",
            "• Supports all text commands via voice"
        ]
        
        text_widget.configure(state='normal')
        for command in commands:
            if command.startswith('🎯') or command.startswith('🌐') or command.startswith('📁') or command.startswith('🖥️') or command.startswith('🎤'):
                text_widget.insert('end', f"\n{command}\n", 'header')
            else:
                text_widget.insert('end', f"{command}\n")
        text_widget.configure(state='disabled')
        
        # Configure tags
        text_widget.tag_configure('header', font=('Segoe UI', 11, 'bold'), foreground=self.colors['accent'])
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        if event.state & 0x4:  # Control is held
            return  # Allow newline
        self.send_text_command()
        return 'break'
    
    def send_text_command(self):
        """Send text command"""
        command = self.text_input.get('1.0', 'end-1c').strip()
        if not command:
            return
        
        self.text_input.delete('1.0', 'end')
        self.add_chat_message(f"You: {command}", 'user')
        self.process_command(command)
    
    def send_voice_command(self):
        """Send voice command"""
        if not self.voice_available:
            self.show_error("Voice recognition is not available")
            return
        
        self.voice_btn.configure(text="🎤 Listening...", state='disabled')
        self.update_status("Listening for voice command...")
        
        def voice_thread():
            try:
                # Import voice input here to avoid startup delays
                from input.voice_input import get_voice_input
                
                command = get_voice_input()
                if command:
                    self.window.after(0, lambda: self.add_chat_message(f"You (voice): {command}", 'user'))
                    self.window.after(0, lambda: self.process_command(command))
                else:
                    self.window.after(0, lambda: self.update_status("No voice command detected"))
                    
            except Exception as e:
                self.window.after(0, lambda: self.show_error(f"Voice recognition error: {e}"))
            finally:
                self.window.after(0, lambda: self.voice_btn.configure(text="🎤 Voice", state='normal'))
                self.window.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=voice_thread, daemon=True).start()
    
    def process_command(self, command: str):
        """Process a command"""
        if not self.shadow_ai:
            self.add_chat_message("Shadow AI is not available", 'error')
            return
        
        self.ai_engine_status.set_status('processing')
        self.update_status("Processing command...")
        
        def process_thread():
            try:
                response = self.shadow_ai.process_command(command)
                self.window.after(0, lambda: self.add_chat_message(f"Shadow AI: {response}", 'assistant'))
                self.window.after(0, lambda: self.log_activity(f"🤖 Executed: {command}"))
                
            except Exception as e:
                error_msg = f"Error processing command: {e}"
                self.window.after(0, lambda: self.add_chat_message(error_msg, 'error'))
                self.window.after(0, lambda: self.log_activity(f"❌ Error: {command}"))
            finally:
                self.window.after(0, lambda: self.ai_engine_status.set_status('success'))
                self.window.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def add_chat_message(self, message: str, message_type: str = 'info'):
        """Add message to chat display"""
        self.chat_display.configure(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Configure colors based on message type
        colors = {
            'user': '#2C3E50',
            'assistant': '#27AE60',
            'error': '#E74C3C',
            'info': '#3498DB'
        }
        
        # Add timestamp
        self.chat_display.insert('end', f"[{timestamp}] ", 'timestamp')
        
        # Add message
        self.chat_display.insert('end', f"{message}\n\n", message_type)
        
        # Configure tags
        self.chat_display.tag_configure('timestamp', foreground='#7F8C8D', font=('Segoe UI', 9))
        self.chat_display.tag_configure(message_type, foreground=colors.get(message_type, '#2C3E50'))
        
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', 'end')
        self.chat_display.configure(state='disabled')
        self.log_activity("🗑️ Chat cleared")
    
    def log_activity(self, message: str):
        """Log activity message"""
        self.activity_log.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.insert('end', f"[{timestamp}] {message}\n")
        self.activity_log.configure(state='disabled')
        self.activity_log.see('end')
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_label.configure(text=message)
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.window.after(1000, self.update_time)
    
    def start_status_updates(self):
        """Start periodic status updates"""
        def update_loop():
            # Update system status
            try:
                # You can add actual system monitoring here
                self.system_status.set_status('success')
            except:
                self.system_status.set_status('error')
            
            # Schedule next update
            self.window.after(5000, update_loop)
        
        update_loop()
    
    def show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def show_info(self, message: str):
        """Show info message"""
        messagebox.showinfo("Information", message)
    
    # Quick action methods
    def quick_notepad(self):
        """Quick open notepad"""
        self.process_command("open notepad")
    
    def quick_browser(self):
        """Quick open browser"""
        self.process_command("open browser")
    
    def quick_screenshot(self):
        """Quick take screenshot"""
        self.process_command("take screenshot")
    
    def quick_explorer(self):
        """Quick open file explorer"""
        self.process_command("open file explorer")
    
    def quick_system_info(self):
        """Quick system info"""
        self.process_command("show system information")
    
    def run(self):
        """Start the GUI"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.window.quit()

def main():
    """Main function"""
    try:
        app = ShadowAIPremiumGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Shadow AI Premium GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
