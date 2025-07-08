#!/usr/bin/env python3
"""
Shadow AI - Cyberpunk Dark GUI
Futuristic dark theme with neon accents and sci-fi styling
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import logging
from datetime import datetime
import sys
import os
import math
import random
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

class NeonButton(tk.Button):
    """Cyberpunk-style neon button with glow effects"""
    
    def __init__(self, parent, **kwargs):
        # Extract neon options
        self.neon_color = kwargs.pop('neon_color', '#00FF41')
        self.glow_color = kwargs.pop('glow_color', '#004D1A')
        self.dark_bg = kwargs.pop('dark_bg', '#0A0A0A')
        
        # Default cyberpunk styling
        kwargs.setdefault('bg', self.dark_bg)
        kwargs.setdefault('fg', self.neon_color)
        kwargs.setdefault('activebackground', self.glow_color)
        kwargs.setdefault('activeforeground', '#00FF41')
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('borderwidth', 2)
        kwargs.setdefault('highlightbackground', self.neon_color)
        kwargs.setdefault('highlightcolor', self.neon_color)
        kwargs.setdefault('highlightthickness', 1)
        kwargs.setdefault('font', ('Consolas', 10, 'bold'))
        kwargs.setdefault('cursor', 'hand2')
        
        super().__init__(parent, **kwargs)
        
        # Animation state
        self.glow_intensity = 0
        self.is_glowing = False
        
        # Bind events
        self.bind('<Enter>', self.start_glow)
        self.bind('<Leave>', self.stop_glow)
        self.bind('<Button-1>', self.on_click)
    
    def start_glow(self, event=None):
        """Start glow animation"""
        self.is_glowing = True
        self.animate_glow()
    
    def stop_glow(self, event=None):
        """Stop glow animation"""
        self.is_glowing = False
        self.configure(bg=self.dark_bg, highlightthickness=1)
    
    def animate_glow(self):
        """Animate glow effect"""
        if not self.is_glowing:
            return
        
        self.glow_intensity = (self.glow_intensity + 0.1) % (2 * math.pi)
        intensity = (math.sin(self.glow_intensity) + 1) / 2
        
        # Calculate glow color
        glow_alpha = int(100 + 155 * intensity)
        glow_hex = f"#{0:02x}{glow_alpha:02x}{65:02x}"
        
        # Update appearance
        self.configure(
            bg=glow_hex,
            highlightthickness=int(2 + 3 * intensity)
        )
        
        self.after(50, self.animate_glow)
    
    def on_click(self, event):
        """Handle click with flash effect"""
        self.configure(bg='#00FF41')
        self.after(100, lambda: self.configure(bg=self.dark_bg))

class CyberpunkPanel(tk.Frame):
    """Cyberpunk-style panel with neon borders"""
    
    def __init__(self, parent, title="", **kwargs):
        # Panel options
        neon_color = kwargs.pop('neon_color', '#00FF41')
        dark_bg = kwargs.pop('dark_bg', '#0D0D0D')
        
        super().__init__(parent, bg=dark_bg, **kwargs)
        
        # Neon border effect
        self.border_frame = tk.Frame(
            self,
            bg=neon_color,
            height=2
        )
        self.border_frame.pack(fill='x')
        
        # Title bar
        if title:
            title_frame = tk.Frame(self, bg=dark_bg, height=40)
            title_frame.pack(fill='x')
            title_frame.pack_propagate(False)
            
            # Title with cyberpunk font
            title_label = tk.Label(
                title_frame,
                text=f">>> {title.upper()}",
                font=('Consolas', 12, 'bold'),
                bg=dark_bg,
                fg=neon_color
            )
            title_label.pack(side='left', padx=15, pady=10)
            
            # Decorative elements
            for i in range(3):
                dot = tk.Label(
                    title_frame,
                    text="●",
                    font=('Consolas', 8),
                    bg=dark_bg,
                    fg=neon_color
                )
                dot.pack(side='right', padx=2, pady=10)
        
        # Content area
        self.content_frame = tk.Frame(self, bg=dark_bg)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)

class MatrixRain(tk.Canvas):
    """Matrix-style digital rain effect"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.width = kwargs.get('width', 200)
        self.height = kwargs.get('height', 400)
        self.columns = self.width // 15
        self.drops = [0] * self.columns
        
        self.characters = "01"
        self.is_running = False
        
        self.start_rain()
    
    def start_rain(self):
        """Start the matrix rain effect"""
        self.is_running = True
        self.rain_step()
    
    def stop_rain(self):
        """Stop the matrix rain effect"""
        self.is_running = False
    
    def rain_step(self):
        """Single step of rain animation"""
        if not self.is_running:
            return
        
        # Clear canvas
        self.delete("all")
        
        # Draw characters
        for i in range(self.columns):
            char = random.choice(self.characters)
            x = i * 15
            y = self.drops[i] * 20
            
            # Green gradient effect
            if y < self.height:
                alpha = max(0, 255 - (y % 200))
                color = f"#{0:02x}{alpha:02x}{0:02x}"
                
                self.create_text(
                    x, y,
                    text=char,
                    fill=color,
                    font=('Consolas', 12, 'bold')
                )
            
            # Reset drop if it goes off screen
            if self.drops[i] * 20 > self.height and random.random() > 0.975:
                self.drops[i] = 0
            
            self.drops[i] += 1
        
        self.after(100, self.rain_step)

