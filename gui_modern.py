# gui_modern.py
"""
Modern Animated GUI for Shadow AI
Beautiful, responsive interface with real-time task visualization
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import queue
import json
import math
import random
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from pathlib import Path

# Import Shadow AI components with fallbacks
try:
    from brain.universal_processor import process_universal_command
    from brain.universal_executor import execute_universal_task
    SHADOW_AI_AVAILABLE = True
except ImportError:
    SHADOW_AI_AVAILABLE = False
    logging.warning("Shadow AI modules not available - using fallback mode")

# Don't import voice modules at startup to avoid microphone calibration
VOICE_AVAILABLE = False
_voice_input_module = None
_get_voice_input = None
_speak_response = None

def _lazy_import_voice():
    """Lazy import voice modules only when needed"""
    global VOICE_AVAILABLE, _voice_input_module, _get_voice_input, _speak_response
    
    if _voice_input_module is None:
        try:
            from input import voice_input as vi
            _voice_input_module = vi
            _get_voice_input = vi.get_voice_input
            _speak_response = vi.speak_response
            VOICE_AVAILABLE = True
        except Exception as e:
            logging.warning(f"Voice input not available: {e}")
            VOICE_AVAILABLE = False
    
    return VOICE_AVAILABLE

from utils.logging import setup_logging

# Fallback functions
def fallback_process_command(command):
    """Fallback command processor when Shadow AI is not available"""
    class FallbackTask:
        def __init__(self, command):
            self.description = f"Fallback processing: {command}"
            self.complexity = type('obj', (object,), {'value': 'Simple'})()
            self.estimated_duration = 2
            self.steps = [{"action": "simulate_work", "description": "Simulating work"}]
    
    return FallbackTask(command)

def fallback_execute_task(task):
    """Fallback task executor"""
    class FallbackResult:
        def __init__(self):
            self.success = True
            self.execution_time = 2.0
            self.warnings = ["Running in fallback mode - Shadow AI modules not available"]
            self.error_message = None
            self.step_results = []
    
    time.sleep(2)  # Simulate work
    return FallbackResult()

def fallback_voice_input(prompt):
    """Fallback voice input when not available"""
    return None

def fallback_speak(text):
    """Fallback speech when not available"""
    print(f"🔊 {text}")

class ModernShadowGUI:
    def __init__(self):
        # Initialize state management first
        self.is_processing = False
        self.current_task = None
        self.voice_mode = False
        
        # Animation variables
        self.pulse_value = 0
        self.typing_dots = 0
        self.progress_value = 0
        self.glow_intensity = 0
        self.button_hover_state = {}
        
        # Queue for thread communication
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_animations()
        
        # Setup logging
        setup_logging()
        
        # Start background workers
        self.start_background_workers()
        
    def setup_window(self):
        """Configure the main window with premium styling"""
        self.root.title("Shadow AI - Universal Assistant")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Enable window transparency and effects
        self.root.attributes('-alpha', 0.98)  # Slight transparency for premium feel
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Set ultra-modern premium color scheme with vibrant gradients
        self.colors = {
            # Dark theme base colors
            'bg_primary': '#0d0d0f',      # Deep space black
            'bg_secondary': '#1a1a1f',    # Dark charcoal
            'bg_tertiary': '#2a2a35',     # Medium gray-blue
            'bg_card': '#1e1e26',         # Card background
            'bg_elevated': '#252530',     # Elevated surfaces
            
            # Vibrant accent colors
            'accent': '#00f5ff',          # Electric cyan
            'accent_hover': '#00e1ff',    # Brighter cyan
            'accent_secondary': '#ff006e', # Hot pink
            'accent_tertiary': '#8b5cf6', # Purple
            'accent_gold': '#fbbf24',     # Gold
            
            # Gradient colors
            'gradient_start': '#667eea',  # Purple-blue
            'gradient_end': '#764ba2',    # Deep purple
            'gradient_warm_start': '#ff9a8b',  # Warm pink
            'gradient_warm_end': '#a8edea',    # Mint
            'gradient_cool_start': '#667eea',  # Cool blue
            'gradient_cool_end': '#764ba2',    # Purple
            
            # Text colors
            'text_primary': '#ffffff',    # Pure white
            'text_secondary': '#b8c5d1',  # Light blue-gray
            'text_muted': '#8a94a6',      # Muted blue-gray
            'text_accent': '#00f5ff',     # Accent text
            
            # Status colors
            'success': '#10b981',         # Emerald green
            'warning': '#f59e0b',         # Amber
            'error': '#ef4444',           # Red
            'processing': '#3b82f6',      # Blue
            'info': '#06b6d4',            # Cyan
            
            # Effect colors
            'glow': '#00f5ff',            # Translucent glow
            'glow_strong': '#00e1ff',     # Strong glow
            'shadow': '#000000',          # Deep shadow
            'border': '#404040',          # Border color
            'border_active': '#00f5ff',   # Active border
            
            # Animation colors
            'pulse_start': '#667eea',     # Pulse start
            'pulse_end': '#764ba2',       # Pulse end
            'shimmer': '#ffffff',         # Shimmer effect
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Add window fade-in animation
        self.fade_in_window()
        
    def setup_styles(self):
        """Configure enhanced ttk styles with modern design"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Enhanced styles with modern aesthetics
        style.configure('Modern.TFrame', 
                       background=self.colors['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Card.TFrame', 
                       background=self.colors['bg_card'],
                       relief='flat',
                       borderwidth=1,
                       fieldbackground=self.colors['bg_card'])
        
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'], 
                       font=('Segoe UI Light', 28, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_secondary'], 
                       font=('Segoe UI', 13))
        
        style.configure('Status.TLabel', 
                       background=self.colors['bg_card'], 
                       foreground=self.colors['text_primary'], 
                       font=('Segoe UI Semibold', 10))
        
        style.configure('Modern.TButton', 
                       font=('Segoe UI', 11), 
                       padding=(25, 15),
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Accent.TButton', 
                       background=self.colors['accent'], 
                       foreground='white', 
                       font=('Segoe UI', 12, 'bold'),
                       relief='flat',
                       borderwidth=0)
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Enhanced left panel with shadow effect
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_card'], 
                             relief='flat', bd=1,
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
        self.create_input_panel(left_panel)
        
        # Enhanced right panel with shadow effect  
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_card'], 
                              relief='flat', bd=1,
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(15, 0))
        self.create_status_panel(right_panel)
        
    def create_header(self, parent):
        """Create the ultra-modern header with gradient backgrounds and animations"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Create gradient background canvas for header
        header_canvas = tk.Canvas(header_frame, height=150, 
                                 bg=self.colors['bg_primary'], 
                                 highlightthickness=0)
        header_canvas.pack(fill='x', pady=(0, 20))
        
        # Draw animated gradient background
        self.create_gradient_background(header_canvas)
        
        # Main title with enhanced styling and glow effect
        title_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_container.pack(anchor='center', pady=(10, 5))
        
        # Add glowing title with shadow effect
        title_shadow = tk.Label(title_container, text="🧠 Shadow AI", 
                               font=('Segoe UI Light', 36, 'bold'),
                               bg=self.colors['bg_primary'], 
                               fg=self.colors['shadow'])
        title_shadow.place(x=2, y=2)
        
        self.title_label = tk.Label(title_container, text="🧠 Shadow AI", 
                                   font=('Segoe UI Light', 36, 'bold'),
                                   bg=self.colors['bg_primary'], 
                                   fg=self.colors['accent'])
        self.title_label.pack()
        
        # Animated subtitle with rainbow effect
        subtitle_label = tk.Label(header_frame, 
                                 text="⚡ Universal AI Assistant with Advanced Capabilities ⚡", 
                                 font=('Segoe UI', 16, 'italic'),
                                 bg=self.colors['bg_primary'], 
                                 fg=self.colors['text_accent'])
        subtitle_label.pack(anchor='center', pady=(0, 15))
        
        # Enhanced info section with glowing cards
        info_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        info_container.pack(anchor='center', pady=(15, 0))
        
        # Version card with gradient background
        version_card = tk.Frame(info_container, bg=self.colors['bg_elevated'], 
                               relief='flat', bd=0)
        version_card.pack(side='left', padx=(0, 25), pady=8)
        
        version_canvas = tk.Canvas(version_card, width=220, height=40, 
                                  bg=self.colors['bg_elevated'], 
                                  highlightthickness=0)
        version_canvas.pack()
        
        # Draw gradient background for version card
        self.create_card_gradient(version_canvas, self.colors['gradient_cool_start'], 
                                 self.colors['gradient_cool_end'])
        
        version_label = tk.Label(version_canvas, text="🚀 v3.0 | Powered by Gemini AI", 
                                font=('Segoe UI', 11, 'bold'), 
                                bg=self.colors['bg_elevated'], 
                                fg=self.colors['text_primary'])
        version_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Enhanced status indicator with animated glow
        status_card = tk.Frame(info_container, bg=self.colors['bg_elevated'], 
                              relief='flat', bd=0)
        status_card.pack(side='left', pady=8)
        
        status_canvas = tk.Canvas(status_card, width=180, height=40, 
                                 bg=self.colors['bg_elevated'], 
                                 highlightthickness=0)
        status_canvas.pack()
        
        # Draw gradient background for status card
        self.create_card_gradient(status_canvas, self.colors['gradient_warm_start'], 
                                 self.colors['gradient_warm_end'])
        
        self.status_frame = tk.Frame(status_canvas, bg=self.colors['bg_elevated'])
        self.status_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.status_indicator = tk.Canvas(self.status_frame, width=24, height=24, 
                                         bg=self.colors['bg_elevated'], 
                                         highlightthickness=0)
        self.status_indicator.pack(side='left', padx=(0, 12))
        
        self.status_label = tk.Label(self.status_frame, text="Ready", 
                                    font=('Segoe UI', 11, 'bold'),
                                    bg=self.colors['bg_elevated'], 
                                    fg=self.colors['text_primary'])
        self.status_label.pack(side='left')
        
        # Draw enhanced status indicator with glow and animation
        self.update_status_indicator('ready')
        
        # Add floating particles animation
        self.animate_header_particles(header_canvas)
        
    def create_input_panel(self, parent):
        """Create the input and control panel"""
        # Enhanced panel title with modern styling
        title_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        title_frame.pack(fill='x', padx=20, pady=(25, 15))
        
        title_label = tk.Label(title_frame, text="💬 Command Center", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=self.colors['bg_card'], 
                              fg=self.colors['accent'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Enter your commands or use voice input", 
                                 font=('Segoe UI', 11), 
                                 bg=self.colors['bg_card'], 
                                 fg=self.colors['text_muted'])
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Enhanced input section with better styling
        input_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat')
        input_frame.pack(fill='x', padx=20, pady=15)
        
        # Enhanced text input with animated gradient border
        input_label = tk.Label(input_frame, text="💭 What would you like me to do?", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg=self.colors['bg_card'], 
                              fg=self.colors['text_accent'])
        input_label.pack(anchor='w', pady=(0, 12))
        
        # Ultra-modern input container with animated border
        input_outer = tk.Frame(input_frame, bg=self.colors['bg_card'])
        input_outer.pack(fill='x', pady=(0, 20))
        
        self.input_border_canvas = tk.Canvas(input_outer, height=90, 
                                           bg=self.colors['bg_card'], 
                                           highlightthickness=0)
        self.input_border_canvas.pack(fill='x')
        
        input_container = tk.Frame(self.input_border_canvas, bg=self.colors['bg_elevated'])
        input_container.place(relx=0.5, rely=0.5, anchor='center', 
                             relwidth=0.98, relheight=0.9)
        
        self.command_entry = tk.Text(input_container, height=3, 
                                    font=('Segoe UI', 13), 
                                    bg=self.colors['bg_elevated'], 
                                    fg=self.colors['text_primary'], 
                                    insertbackground=self.colors['accent'], 
                                    relief='flat', 
                                    bd=0,
                                    wrap='word', 
                                    padx=25, pady=20,
                                    selectbackground=self.colors['accent'],
                                    selectforeground='white')
        self.command_entry.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Animate input border
        self.animate_input_border()
        
        # Enhanced control buttons with ultra-modern styling and gradients
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_card'])
        button_frame.pack(fill='x', pady=(15, 0))
        
        # Execute button with animated gradient and glow effect
        execute_container = tk.Frame(button_frame, bg=self.colors['bg_card'])
        execute_container.pack(side='left', padx=(0, 15))
        
        self.execute_canvas = tk.Canvas(execute_container, width=150, height=50, 
                                       bg=self.colors['bg_card'], 
                                       highlightthickness=0)
        self.execute_canvas.pack()
        
        self.execute_btn = tk.Button(self.execute_canvas, text="⚡ Execute", 
                                    font=('Segoe UI', 13, 'bold'), 
                                    bg=self.colors['accent'], 
                                    fg='white', 
                                    activebackground=self.colors['accent_hover'],
                                    activeforeground='white',
                                    relief='flat', 
                                    bd=0,
                                    cursor='hand2',
                                    command=self.execute_command)
        self.execute_btn.place(relx=0.5, rely=0.5, anchor='center', width=140, height=40)
        
        # Voice button with animated styling
        voice_container = tk.Frame(button_frame, bg=self.colors['bg_card'])
        voice_container.pack(side='left', padx=(0, 15))
        
        self.voice_canvas = tk.Canvas(voice_container, width=120, height=50, 
                                     bg=self.colors['bg_card'], 
                                     highlightthickness=0)
        self.voice_canvas.pack()
        
        self.voice_btn = tk.Button(self.voice_canvas, text="🎤 Voice", 
                                  font=('Segoe UI', 12, 'bold'), 
                                  bg=self.colors['accent_secondary'], 
                                  fg='white', 
                                  activebackground=self.colors['accent_tertiary'],
                                  activeforeground='white',
                                  relief='flat', 
                                  bd=0,
                                  cursor='hand2',
                                  command=self.toggle_voice_mode)
        self.voice_btn.place(relx=0.5, rely=0.5, anchor='center', width=110, height=40)
        
        # Clear button with modern styling
        clear_container = tk.Frame(button_frame, bg=self.colors['bg_card'])
        clear_container.pack(side='left')
        
        self.clear_canvas = tk.Canvas(clear_container, width=100, height=50, 
                                     bg=self.colors['bg_card'], 
                                     highlightthickness=0)
        self.clear_canvas.pack()
        
        self.clear_btn = tk.Button(self.clear_canvas, text="🗑️ Clear", 
                                  font=('Segoe UI', 11, 'bold'), 
                                  bg=self.colors['bg_elevated'], 
                                  fg=self.colors['text_secondary'], 
                                  activebackground=self.colors['error'],
                                  activeforeground='white',
                                  relief='flat', 
                                  bd=0,
                                  cursor='hand2',
                                  command=self.clear_input)
        self.clear_btn.place(relx=0.5, rely=0.5, anchor='center', width=90, height=40)
        
        # Add enhanced hover effects and gradient backgrounds
        self.setup_button_effects()
        
        # Add button animations
        self.animate_buttons()
        
        # Enhanced examples section with better styling
        examples_frame = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat')
        examples_frame.pack(fill='both', expand=True, padx=20, pady=(25, 25))
        
        # Examples header with icon
        examples_header = tk.Frame(examples_frame, bg=self.colors['bg_card'])
        examples_header.pack(fill='x', padx=20, pady=(20, 15))
        
        examples_label = tk.Label(examples_header, text="💡 Example Commands", 
                                 font=('Segoe UI', 16, 'bold'), 
                                 bg=self.colors['bg_card'], 
                                 fg=self.colors['accent'])
        examples_label.pack(anchor='w')
        
        examples_hint = tk.Label(examples_header, text="Double-click any example to try it", 
                                font=('Segoe UI', 10), 
                                bg=self.colors['bg_card'], 
                                fg=self.colors['text_muted'])
        examples_hint.pack(anchor='w', pady=(2, 0))
        
        # Enhanced examples list with better styling
        examples = [
            "✍️ Write an article about artificial intelligence",
            "📝 Open Notepad and create a shopping list", 
            "🔍 Search for the best laptops under $1000",
            "📧 Create a professional email template",
            "📸 Take a screenshot and save it to desktop",
            "📁 Organize my Downloads folder by file type"
        ]
        
        # Custom styled listbox
        listbox_frame = tk.Frame(examples_frame, bg=self.colors['bg_tertiary'], 
                                relief='flat', bd=1)
        listbox_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.examples_listbox = tk.Listbox(listbox_frame, 
                                          font=('Segoe UI', 11), 
                                          bg=self.colors['bg_tertiary'], 
                                          fg=self.colors['text_primary'], 
                                          selectbackground=self.colors['accent'], 
                                          selectforeground='white',
                                          activestyle='none',
                                          relief='flat', 
                                          bd=0,
                                          height=6,
                                          highlightthickness=0)
        self.examples_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        for example in examples:
            self.examples_listbox.insert(tk.END, f"  {example}")
        
        self.examples_listbox.bind('<Double-Button-1>', self.use_example)
        
        # Add hover effects
        self.examples_listbox.bind('<Enter>', lambda e: self.examples_listbox.config(cursor='hand2'))
        self.examples_listbox.bind('<Leave>', lambda e: self.examples_listbox.config(cursor=''))
        
    def create_status_panel(self, parent):
        """Create the status and visualization panel"""
        # Enhanced panel title
        title_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        title_frame.pack(fill='x', padx=20, pady=(25, 15))
        
        title_label = tk.Label(title_frame, text="📊 Task Monitor", 
                              font=('Segoe UI', 18, 'bold'), 
                              bg=self.colors['bg_card'], 
                              fg=self.colors['accent'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame, text="Real-time task progress and activity", 
                                 font=('Segoe UI', 11), 
                                 bg=self.colors['bg_card'], 
                                 fg=self.colors['text_muted'])
        subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Enhanced current task section
        task_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        task_frame.pack(fill='x', padx=20, pady=12)
        
        task_label = tk.Label(task_frame, text="Current Task:", 
                             font=('Segoe UI', 12, 'bold'), 
                             bg=self.colors['bg_card'], 
                             fg=self.colors['text_secondary'])
        task_label.pack(anchor='w')
        
        self.current_task_label = tk.Label(task_frame, text="Waiting for command...", 
                                          font=('Segoe UI', 11), 
                                          bg=self.colors['bg_card'], 
                                          fg=self.colors['text_primary'],
                                          wraplength=300)
        self.current_task_label.pack(anchor='w', pady=(5, 0))
        
        # Enhanced progress section
        progress_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        progress_frame.pack(fill='x', padx=20, pady=12)
        
        progress_label = tk.Label(progress_frame, text="Progress:", 
                                 font=('Segoe UI', 12, 'bold'), 
                                 bg=self.colors['bg_card'], 
                                 fg=self.colors['text_secondary'])
        progress_label.pack(anchor='w')
        
        # Enhanced progress canvas with border
        progress_container = tk.Frame(progress_frame, bg=self.colors['border'])
        progress_container.pack(fill='x', pady=(8, 0))
        
        self.progress_canvas = tk.Canvas(progress_container, height=25, 
                                        bg=self.colors['bg_tertiary'], 
                                        highlightthickness=0,
                                        relief='flat', bd=0)
        self.progress_canvas.pack(fill='x', padx=1, pady=1)
        
        # Enhanced activity log
        log_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        log_frame.pack(fill='both', expand=True, padx=20, pady=(25, 25))
        
        # Log header
        log_header = tk.Frame(log_frame, bg=self.colors['bg_card'])
        log_header.pack(fill='x', pady=(0, 15))
        
        log_label = tk.Label(log_header, text="📝 Activity Log", 
                            font=('Segoe UI', 16, 'bold'), 
                            bg=self.colors['bg_card'], 
                            fg=self.colors['accent'])
        log_label.pack(anchor='w')
        
        log_hint = tk.Label(log_header, text="Real-time activity and task progress", 
                           font=('Segoe UI', 10), 
                           bg=self.colors['bg_card'], 
                           fg=self.colors['text_muted'])
        log_hint.pack(anchor='w', pady=(2, 0))
        
        # Enhanced log container with border
        log_container = tk.Frame(log_frame, bg=self.colors['border'])
        log_container.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=15, 
                                                 font=('Consolas', 10), 
                                                 bg=self.colors['bg_tertiary'], 
                                                 fg=self.colors['text_primary'], 
                                                 insertbackground=self.colors['accent'], 
                                                 relief='flat', 
                                                 bd=0,
                                                 wrap='word',
                                                 selectbackground=self.colors['accent'],
                                                 selectforeground='white')
        self.log_text.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Add enhanced welcome messages showcasing new features
        self.add_log_entry("🚀 Shadow AI v3.0 Ultra - Premium Edition Initialized!", "success")
        self.add_log_entry("✨ FIXED: Unknown action errors resolved - all AI commands now supported", "success")
        self.add_log_entry("🎨 NEW: Ultra-modern UI with animated gradients and particles", "processing")
        self.add_log_entry("⚡ NEW: Dynamic button effects and flowing input borders", "processing")
        self.add_log_entry("🌈 NEW: Rainbow progress bars with animated particles", "processing")
        self.add_log_entry("💫 NEW: Floating particle animations and window transparency", "processing")
        self.add_log_entry("💡 Try: 'open notepad and write an article about AI' - now works perfectly!", "info")
        self.add_log_entry("🎤 Voice input available with enhanced visual feedback", "info")
        
    def setup_animations(self):
        """Setup animation timers and effects"""
        self.animate_pulse()
        self.animate_typing()
        
    def animate_pulse(self):
        """Animate the status indicator pulse"""
        try:
            if hasattr(self, 'is_processing') and self.is_processing:
                self.pulse_value = (self.pulse_value + 0.1) % (2 * 3.14159)
                self.update_status_indicator('processing')
            
            self.root.after(50, self.animate_pulse)
        except Exception:
            # Ignore animation errors and continue
            self.root.after(50, self.animate_pulse)
        
    def animate_typing(self):
        """Animate typing dots when processing"""
        try:
            if hasattr(self, 'is_processing') and self.is_processing:
                self.typing_dots = (self.typing_dots + 1) % 4
                dots = "." * self.typing_dots + " " * (3 - self.typing_dots)
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=f"Processing{dots}")
            
            self.root.after(500, self.animate_typing)
        except Exception:
            # Ignore animation errors and continue
            self.root.after(500, self.animate_typing)
        
    def update_status_indicator(self, status):
        """Update the enhanced status indicator with glow effects"""
        self.status_indicator.delete("all")
        
        if status == 'ready':
            color = self.colors['success']
            glow_color = '#4caf50'
        elif status == 'processing':
            # Enhanced pulsing effect with glow
            import math
            alpha = (math.sin(self.pulse_value) + 1) / 2
            color = self.interpolate_color(self.colors['processing'], '#ffffff', alpha * 0.4)
            glow_color = self.colors['glow']
        elif status == 'error':
            color = self.colors['error']
            glow_color = '#f44336'
        elif status == 'warning':
            color = self.colors['warning']
            glow_color = '#ff9800'
        else:
            color = self.colors['text_secondary']
            glow_color = '#78909c'
        
        # Draw glow effect
        self.status_indicator.create_oval(2, 2, 18, 18, fill=glow_color, outline="")
        # Draw main indicator
        self.status_indicator.create_oval(4, 4, 16, 16, fill=color, outline="")
        # Add inner highlight
        self.status_indicator.create_oval(6, 6, 10, 10, fill='#ffffff', outline="")
        
    def interpolate_color(self, color1, color2, factor):
        """Interpolate between two hex colors"""
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        
        def rgb_to_hex(rgb):
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        rgb = tuple(int(rgb1[i] + factor * (rgb2[i] - rgb1[i])) for i in range(3))
        return rgb_to_hex(rgb)
        
    def update_progress(self, progress):
        """Update the ultra-modern progress bar with animated gradients and particles"""
        if not hasattr(self, 'progress_canvas') or not self.progress_canvas.winfo_exists():
            self.root.after(50, lambda: self.update_progress(progress))
            return
            
        self.progress_canvas.delete("all")
        self.progress_canvas.update_idletasks()
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        if width > 1:
            # Ultra-modern background with depth
            self.progress_canvas.create_rectangle(0, 0, width, height, 
                                                fill=self.colors['bg_elevated'], 
                                                outline="")
            
            # Inner shadow for depth (simplified for Windows compatibility)
            for i in range(3):
                shadow_color = "#111111"  # Simple dark color instead of alpha
                self.progress_canvas.create_rectangle(i, i, width-i, height-i, 
                                                    outline=shadow_color, width=1)
            
            progress_width = width * (progress / 100)
            if progress_width > 0:
                # Create animated gradient progress bar
                import math
                time_factor = time.time() * 4
                
                for i in range(int(progress_width)):
                    factor = (math.sin(time_factor + i * 0.1) + 1) / 2
                    
                    # Dynamic color based on progress
                    if progress < 30:
                        # Red to orange gradient for low progress
                        r1, g1, b1 = self.hex_to_rgb(self.colors['error'])
                        r2, g2, b2 = self.hex_to_rgb(self.colors['warning'])
                    elif progress < 70:
                        # Orange to blue gradient for medium progress
                        r1, g1, b1 = self.hex_to_rgb(self.colors['warning'])
                        r2, g2, b2 = self.hex_to_rgb(self.colors['processing'])
                    else:
                        # Blue to green gradient for high progress
                        r1, g1, b1 = self.hex_to_rgb(self.colors['processing'])
                        r2, g2, b2 = self.hex_to_rgb(self.colors['success'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    self.progress_canvas.create_line(i+3, 3, i+3, height-3, 
                                                   fill=color, width=1)
                
                # Animated particles on progress bar
                if progress > 10:
                    particle_count = int(progress / 20) + 1
                    for i in range(particle_count):
                        import random
                        x = random.randint(5, int(progress_width) - 5)
                        y = random.randint(height//4, 3*height//4)
                        
                        # Create glowing particle
                        self.progress_canvas.create_oval(x-2, y-2, x+2, y+2, 
                                                       fill=self.colors['shimmer'], 
                                                       outline="")
                        self.progress_canvas.create_oval(x-1, y-1, x+1, y+1, 
                                                       fill='white', outline="")
                
                # Leading edge glow effect (simplified for Windows)
                if progress_width > 5:
                    glow_x = int(progress_width)
                    for i in range(8):
                        glow_color = self.colors['accent']  # Solid color instead of alpha
                        if i < 4:  # Only first few pixels for glow effect
                            self.progress_canvas.create_line(glow_x + i, 2, glow_x + i, height-2, 
                                                           fill=glow_color, width=1)
            
            # Ultra-modern progress text with glow
            progress_text = f"{progress:.1f}%"
            text_x, text_y = width//2, height//2
            
            # Text glow effect (simplified for Windows)
            for offset in [(1,1), (-1,1), (1,-1), (-1,-1)]:
                self.progress_canvas.create_text(text_x + offset[0], text_y + offset[1], 
                                               text=progress_text, 
                                               fill=self.colors['shadow'], 
                                               font=('Segoe UI', 11, 'bold'))
            
            # Main text
            text_color = self.colors['text_primary'] if progress < 70 else '#000000'
            self.progress_canvas.create_text(text_x, text_y, 
                                           text=progress_text, 
                                           fill=text_color, 
                                           font=('Segoe UI', 11, 'bold'))
        
    def add_log_entry(self, message, level="info"):
        """Add an entry to the activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on level
        colors = {
            'info': self.colors['text_secondary'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['error'],
            'processing': self.colors['processing']
        }
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        # Color the last line
        start_line = self.log_text.index(tk.END + "-2l linestart")
        end_line = self.log_text.index(tk.END + "-1l lineend")
        
        tag_name = f"level_{level}_{timestamp}"
        self.log_text.tag_add(tag_name, start_line, end_line)
        self.log_text.tag_config(tag_name, foreground=colors.get(level, colors['info']))
        
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        
    def execute_command(self):
        """Execute the command from the input field"""
        command = self.command_entry.get(1.0, tk.END).strip()
        if not command:
            messagebox.showwarning("Warning", "Please enter a command")
            return
        
        if self.is_processing:
            messagebox.showinfo("Info", "Another task is already running")
            return
        
        # Clear input
        self.command_entry.delete(1.0, tk.END)
        
        # Start processing
        self.start_task_processing(command)
        
    def toggle_voice_mode(self):
        """Toggle voice input mode"""
        if self.is_processing:
            messagebox.showinfo("Info", "Cannot change mode while processing")
            return
        
        if not self.voice_mode:
            # Try to import voice modules
            if _lazy_import_voice():
                self.voice_mode = True
                self.voice_btn.config(text="🎤 Listening...", bg=self.colors['accent'])
                self.add_log_entry("🎤 Voice mode activated - Listening for command", "processing")
                
                # Start voice input in background thread
                threading.Thread(target=self.get_voice_command, daemon=True).start()
            else:
                messagebox.showwarning("Voice Not Available", 
                                     "Voice input is not available. Please check your microphone connection.")
                self.add_log_entry("🎤 Voice input not available", "warning")
        else:
            self.voice_mode = False
            self.voice_btn.config(text="🎤 Voice", bg=self.colors['accent_secondary'])
            self.add_log_entry("🎤 Voice mode deactivated", "info")
    
    def get_voice_command(self):
        """Get voice command in background thread"""
        try:
            # Try to import voice modules when needed
            if _lazy_import_voice():
                command = _get_voice_input("What would you like me to do?")
            else:
                command = fallback_voice_input("What would you like me to do?")
                
            if command:
                self.root.after(0, lambda: self.handle_voice_command(command))
            else:
                self.root.after(0, self.voice_input_failed)
        except Exception as e:
            self.root.after(0, lambda: self.voice_input_error(str(e)))
    
    def handle_voice_command(self, command):
        """Handle received voice command"""
        self.command_entry.delete(1.0, tk.END)
        self.command_entry.insert(1.0, command)
        self.voice_mode = False
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['accent_secondary'])
        self.add_log_entry(f"🎤 Voice command received: {command}", "success")
        
        # Auto-execute voice command
        self.start_task_processing(command)
    
    def voice_input_failed(self):
        """Handle voice input failure"""
        self.voice_mode = False
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['accent_secondary'])
        self.add_log_entry("🎤 No voice command detected", "warning")
    
    def voice_input_error(self, error):
        """Handle voice input error"""
        self.voice_mode = False
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['accent_secondary'])
        self.add_log_entry(f"🎤 Voice input error: {error}", "error")
        
    def clear_input(self):
        """Clear the input field"""
        self.command_entry.delete(1.0, tk.END)
        
    def use_example(self, event):
        """Use selected example command"""
        selection = self.examples_listbox.curselection()
        if selection:
            example = self.examples_listbox.get(selection[0]).strip()
            self.command_entry.delete(1.0, tk.END)
            self.command_entry.insert(1.0, example)
            
    def start_task_processing(self, command):
        """Start processing a task"""
        self.is_processing = True
        self.execute_btn.config(state='disabled', text="⏳ Processing...")
        self.current_task_label.config(text=command)
        self.update_status_indicator('processing')
        self.add_log_entry(f"🚀 Starting task: {command}", "processing")
        
        # Reset progress
        self.progress_value = 0
        self.update_progress(0)
        
        # Start task in background thread
        threading.Thread(target=self.process_task, args=(command,), daemon=True).start()
        
        # Start progress animation
        self.animate_progress()
        
    def animate_progress(self):
        """Animate progress during task execution"""
        if self.is_processing and self.progress_value < 90:
            # Simulate progress increase
            self.progress_value += 2
            self.update_progress(self.progress_value)
            self.root.after(200, self.animate_progress)
            
    def process_task(self, command):
        """Process the task in background thread"""
        try:
            # Process the command
            if SHADOW_AI_AVAILABLE:
                task = process_universal_command(command)
            else:
                task = fallback_process_command(command)
            
            if not task:
                self.root.after(0, lambda: self.task_failed("Could not understand the command"))
                return
            
            # Update UI with task details
            self.root.after(0, lambda: self.add_log_entry(f"📊 Task complexity: {task.complexity.value}", "info"))
            self.root.after(0, lambda: self.add_log_entry(f"⏱️ Estimated time: {task.estimated_duration}s", "info"))
            self.root.after(0, lambda: self.add_log_entry(f"📝 Steps: {len(task.steps)}", "info"))
            
            # Execute the task
            if SHADOW_AI_AVAILABLE:
                result = execute_universal_task(task)
            else:
                result = fallback_execute_task(task)
            
            # Update UI with result
            self.root.after(0, lambda: self.task_completed(result))
            
        except Exception as e:
            self.root.after(0, lambda: self.task_failed(f"Error: {str(e)}"))
            
    def task_completed(self, result):
        """Handle task completion"""
        self.is_processing = False
        self.execute_btn.config(state='normal', text="⚡ Execute")
        self.current_task_label.config(text="Task completed")
        self.update_status_indicator('ready')
        self.status_label.config(text="Ready")
        self.progress_value = 100
        self.update_progress(100)
        
        if result.success:
            self.add_log_entry(f"✅ Task completed successfully in {result.execution_time:.1f}s", "success")
            if result.warnings:
                for warning in result.warnings:
                    self.add_log_entry(f"⚠️ Warning: {warning}", "warning")
        else:
            self.add_log_entry(f"❌ Task failed: {result.error_message}", "error")
            if result.step_results:
                for step_result in result.step_results:
                    if not step_result.get("success", False):
                        self.add_log_entry(f"❌ Step {step_result.get('step_number', '?')}: {step_result.get('error', 'Unknown error')}", "error")
        
        # Reset progress after a delay
        self.root.after(3000, lambda: self.update_progress(0))
        
    def task_failed(self, error_message):
        """Handle task failure"""
        self.is_processing = False
        self.execute_btn.config(state='normal', text="⚡ Execute")
        self.current_task_label.config(text="Task failed")
        self.update_status_indicator('error')
        self.status_label.config(text="Error")
        self.update_progress(0)
        
        self.add_log_entry(f"❌ Task failed: {error_message}", "error")
        
    def start_background_workers(self):
        """Start background worker threads"""
        # Monitor queue for updates
        self.monitor_queues()
        
    def monitor_queues(self):
        """Monitor communication queues"""
        try:
            while True:
                result = self.result_queue.get_nowait()
                # Handle results if needed
        except queue.Empty:
            pass
        
        self.root.after(100, self.monitor_queues)
        
    def button_hover(self, button, is_entering):
        """Enhanced hover effects for modern buttons"""
        if button == self.execute_btn:
            if is_entering:
                button.config(bg=self.colors['accent_hover'])
                # Add extra glow effect
                if hasattr(self, 'execute_canvas'):
                    self.execute_canvas.create_rectangle(0, 0, 
                                                       self.execute_canvas.winfo_width(), 
                                                       self.execute_canvas.winfo_height(),
                                                       outline=self.colors['glow_strong'], 
                                                       width=3, tags="hover_glow")
            else:
                button.config(bg=self.colors['accent'])
                if hasattr(self, 'execute_canvas'):
                    self.execute_canvas.delete("hover_glow")
                    
        elif button == self.voice_btn:
            if is_entering:
                if self.voice_mode:
                    button.config(bg=self.colors['accent_hover'])
                else:
                    button.config(bg=self.colors['accent_tertiary'])
                # Add voice button glow
                if hasattr(self, 'voice_canvas'):
                    self.voice_canvas.create_rectangle(0, 0, 
                                                     self.voice_canvas.winfo_width(), 
                                                     self.voice_canvas.winfo_height(),
                                                     outline=self.colors['accent_secondary'], 
                                                     width=3, tags="voice_hover_glow")
            else:
                if self.voice_mode:
                    button.config(bg=self.colors['accent'])
                else:
                    button.config(bg=self.colors['accent_secondary'])
                if hasattr(self, 'voice_canvas'):
                    self.voice_canvas.delete("voice_hover_glow")
                    
        elif button == self.clear_btn:
            if is_entering:
                button.config(bg=self.colors['error'])
                # Add clear button glow
                if hasattr(self, 'clear_canvas'):
                    self.clear_canvas.create_rectangle(0, 0, 
                                                     self.clear_canvas.winfo_width(), 
                                                     self.clear_canvas.winfo_height(),
                                                     outline=self.colors['error'], 
                                                     width=2, tags="clear_hover_glow")
            else:
                button.config(bg=self.colors['bg_elevated'])
                if hasattr(self, 'clear_canvas'):
                    self.clear_canvas.delete("clear_hover_glow")
        
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

    def fade_in_window(self):
        """Animate window fade-in effect"""
        alpha = 0.0
        def fade_step():
            nonlocal alpha
            alpha += 0.05
            if alpha <= 0.98:
                self.root.attributes('-alpha', alpha)
                self.root.after(20, fade_step)
            else:
                self.root.attributes('-alpha', 0.98)
        
        fade_step()
    
    def create_gradient_background(self, canvas):
        """Create animated gradient background"""
        def update_gradient():
            canvas.delete("gradient")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                # Create gradient effect with shifting colors
                import math
                time_factor = time.time() * 0.5
                
                for i in range(height):
                    factor = (math.sin(time_factor + i * 0.05) + 1) / 2
                    
                    # Interpolate between gradient colors
                    r1, g1, b1 = self.hex_to_rgb(self.colors['gradient_start'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['gradient_end'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(0, i, width, i, fill=color, tags="gradient")
            
            self.root.after(100, update_gradient)
        
        update_gradient()
    
    def create_card_gradient(self, canvas, start_color, end_color):
        """Create gradient background for cards"""
        def draw_gradient():
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                canvas.delete("card_gradient")
                
                for i in range(width):
                    factor = i / width
                    
                    # Interpolate between colors
                    r1, g1, b1 = self.hex_to_rgb(start_color)
                    r2, g2, b2 = self.hex_to_rgb(end_color)
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, 0, i, height, fill=color, tags="card_gradient")
        
        canvas.after(50, draw_gradient)
    
    def animate_header_particles(self, canvas):
        """Animate floating particles in header"""
        particles = []
        
        def create_particle():
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                import random
                x = random.randint(0, width)
                y = height
                size = random.randint(2, 4)
                speed = random.uniform(0.5, 2.0)
                
                particle_id = canvas.create_oval(x-size, y-size, x+size, y+size, 
                                               fill=self.colors['shimmer'], 
                                               outline="", tags="particle")
                
                particles.append({
                    'id': particle_id,
                    'x': x,
                    'y': y,
                    'speed': speed,
                    'size': size
                })
        
        def update_particles():
            for particle in particles[:]:
                particle['y'] -= particle['speed']
                
                if particle['y'] < -10:
                    canvas.delete(particle['id'])
                    particles.remove(particle)
                else:
                    canvas.coords(particle['id'], 
                                particle['x'] - particle['size'], 
                                particle['y'] - particle['size'],
                                particle['x'] + particle['size'], 
                                particle['y'] + particle['size'])
            
            # Randomly create new particles
            import random
            if random.random() < 0.1:  # 10% chance each update
                create_particle()
            
            self.root.after(50, update_particles)
        
        update_particles()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def setup_button_effects(self):
        """Setup enhanced button hover and gradient effects"""
        # Execute button gradient background
        def draw_execute_gradient():
            canvas = self.execute_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                canvas.delete("btn_gradient")
                
                # Create animated gradient
                import math
                time_factor = time.time() * 2
                
                for i in range(width):
                    factor = (math.sin(time_factor + i * 0.1) + 1) / 2
                    
                    # Interpolate between accent colors
                    r1, g1, b1 = self.hex_to_rgb(self.colors['accent'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['accent_hover'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, 0, i, height, fill=color, tags="btn_gradient")
            
            self.root.after(100, draw_execute_gradient)
        
        draw_execute_gradient()
        
        # Voice button gradient
        def draw_voice_gradient():
            canvas = self.voice_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                canvas.delete("voice_gradient")
                
                import math
                time_factor = time.time() * 1.5
                
                for i in range(width):
                    factor = (math.sin(time_factor + i * 0.15) + 1) / 2
                    
                    r1, g1, b1 = self.hex_to_rgb(self.colors['accent_secondary'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['accent_tertiary'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, 0, i, height, fill=color, tags="voice_gradient")
            
            self.root.after(120, draw_voice_gradient)
        
        draw_voice_gradient()
    
    def animate_buttons(self):
        """Animate button glow effects"""
        def update_button_glow():
            import math
            time_factor = time.time() * 3
            
            # Animate execute button glow
            alpha = (math.sin(time_factor) + 1) / 2
            glow_width = int(2 + alpha * 3)
            
            # Add glow effects around buttons
            if hasattr(self, 'execute_canvas'):
                self.execute_canvas.delete("glow")
                width = self.execute_canvas.winfo_width()
                height = self.execute_canvas.winfo_height()
                
                if width > 1:
                    # Create glow effect (simplified for Windows)
                    for i in range(glow_width):
                        color = self.colors['glow']  # Solid color instead of alpha
                        
                        if i < 2:  # Only create a simple border effect
                            self.execute_canvas.create_rectangle(
                                -i, -i, width + i, height + i,
                                outline=color, width=1, tags="glow"
                            )
            
            self.root.after(50, update_button_glow)
        
        update_button_glow()
    
    def animate_input_border(self):
        """Animate the input field border with flowing colors"""
        def update_border():
            canvas = self.input_border_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width > 1 and height > 1:
                canvas.delete("input_border")
                
                import math
                time_factor = time.time() * 2
                
                # Create flowing border effect
                border_width = 3
                
                # Top border
                for i in range(width):
                    factor = (math.sin(time_factor + i * 0.02) + 1) / 2
                    
                    r1, g1, b1 = self.hex_to_rgb(self.colors['accent'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['accent_secondary'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, 0, i+1, 0, fill=color, width=border_width, tags="input_border")
                
                # Bottom border
                for i in range(width):
                    factor = (math.sin(time_factor + i * 0.02 + 3.14) + 1) / 2
                    
                    r1, g1, b1 = self.hex_to_rgb(self.colors['accent'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['accent_secondary'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(i, height-1, i+1, height-1, fill=color, width=border_width, tags="input_border")
                
                # Left and right borders
                for i in range(height):
                    factor = (math.sin(time_factor + i * 0.03) + 1) / 2
                    
                    r1, g1, b1 = self.hex_to_rgb(self.colors['accent_tertiary'])
                    r2, g2, b2 = self.hex_to_rgb(self.colors['accent_gold'])
                    
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_line(0, i, 0, i+1, fill=color, width=border_width, tags="input_border")
                    canvas.create_line(width-1, i, width-1, i+1, fill=color, width=border_width, tags="input_border")
            
            self.root.after(80, update_border)
        
        update_border()
        
        # Add enhanced hover effects to all buttons
        self.execute_btn.bind('<Enter>', lambda e: self.button_hover(self.execute_btn, True))
        self.execute_btn.bind('<Leave>', lambda e: self.button_hover(self.execute_btn, False))
        
        self.voice_btn.bind('<Enter>', lambda e: self.button_hover(self.voice_btn, True))
        self.voice_btn.bind('<Leave>', lambda e: self.button_hover(self.voice_btn, False))
        
        self.clear_btn.bind('<Enter>', lambda e: self.button_hover(self.clear_btn, True))
        self.clear_btn.bind('<Leave>', lambda e: self.button_hover(self.clear_btn, False))
