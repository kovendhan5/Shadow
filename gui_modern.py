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
        """Configure the main window"""
        self.root.title("Shadow AI - Universal Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Set dark theme colors
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#404040',
            'accent': '#00d4aa',
            'accent_hover': '#00b896',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'success': '#4ade80',
            'warning': '#fbbf24',
            'error': '#f87171',
            'processing': '#60a5fa'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Modern.TFrame', background=self.colors['bg_primary'])
        style.configure('Card.TFrame', background=self.colors['bg_secondary'], relief='flat', borderwidth=1)
        style.configure('Title.TLabel', background=self.colors['bg_primary'], foreground=self.colors['text_primary'], 
                       font=('Segoe UI', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['bg_primary'], foreground=self.colors['text_secondary'], 
                       font=('Segoe UI', 12))
        style.configure('Status.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], 
                       font=('Segoe UI', 10))
        style.configure('Modern.TButton', font=('Segoe UI', 11), padding=(20, 10))
        style.configure('Accent.TButton', background=self.colors['accent'], foreground='white', font=('Segoe UI', 11, 'bold'))
        
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
        
        # Left panel - Input and controls
        left_panel = ttk.Frame(content_frame, style='Card.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.create_input_panel(left_panel)
        
        # Right panel - Status and visualization
        right_panel = ttk.Frame(content_frame, style='Card.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        self.create_status_panel(right_panel)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title and subtitle with gradient effect
        title_label = ttk.Label(header_frame, text="🧠 Shadow AI", style='Title.TLabel')
        title_label.pack(anchor='center')
        
        subtitle_label = ttk.Label(header_frame, text="Universal AI Assistant with Advanced Capabilities", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(anchor='center')
        
        # Version and status info
        info_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        info_frame.pack(anchor='center', pady=(5, 0))
        
        version_label = ttk.Label(info_frame, text="v2.0 | Powered by Gemini AI", 
                                 font=('Segoe UI', 9), 
                                 background=self.colors['bg_primary'], 
                                 foreground=self.colors['text_secondary'])
        version_label.pack(side='left', padx=(0, 20))
        
        # Status indicator
        self.status_frame = ttk.Frame(info_frame, style='Modern.TFrame')
        self.status_frame.pack(side='left')
        
        self.status_indicator = tk.Canvas(self.status_frame, width=16, height=16, 
                                         bg=self.colors['bg_primary'], highlightthickness=0)
        self.status_indicator.pack(side='left', padx=(0, 8))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", style='Status.TLabel')
        self.status_label.pack(side='left')
        
        # Draw initial status indicator
        self.update_status_indicator('ready')
        
    def create_input_panel(self, parent):
        """Create the input and control panel"""
        # Panel title
        title_frame = ttk.Frame(parent, style='Card.TFrame')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(title_frame, text="💬 Command Center", 
                               font=('Segoe UI', 16, 'bold'), 
                               background=self.colors['bg_secondary'], 
                               foreground=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        # Input section
        input_frame = ttk.Frame(parent, style='Card.TFrame')
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Text input
        input_label = ttk.Label(input_frame, text="What would you like me to do?", 
                               font=('Segoe UI', 11), 
                               background=self.colors['bg_secondary'], 
                               foreground=self.colors['text_secondary'])
        input_label.pack(anchor='w', pady=(0, 5))
        
        self.command_entry = tk.Text(input_frame, height=3, font=('Segoe UI', 11), 
                                    bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], 
                                    insertbackground=self.colors['accent'], relief='flat', 
                                    wrap='word', padx=15, pady=10)
        self.command_entry.pack(fill='x', pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(input_frame, style='Card.TFrame')
        button_frame.pack(fill='x')
        
        self.execute_btn = tk.Button(button_frame, text="✨ Execute", 
                                    font=('Segoe UI', 11, 'bold'), 
                                    bg=self.colors['accent'], fg='white', 
                                    relief='flat', padx=30, pady=12,
                                    command=self.execute_command)
        self.execute_btn.pack(side='left', padx=(0, 10))
        
        self.voice_btn = tk.Button(button_frame, text="🎤 Voice", 
                                  font=('Segoe UI', 11), 
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], 
                                  relief='flat', padx=20, pady=12,
                                  command=self.toggle_voice_mode)
        self.voice_btn.pack(side='left', padx=(0, 10))
        
        self.clear_btn = tk.Button(button_frame, text="🗑️ Clear", 
                                  font=('Segoe UI', 11), 
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], 
                                  relief='flat', padx=20, pady=12,
                                  command=self.clear_input)
        self.clear_btn.pack(side='left')
        
        # Examples section
        examples_frame = ttk.Frame(parent, style='Card.TFrame')
        examples_frame.pack(fill='both', expand=True, padx=20, pady=(20, 20))
        
        examples_label = ttk.Label(examples_frame, text="💡 Example Commands", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  background=self.colors['bg_secondary'], 
                                  foreground=self.colors['text_primary'])
        examples_label.pack(anchor='w', pady=(0, 10))
        
        examples = [
            "Write an article about artificial intelligence",
            "Open Notepad and create a shopping list",
            "Search for the best laptops under $1000",
            "Create a professional email template",
            "Take a screenshot and save it to desktop",
            "Organize my Downloads folder by file type"
        ]
        
        self.examples_listbox = tk.Listbox(examples_frame, font=('Segoe UI', 10), 
                                          bg=self.colors['bg_tertiary'], 
                                          fg=self.colors['text_secondary'], 
                                          selectbackground=self.colors['accent'], 
                                          relief='flat', height=6)
        self.examples_listbox.pack(fill='both', expand=True)
        
        for example in examples:
            self.examples_listbox.insert(tk.END, f"  {example}")
        
        self.examples_listbox.bind('<Double-Button-1>', self.use_example)
        
    def create_status_panel(self, parent):
        """Create the status and visualization panel"""
        # Panel title
        title_frame = ttk.Frame(parent, style='Card.TFrame')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(title_frame, text="📊 Task Monitor", 
                               font=('Segoe UI', 16, 'bold'), 
                               background=self.colors['bg_secondary'], 
                               foreground=self.colors['text_primary'])
        title_label.pack(anchor='w')
        
        # Current task section
        task_frame = ttk.Frame(parent, style='Card.TFrame')
        task_frame.pack(fill='x', padx=20, pady=10)
        
        task_label = ttk.Label(task_frame, text="Current Task:", 
                              font=('Segoe UI', 11, 'bold'), 
                              background=self.colors['bg_secondary'], 
                              foreground=self.colors['text_secondary'])
        task_label.pack(anchor='w')
        
        self.current_task_label = ttk.Label(task_frame, text="Waiting for command...", 
                                           font=('Segoe UI', 11), 
                                           background=self.colors['bg_secondary'], 
                                           foreground=self.colors['text_primary'])
        self.current_task_label.pack(anchor='w', pady=(5, 0))
        
        # Progress section
        progress_frame = ttk.Frame(parent, style='Card.TFrame')
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        progress_label = ttk.Label(progress_frame, text="Progress:", 
                                  font=('Segoe UI', 11, 'bold'), 
                                  background=self.colors['bg_secondary'], 
                                  foreground=self.colors['text_secondary'])
        progress_label.pack(anchor='w')
        
        self.progress_canvas = tk.Canvas(progress_frame, height=20, 
                                        bg=self.colors['bg_tertiary'], 
                                        highlightthickness=0)
        self.progress_canvas.pack(fill='x', pady=(5, 0))
        
        # Activity log
        log_frame = ttk.Frame(parent, style='Card.TFrame')
        log_frame.pack(fill='both', expand=True, padx=20, pady=(20, 20))
        
        log_label = ttk.Label(log_frame, text="📝 Activity Log", 
                             font=('Segoe UI', 14, 'bold'), 
                             background=self.colors['bg_secondary'], 
                             foreground=self.colors['text_primary'])
        log_label.pack(anchor='w', pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
                                                 font=('Consolas', 10), 
                                                 bg=self.colors['bg_tertiary'], 
                                                 fg=self.colors['text_primary'], 
                                                 insertbackground=self.colors['accent'], 
                                                 relief='flat', wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # Add initial welcome message
        self.add_log_entry("🚀 Shadow AI initialized and ready!", "success")
        self.add_log_entry("💡 Try typing a command or click an example", "info")
        self.add_log_entry("🎤 Voice input available on demand", "info")
        
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
        """Update the status indicator color and animation"""
        self.status_indicator.delete("all")
        
        if status == 'ready':
            color = self.colors['success']
        elif status == 'processing':
            # Pulsing blue for processing
            import math
            alpha = (math.sin(self.pulse_value) + 1) / 2
            color = self.interpolate_color(self.colors['processing'], '#ffffff', alpha * 0.3)
        elif status == 'error':
            color = self.colors['error']
        elif status == 'warning':
            color = self.colors['warning']
        else:
            color = self.colors['text_secondary']
        
        self.status_indicator.create_oval(2, 2, 14, 14, fill=color, outline="")
        
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
        """Update the progress bar"""
        self.progress_canvas.delete("all")
        
        # Schedule update if canvas isn't ready
        if not hasattr(self, 'progress_canvas') or not self.progress_canvas.winfo_exists():
            self.root.after(50, lambda: self.update_progress(progress))
            return
            
        self.progress_canvas.update_idletasks()
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        if width > 1:  # Make sure canvas is initialized
            # Background
            self.progress_canvas.create_rectangle(0, 0, width, height, 
                                                fill=self.colors['bg_tertiary'], outline="")
            
            # Progress bar
            progress_width = width * (progress / 100)
            if progress_width > 0:
                self.progress_canvas.create_rectangle(0, 0, progress_width, height, 
                                                    fill=self.colors['accent'], outline="")
            
            # Progress text
            self.progress_canvas.create_text(width//2, height//2, 
                                           text=f"{progress:.1f}%", 
                                           fill=self.colors['text_primary'], 
                                           font=('Segoe UI', 9))
        
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
            self.voice_btn.config(text="🎤 Voice", bg=self.colors['bg_tertiary'])
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
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['bg_tertiary'])
        self.add_log_entry(f"🎤 Voice command received: {command}", "success")
        
        # Auto-execute voice command
        self.start_task_processing(command)
    
    def voice_input_failed(self):
        """Handle voice input failure"""
        self.voice_mode = False
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['bg_tertiary'])
        self.add_log_entry("🎤 No voice command detected", "warning")
    
    def voice_input_error(self, error):
        """Handle voice input error"""
        self.voice_mode = False
        self.voice_btn.config(text="🎤 Voice", bg=self.colors['bg_tertiary'])
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
        self.execute_btn.config(state='normal', text="✨ Execute")
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
        self.execute_btn.config(state='normal', text="✨ Execute")
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
        
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

def main():
    """Main entry point for the modern GUI"""
    app = ModernShadowGUI()
    app.run()

if __name__ == "__main__":
    main()