class CyberpunkProgressBar(tk.Canvas):
    """Cyberpunk-style animated progress bar"""
    
    def __init__(self, parent, **kwargs):
        self.width = kwargs.get('width', 300)
        self.height = kwargs.get('height', 20)
        
        super().__init__(parent, width=self.width, height=self.height, 
                        bg='#000000', highlightthickness=0, **kwargs)
        
        self.progress = 0
        self.is_animating = False
        self.animation_step = 0
    
    def set_progress(self, progress):
        """Set progress value (0-100)"""
        self.progress = max(0, min(100, progress))
        self.draw_progress()
    
    def start_animation(self):
        """Start pulsing animation"""
        self.is_animating = True
        self.animate()
    
    def stop_animation(self):
        """Stop pulsing animation"""
        self.is_animating = False
    
    def draw_progress(self):
        """Draw the progress bar"""
        self.delete("all")
        
        # Background
        self.create_rectangle(2, 2, self.width-2, self.height-2, 
                            fill='#0D0D0D', outline='#00FF41', width=1)
        
        # Progress fill
        if self.progress > 0:
            fill_width = int((self.width - 4) * self.progress / 100)
            
            # Gradient effect
            for i in range(fill_width):
                alpha = int(100 + 155 * (i / fill_width))
                color = f"#{0:02x}{alpha:02x}{0:02x}"
                
                self.create_line(
                    3 + i, 3,
                    3 + i, self.height - 3,
                    fill=color,
                    width=1
                )
        
        # Scanning line animation
        if self.is_animating:
            scan_pos = (self.animation_step % 100) / 100 * (self.width - 4)
            self.create_line(
                3 + scan_pos, 3,
                3 + scan_pos, self.height - 3,
                fill='#00FFFF',
                width=2
            )
    
    def animate(self):
        """Animation loop"""
        if not self.is_animating:
            return
        
        self.animation_step += 2
        self.draw_progress()
        self.after(50, self.animate)

class ShadowAICyberpunkGUI:
    """Cyberpunk-themed Shadow AI GUI"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.shadow_ai = None
        self.voice_available = False
        
        # Cyberpunk color scheme
        self.colors = {
            'bg_primary': '#000000',
            'bg_secondary': '#0D0D0D',
            'bg_tertiary': '#1A1A1A',
            'neon_green': '#00FF41',
            'neon_blue': '#0099FF',
            'neon_cyan': '#00FFFF',
            'neon_purple': '#9900FF',
            'neon_red': '#FF0040',
            'neon_yellow': '#FFFF00',
            'text_primary': '#00FF41',
            'text_secondary': '#00CC33',
            'text_muted': '#004D1A'
        }
        
        self.setup_window()
        self.create_widgets()
        self.setup_shadow_ai()
        self.start_effects()
    
    def setup_window(self):
        """Configure main window with cyberpunk theme"""
        self.window.title("Shadow AI - Cyberpunk Interface")
        self.window.geometry("1300x800")
        self.window.minsize(1100, 700)
        self.window.configure(bg=self.colors['bg_primary'])
        
        # Set window to appear on top and center
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))
    
    def create_widgets(self):
        """Create cyberpunk-themed widgets"""
        # Main container
        main_frame = tk.Frame(self.window, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left panel - Matrix effects
        self.create_left_panel(content_frame)
        
        # Center panel - Main interface
        self.create_center_panel(content_frame)
        
        # Right panel - Status and controls
        self.create_right_panel(content_frame)
        
        # Footer
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create cyberpunk header"""
        header = CyberpunkPanel(
            parent,
            title="SHADOW AI CYBERPUNK INTERFACE",
            neon_color=self.colors['neon_green'],
            dark_bg=self.colors['bg_secondary'],
            height=80
        )
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)
        
        # ASCII art logo
        logo_text = """
╔═╗╦ ╦╔═╗╔╦╗╔═╗╦ ╦  ╔═╗╦
╚═╗╠═╣╠═╣ ║║║ ║║║║  ╠═╣║
╚═╝╩ ╩╩ ╩═╩╝╚═╝╚╩╝  ╩ ╩╩
        """
        
        logo_label = tk.Label(
            header.content_frame,
            text=logo_text,
            font=('Consolas', 8, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_green'],
            justify='left'
        )
        logo_label.pack(side='left', padx=10)
        
        # Status indicators
        status_frame = tk.Frame(header.content_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(side='right', padx=20)
        
        # System status
        self.create_status_displays(status_frame)
    
    def create_status_displays(self, parent):
        """Create cyberpunk status displays"""
        status_items = [
            ("AI_CORE", "ai_status"),
            ("VOICE_SYS", "voice_status"),
            ("NET_LINK", "network_status")
        ]
        
        for i, (label, attr) in enumerate(status_items):
            frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
            frame.grid(row=i, column=0, sticky='w', pady=2)
            
            # Status label
            tk.Label(
                frame,
                text=f"{label}:",
                font=('Consolas', 9, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).pack(side='left')
            
            # Status indicator
            status_label = tk.Label(
                frame,
                text="[OFFLINE]",
                font=('Consolas', 9, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['neon_red']
            )
            status_label.pack(side='left', padx=(10, 0))
            setattr(self, attr, status_label)
    
    def create_left_panel(self, parent):
        """Create left panel with matrix effects"""
        left_frame = tk.Frame(parent, bg=self.colors['bg_primary'], width=200)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Matrix rain effect
        self.matrix_rain = MatrixRain(
            left_frame,
            width=200,
            height=500,
            bg=self.colors['bg_primary']
        )
        self.matrix_rain.pack(fill='both', expand=True)
    
    def create_center_panel(self, parent):
        """Create center panel with main interface"""
        center_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        center_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Chat interface
        chat_panel = CyberpunkPanel(
            center_frame,
            title="NEURAL INTERFACE",
            neon_color=self.colors['neon_cyan'],
            dark_bg=self.colors['bg_secondary']
        )
        chat_panel.pack(fill='both', expand=True, pady=(0, 10))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_panel.content_frame,
            font=('Consolas', 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_green'],
            insertbackground=self.colors['neon_green'],
            relief='flat',
            borderwidth=0,
            state='disabled',
            wrap=tk.WORD
        )
        self.chat_display.pack(fill='both', expand=True, pady=(0, 10))
        
        # Input area
        self.create_input_area(chat_panel.content_frame)
    
    def create_input_area(self, parent):
        """Create cyberpunk input area"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Command prompt label
        prompt_label = tk.Label(
            input_frame,
            text="root@shadow-ai:~$",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_green']
        )
        prompt_label.pack(side='left', padx=(0, 10))
        
        # Input field
        self.text_input = tk.Entry(
            input_frame,
            font=('Consolas', 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_green'],
            insertbackground=self.colors['neon_green'],
            relief='flat',
            borderwidth=2,
            highlightbackground=self.colors['neon_green'],
            highlightcolor=self.colors['neon_cyan'],
            highlightthickness=1
        )
        self.text_input.pack(fill='x', expand=True, pady=2)
        self.text_input.bind('<Return>', self.send_command)
        
        # Control buttons
        button_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x')
        
        # Execute button
        self.execute_btn = NeonButton(
            button_frame,
            text=">>> EXECUTE",
            neon_color=self.colors['neon_green'],
            command=self.send_command,
            padx=20,
            pady=5
        )
        self.execute_btn.pack(side='left', padx=(0, 10))
        
        # Voice button
        self.voice_btn = NeonButton(
            button_frame,
            text="VOICE_INPUT",
            neon_color=self.colors['neon_blue'],
            command=self.voice_command,
            padx=20,
            pady=5
        )
        self.voice_btn.pack(side='left', padx=(0, 10))
        
        # Clear button
        clear_btn = NeonButton(
            button_frame,
            text="CLEAR",
            neon_color=self.colors['neon_red'],
            command=self.clear_terminal,
            padx=20,
            pady=5
        )
        clear_btn.pack(side='left')
    
    def create_right_panel(self, parent):
        """Create right panel with system info"""
        right_frame = tk.Frame(parent, bg=self.colors['bg_primary'], width=300)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # System monitor
        monitor_panel = CyberpunkPanel(
            right_frame,
            title="SYSTEM MONITOR",
            neon_color=self.colors['neon_purple'],
            dark_bg=self.colors['bg_secondary']
        )
        monitor_panel.pack(fill='x', pady=(0, 10))
        
        # Progress bars
        self.create_progress_monitors(monitor_panel.content_frame)
        
        # Activity log
        activity_panel = CyberpunkPanel(
            right_frame,
            title="ACTIVITY LOG",
            neon_color=self.colors['neon_yellow'],
            dark_bg=self.colors['bg_secondary']
        )
        activity_panel.pack(fill='both', expand=True)
        
        # Activity display
        self.activity_log = scrolledtext.ScrolledText(
            activity_panel.content_frame,
            height=15,
            font=('Consolas', 8),
            bg=self.colors['bg_primary'],
            fg=self.colors['neon_yellow'],
            relief='flat',
            borderwidth=0,
            state='disabled'
        )
        self.activity_log.pack(fill='both', expand=True)
    
    def create_progress_monitors(self, parent):
        """Create cyberpunk progress monitors"""
        monitors = [
            ("CPU_USAGE", "cpu_bar"),
            ("MEM_USAGE", "mem_bar"),
            ("AI_LOAD", "ai_bar")
        ]
        
        for label, attr in monitors:
            frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
            frame.pack(fill='x', pady=5)
            
            # Label
            tk.Label(
                frame,
                text=f"{label}:",
                font=('Consolas', 9, 'bold'),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary']
            ).pack(anchor='w')
            
            # Progress bar
            progress_bar = CyberpunkProgressBar(
                frame,
                width=250,
                height=15,
                bg=self.colors['bg_secondary']
            )
            progress_bar.pack(pady=(2, 0))
            setattr(self, attr, progress_bar)
    
    def create_footer(self, parent):
        """Create cyberpunk footer"""
        footer = tk.Frame(parent, bg=self.colors['bg_secondary'], height=40)
        footer.pack(fill='x', pady=(10, 0))
        footer.pack_propagate(False)
        
        # Status message
        self.status_label = tk.Label(
            footer,
            text=">>> SYSTEM READY",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_green']
        )
        self.status_label.pack(side='left', padx=15, pady=10)
        
        # Time display
        self.time_label = tk.Label(
            footer,
            text="",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['neon_cyan']
        )
        self.time_label.pack(side='right', padx=15, pady=10)
    
    def setup_shadow_ai(self):
        """Initialize Shadow AI with cyberpunk status"""
        try:
            if ShadowAI:
                self.shadow_ai = ShadowAI()
                self.ai_status.configure(text="[ONLINE]", fg=self.colors['neon_green'])
                self.log_activity(">>> AI_CORE: INITIALIZATION COMPLETE")
            else:
                self.ai_status.configure(text="[ERROR]", fg=self.colors['neon_red'])
                self.log_activity(">>> AI_CORE: INITIALIZATION FAILED")
        except Exception as e:
            self.ai_status.configure(text="[ERROR]", fg=self.colors['neon_red'])
            self.log_activity(f">>> AI_CORE: ERROR - {e}")
        
        # Voice setup
        if VOICE_ENABLED:
            self.voice_available = True
            self.voice_status.configure(text="[ONLINE]", fg=self.colors['neon_green'])
            self.log_activity(">>> VOICE_SYS: READY")
        else:
            self.voice_available = False
            self.voice_status.configure(text="[OFFLINE]", fg=self.colors['neon_red'])
            self.voice_btn.configure(state='disabled')
            self.log_activity(">>> VOICE_SYS: DISABLED")
        
        # Network status
        self.network_status.configure(text="[ONLINE]", fg=self.colors['neon_green'])
        self.log_activity(">>> NET_LINK: ESTABLISHED")
    
    def start_effects(self):
        """Start all cyberpunk effects"""
        # Start progress bar animations
        self.cpu_bar.start_animation()
        self.mem_bar.start_animation()
        self.ai_bar.start_animation()
        
        # Set initial values
        self.cpu_bar.set_progress(35)
        self.mem_bar.set_progress(60)
        self.ai_bar.set_progress(85)
        
        # Start time updates
        self.update_time()
        
        # Start system monitoring
        self.monitor_system()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"TIME: {current_time}")
        self.window.after(1000, self.update_time)
    
    def monitor_system(self):
        """Monitor system with random updates"""
        # Random progress updates
        self.cpu_bar.set_progress(random.randint(20, 80))
        self.mem_bar.set_progress(random.randint(40, 90))
        self.ai_bar.set_progress(random.randint(70, 100))
        
        self.window.after(5000, self.monitor_system)
    
    def send_command(self, event=None):
        """Send command to AI"""
        command = self.text_input.get().strip()
        if not command:
            return
        
        self.text_input.delete(0, 'end')
        self.add_terminal_output(f"root@shadow-ai:~$ {command}")
        self.log_activity(f">>> COMMAND: {command}")
        
        if self.shadow_ai:
            self.process_command(command)
        else:
            self.add_terminal_output("ERROR: AI_CORE not available")
    
    def voice_command(self):
        """Handle voice command"""
        if not self.voice_available:
            self.add_terminal_output("ERROR: VOICE_SYS offline")
            return
        
        self.voice_btn.configure(text="LISTENING...")
        self.log_activity(">>> VOICE_SYS: LISTENING")
        
        def voice_thread():
            try:
                from input.voice_input import get_voice_input
                command = get_voice_input()
                if command:
                    self.window.after(0, lambda: self.add_terminal_output(f"VOICE: {command}"))
                    self.window.after(0, lambda: self.process_command(command))
            except Exception as e:
                self.window.after(0, lambda: self.add_terminal_output(f"VOICE_ERROR: {e}"))
            finally:
                self.window.after(0, lambda: self.voice_btn.configure(text="VOICE_INPUT"))
        
        threading.Thread(target=voice_thread, daemon=True).start()
    
    def process_command(self, command):
        """Process AI command"""
        self.ai_bar.set_progress(100)
        self.status_label.configure(text=">>> PROCESSING...")
        
        def process_thread():
            try:
                response = self.shadow_ai.process_command(command)
                self.window.after(0, lambda: self.add_terminal_output(f"AI: {response}"))
                self.window.after(0, lambda: self.log_activity(f">>> AI_RESPONSE: {response[:50]}..."))
            except Exception as e:
                self.window.after(0, lambda: self.add_terminal_output(f"AI_ERROR: {e}"))
                self.window.after(0, lambda: self.log_activity(f">>> AI_ERROR: {e}"))
            finally:
                self.window.after(0, lambda: self.status_label.configure(text=">>> SYSTEM READY"))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def add_terminal_output(self, text):
        """Add output to terminal"""
        self.chat_display.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert('end', f"[{timestamp}] {text}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')
    
    def log_activity(self, message):
        """Log activity"""
        self.activity_log.configure(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.insert('end', f"[{timestamp}] {message}\n")
        self.activity_log.configure(state='disabled')
        self.activity_log.see('end')
    
    def clear_terminal(self):
        """Clear terminal output"""
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', 'end')
        self.chat_display.configure(state='disabled')
        self.log_activity(">>> TERMINAL: CLEARED")
    
    def run(self):
        """Start the cyberpunk GUI"""
        self.window.mainloop()

def main():
    """Main function"""
    try:
        app = ShadowAICyberpunkGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Shadow AI Cyberpunk GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
