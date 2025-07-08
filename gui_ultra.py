#!/usr/bin/env python3
"""
Shadow AI - Ultra Modern GUI
Advanced glassmorphism design with smooth animations and premium styling
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import time
import logging
from datetime import datetime
import sys
import os
import json
import math
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

class GlassMorphismFrame(tk.Frame):
    """Glassmorphism-style frame with blur effect simulation"""
    
    def __init__(self, parent, **kwargs):
        # Extract glassmorphism options
        glass_bg = kwargs.pop('glass_bg', '#FFFFFF80')
        border_color = kwargs.pop('border_color', '#FFFFFF30')
        
        super().__init__(parent, **kwargs)
        
        # Configure background with transparency simulation
        self.configure(bg='#F0F8FF', relief='flat', bd=1, highlightbackground=border_color, highlightthickness=1)

class AdvancedButton(tk.Button):
    """Advanced button with sophisticated animations and effects"""
    
    def __init__(self, parent, **kwargs):
        # Extract animation options
        self.gradient_start = kwargs.pop('gradient_start', '#667EEA')
        self.gradient_end = kwargs.pop('gradient_end', '#764BA2')
        self.hover_start = kwargs.pop('hover_start', '#5A6FDB')
        self.hover_end = kwargs.pop('hover_end', '#6B4895')
        self.click_color = kwargs.pop('click_color', '#4A5BC4')
        self.animation_speed = kwargs.pop('animation_speed', 10)
        
        # Default styling
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('borderwidth', 0)
        kwargs.setdefault('cursor', 'hand2')
        kwargs.setdefault('font', ('Segoe UI', 10, 'bold'))
        kwargs.setdefault('fg', 'white')
        
        super().__init__(parent, **kwargs)
        
        # Animation state
        self.animation_frame = 0
        self.is_hovering = False
        self.is_animating = False
        
        # Setup gradient background
        self.setup_gradient()
        
        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
    
    def setup_gradient(self):
        """Setup initial gradient background"""
        self.configure(bg=self.gradient_start)
    
    def on_enter(self, event):
        """Handle mouse enter with smooth animation"""
        self.is_hovering = True
        self.animate_to_hover()
    
    def on_leave(self, event):
        """Handle mouse leave with smooth animation"""
        self.is_hovering = False
        self.animate_to_normal()
    
    def on_click(self, event):
        """Handle button click with animation"""
        self.configure(bg=self.click_color)
        self.after(150, self.restore_hover_state)
    
    def on_release(self, event):
        """Handle button release"""
        pass
    
    def restore_hover_state(self):
        """Restore hover state after click"""
        if self.is_hovering:
            self.configure(bg=self.hover_start)
        else:
            self.configure(bg=self.gradient_start)
    
    def animate_to_hover(self):
        """Animate to hover state"""
        if not self.is_animating and self.is_hovering:
            self.is_animating = True
            self.animate_color_transition(self.gradient_start, self.hover_start, True)
    
    def animate_to_normal(self):
        """Animate to normal state"""
        if not self.is_animating and not self.is_hovering:
            self.is_animating = True
            self.animate_color_transition(self.hover_start, self.gradient_start, False)
    
    def animate_color_transition(self, start_color, end_color, to_hover):
        """Animate color transition"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        
        try:
            start_rgb = hex_to_rgb(start_color)
            end_rgb = hex_to_rgb(end_color)
            
            steps = 10
            current_step = 0
            
            def transition_step():
                nonlocal current_step
                if current_step >= steps:
                    self.is_animating = False
                    return
                
                if (to_hover and not self.is_hovering) or (not to_hover and self.is_hovering):
                    self.is_animating = False
                    return
                
                progress = current_step / steps
                current_rgb = tuple(
                    int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * progress)
                    for i in range(3)
                )
                
                self.configure(bg=rgb_to_hex(current_rgb))
                current_step += 1
                self.after(20, transition_step)
            
            transition_step()
        except:
            # Fallback to simple color change
            self.configure(bg=end_color)
            self.is_animating = False

class PulsingStatusIndicator(tk.Canvas):
    """Advanced pulsing status indicator with smooth animations"""
    
    def __init__(self, parent, size=24, **kwargs):
        super().__init__(parent, width=size, height=size, highlightthickness=0, **kwargs)
        
        self.size = size
        self.center = size // 2
        self.radius = (size - 8) // 2
        
        self.status = 'idle'
        self.animation_step = 0
        self.is_animating = False
        
        self.colors = {
            'idle': '#95A5A6',
            'processing': '#3498DB',
            'success': '#27AE60',
            'error': '#E74C3C',
            'warning': '#F39C12'
        }
        
        self.draw_indicator()
    
    def draw_indicator(self):
        """Draw the status indicator"""
        self.delete("all")
        
        if self.status == 'processing':
            self.draw_pulsing_circle()
        else:
            self.draw_static_circle()
    
    def draw_static_circle(self):
        """Draw static circle for non-processing states"""
        color = self.colors.get(self.status, '#95A5A6')
        
        # Main circle
        self.create_oval(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            fill=color,
            outline='',
            tags='indicator'
        )
        
        # Highlight for 3D effect
        self.create_oval(
            self.center - self.radius + 2,
            self.center - self.radius + 2,
            self.center - 2,
            self.center - 2,
            fill='white',
            outline='',
            stipple='gray25',
            tags='highlight'
        )
    
    def draw_pulsing_circle(self):
        """Draw pulsing animation for processing state"""
        base_color = self.colors['processing']
        
        # Calculate pulse intensity
        pulse = math.sin(self.animation_step * 0.2) * 0.5 + 0.5
        
        # Outer glow
        glow_radius = self.radius + int(pulse * 6)
        glow_alpha = int(50 * (1 - pulse))
        
        self.create_oval(
            self.center - glow_radius,
            self.center - glow_radius,
            self.center + glow_radius,
            self.center + glow_radius,
            fill='#87CEEB',
            outline='',
            tags='glow'
        )
        
        # Main circle
        self.create_oval(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            fill=base_color,
            outline='',
            tags='indicator'
        )
        
        # Inner highlight
        highlight_size = int(self.radius * (0.6 + pulse * 0.3))
        self.create_oval(
            self.center - highlight_size,
            self.center - highlight_size,
            self.center + highlight_size,
            self.center + highlight_size,
            fill='white',
            outline='',
            stipple='gray50',
            tags='highlight'
        )
    
    def set_status(self, status):
        """Set status and update indicator"""
        self.status = status
        
        if status == 'processing' and not self.is_animating:
            self.start_animation()
        elif status != 'processing':
            self.stop_animation()
        
        self.draw_indicator()
    
    def start_animation(self):
        """Start pulsing animation"""
        self.is_animating = True
        self.animate()
    
    def stop_animation(self):
        """Stop pulsing animation"""
        self.is_animating = False
    
    def animate(self):
        """Animation loop"""
        if not self.is_animating or self.status != 'processing':
            return
        
        self.animation_step += 1
        self.draw_indicator()
        self.after(50, self.animate)

class ModernCard(tk.Frame):
    """Ultra-modern card with glassmorphism effect"""
    
    def __init__(self, parent, title="", **kwargs):
        # Card styling options
        card_bg = kwargs.pop('card_bg', '#FFFFFF')
        shadow_color = kwargs.pop('shadow_color', '#00000010')
        border_radius = kwargs.pop('border_radius', 12)
        
        super().__init__(parent, bg=shadow_color, **kwargs)
        
        # Shadow layers for depth
        for i in range(3):
            shadow = tk.Frame(
                self,
                bg=shadow_color,
                height=2-i,
                relief='flat'
            )
            shadow.pack(side='bottom', fill='x', pady=(0, i))
        
        # Main content frame
        self.content_frame = tk.Frame(
            self,
            bg=card_bg,
            relief='flat',
            bd=0,
            padx=20,
            pady=15
        )
        self.content_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Title with modern typography
        if title:
            self.title_frame = tk.Frame(self.content_frame, bg=card_bg)
            self.title_frame.pack(fill='x', pady=(0, 15))
            
            self.title_label = tk.Label(
                self.title_frame,
                text=title,
                font=('Segoe UI', 14, 'bold'),
                bg=card_bg,
                fg='#2C3E50'
            )
            self.title_label.pack(side='left')
            
            # Decorative line
            line = tk.Frame(
                self.title_frame,
                height=2,
                bg='#E8EAF0'
            )
            line.pack(side='right', fill='x', expand=True, padx=(15, 0))

class ShadowAIUltraGUI:
    """Ultra-modern Shadow AI GUI with advanced animations and glassmorphism"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.shadow_ai = None
        self.voice_available = False
        
        # Animation state
        self.background_animation_step = 0
        
        self.setup_window()
        self.create_widgets()
        self.setup_shadow_ai()
        self.start_animations()
    
    def setup_window(self):
        """Configure main window with ultra-modern styling"""
        self.window.title("Shadow AI - Ultra Modern Interface")
        self.window.geometry("1400x900")
        self.window.minsize(1200, 800)
        
        # Modern color palette
        self.colors = {
            'primary': '#667EEA',
            'primary_dark': '#5A6FDB',
            'secondary': '#764BA2',
            'accent': '#F093FB',
            'success': '#4FACFE',
            'warning': '#FFB75E',
            'danger': '#ED4264',
            'background': '#F8FAFF',
            'background_alt': '#EDF2FF',
            'card': '#FFFFFF',
            'card_alt': '#FBFCFF',
            'text': '#2D3748',
            'text_light': '#718096',
            'text_lighter': '#A0AEC0',
            'border': '#E2E8F0',
            'shadow': '#E6FFFA'
        }
        
        # Gradient background
        self.setup_gradient_background()
        
        # Custom fonts
        self.setup_fonts()
        
        # Configure styles
        self.setup_advanced_styles()
    
    def setup_gradient_background(self):
        """Create animated gradient background"""
        self.bg_canvas = tk.Canvas(
            self.window,
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Start background animation
        self.animate_background()
    
    def setup_fonts(self):
        """Setup custom fonts"""
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'code': ('Consolas', 10)
        }
    
    def setup_advanced_styles(self):
        """Setup advanced TTK styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook style
        style.configure(
            'Ultra.TNotebook',
            background=self.colors['background'],
            borderwidth=0,
            focuscolor='none'
        )
        
        style.configure(
            'Ultra.TNotebook.Tab',
            background=self.colors['card'],
            foreground=self.colors['text'],
            padding=[25, 15],
            focuscolor='none',
            borderwidth=0
        )
        
        style.map(
            'Ultra.TNotebook.Tab',
            background=[
                ('selected', self.colors['primary']),
                ('active', self.colors['primary_dark'])
            ],
            foreground=[
                ('selected', 'white'),
                ('active', 'white')
            ]
        )
    
    def animate_background(self):
        """Animate the gradient background"""
        width = self.window.winfo_width() if self.window.winfo_width() > 1 else 1400
        height = self.window.winfo_height() if self.window.winfo_height() > 1 else 900
        
        self.bg_canvas.delete("all")
        
        # Create animated gradient
        step = self.background_animation_step
        
        # Multiple gradient layers for depth
        for i in range(5):
            offset = (step + i * 20) % 360
            
            # Calculate gradient colors
            r1 = int(102 + 50 * math.sin(math.radians(offset)))
            g1 = int(126 + 50 * math.sin(math.radians(offset + 120)))
            b1 = int(234 + 21 * math.sin(math.radians(offset + 240)))
            
            r2 = int(118 + 30 * math.sin(math.radians(offset + 180)))
            g2 = int(75 + 40 * math.sin(math.radians(offset + 300)))
            b2 = int(162 + 30 * math.sin(math.radians(offset + 60)))
            
            color1 = f"#{r1:02x}{g1:02x}{b1:02x}"
            color2 = f"#{r2:02x}{g2:02x}{b2:02x}"
            
            # Create gradient rectangles
            steps = 50
            for j in range(steps):
                y = (height * j) // steps
                next_y = (height * (j + 1)) // steps
                
                # Interpolate colors
                progress = j / steps
                r = int(r1 + (r2 - r1) * progress)
                g = int(g1 + (g2 - g1) * progress)
                b = int(b1 + (b2 - b1) * progress)
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                self.bg_canvas.create_rectangle(
                    0, y, width, next_y,
                    fill=color,
                    outline=color,
                    stipple=f"gray{10 + i * 5}"
                )
        
        self.background_animation_step = (self.background_animation_step + 1) % 360
        self.window.after(100, self.animate_background)
    
    def create_widgets(self):
        """Create ultra-modern widget layout"""
        # Main container with glassmorphism
        self.main_frame = GlassMorphismFrame(
            self.window,
            bg=self.colors['background']
        )
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        
        # Header
        self.create_ultra_header()
        
        # Content area
        self.create_ultra_content()
        
        # Footer
        self.create_ultra_footer()
    
    def create_ultra_header(self):
        """Create ultra-modern header"""
        header = ModernCard(
            self.main_frame,
            card_bg=self.colors['card'],
            height=120
        )
        header.pack(fill='x', padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        # Logo and title section
        title_section = tk.Frame(header.content_frame, bg=self.colors['card'])
        title_section.pack(side='left', fill='y', expand=True)
        
        # Main title with gradient effect
        title_frame = tk.Frame(title_section, bg=self.colors['card'])
        title_frame.pack(anchor='w', pady=(10, 5))
        
        title_label = tk.Label(
            title_frame,
            text="🚀 Shadow AI",
            font=self.fonts['title'],
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        title_label.pack(side='left')
        
        # Subtitle
        subtitle_label = tk.Label(
            title_section,
            text="Ultra Modern AI Assistant",
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(anchor='w')
        
        # Status panel
        self.create_status_panel(header.content_frame)
    
    def create_status_panel(self, parent):
        """Create advanced status panel"""
        status_panel = tk.Frame(parent, bg=self.colors['card'])
        status_panel.pack(side='right', fill='y', padx=(20, 0))
        
        # Status grid
        status_items = [
            ("AI Engine", "ai_status"),
            ("Voice Recognition", "voice_status"),
            ("System Monitor", "system_status")
        ]
        
        for i, (label, attr) in enumerate(status_items):
            item_frame = tk.Frame(status_panel, bg=self.colors['card'])
            item_frame.grid(row=i, column=0, sticky='w', pady=5, padx=10)
            
            # Advanced status indicator
            indicator = PulsingStatusIndicator(
                item_frame,
                size=20,
                bg=self.colors['card']
            )
            indicator.pack(side='left', padx=(0, 10))
            setattr(self, attr, indicator)
            
            # Status label
            tk.Label(
                item_frame,
                text=label,
                font=self.fonts['small'],
                bg=self.colors['card'],
                fg=self.colors['text']
            ).pack(side='left')
    
    def create_ultra_content(self):
        """Create ultra-modern content area"""
        content_card = ModernCard(
            self.main_frame,
            card_bg=self.colors['card']
        )
        content_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create notebook
        self.notebook = ttk.Notebook(
            content_card.content_frame,
            style='Ultra.TNotebook'
        )
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_chat_interface()
        self.create_control_center()
        self.create_analytics_tab()
        self.create_settings_tab()
    
    def create_chat_interface(self):
        """Create ultra-modern chat interface"""
        chat_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(chat_frame, text="💬 Chat Interface")
        
        # Chat layout
        chat_container = tk.Frame(chat_frame, bg=self.colors['background'])
        chat_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Chat display area
        chat_display_card = ModernCard(
            chat_container,
            title="Conversation History",
            card_bg=self.colors['card']
        )
        chat_display_card.pack(fill='both', expand=True, pady=(0, 15))
        
        # Ultra-modern chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_display_card.content_frame,
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief='flat',
            borderwidth=0,
            state='disabled',
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Input area
        self.create_input_area(chat_container)
    
    def create_input_area(self, parent):
        """Create ultra-modern input area"""
        input_card = ModernCard(
            parent,
            title="Command Input",
            card_bg=self.colors['card'],
            height=150
        )
        input_card.pack(fill='x')
        input_card.pack_propagate(False)
        
        # Text input with modern styling
        input_frame = tk.Frame(input_card.content_frame, bg=self.colors['card'])
        input_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Input text area
        self.text_input = tk.Text(
            input_frame,
            height=3,
            font=self.fonts['body'],
            bg=self.colors['background'],
            fg=self.colors['text'],
            relief='flat',
            borderwidth=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary'],
            highlightthickness=2,
            wrap=tk.WORD,
            padx=15,
            pady=10
        )
        self.text_input.pack(fill='both', expand=True, pady=(0, 15))
        self.text_input.bind('<Return>', self.on_enter_pressed)
        
        # Control buttons
        self.create_control_buttons(input_card.content_frame)
    
    def create_control_buttons(self, parent):
        """Create ultra-modern control buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(fill='x')
        
        # Send button
        self.send_btn = AdvancedButton(
            button_frame,
            text="🚀 Send Command",
            gradient_start=self.colors['primary'],
            gradient_end=self.colors['primary_dark'],
            hover_start=self.colors['primary_dark'],
            hover_end=self.colors['secondary'],
            command=self.send_text_command,
            font=self.fonts['subheading'],
            padx=30,
            pady=12
        )
        self.send_btn.pack(side='right', padx=(10, 0))
        
        # Voice button
        self.voice_btn = AdvancedButton(
            button_frame,
            text="🎤 Voice Input",
            gradient_start=self.colors['success'],
            gradient_end='#0093E9',
            hover_start='#0093E9',
            hover_end=self.colors['success'],
            command=self.send_voice_command,
            font=self.fonts['subheading'],
            padx=30,
            pady=12
        )
        self.voice_btn.pack(side='right', padx=(10, 0))
        
        # Clear button
        clear_btn = AdvancedButton(
            button_frame,
            text="🗑️ Clear",
            gradient_start=self.colors['text_light'],
            gradient_end=self.colors['text_lighter'],
            hover_start=self.colors['text_lighter'],
            hover_end=self.colors['text_light'],
            command=self.clear_chat,
            font=self.fonts['body'],
            padx=20,
            pady=12
        )
        clear_btn.pack(side='left')
    
    def create_control_center(self):
        """Create ultra-modern control center"""
        control_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(control_frame, text="🎛️ Control Center")
        
        # Add control center content
        tk.Label(
            control_frame,
            text="Advanced Control Center",
            font=self.fonts['heading'],
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(pady=50)
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        analytics_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        # Add analytics content
        tk.Label(
            analytics_frame,
            text="System Analytics & Monitoring",
            font=self.fonts['heading'],
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(pady=50)
    
    def create_settings_tab(self):
        """Create ultra-modern settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Add settings content
        tk.Label(
            settings_frame,
            text="Advanced Configuration",
            font=self.fonts['heading'],
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(pady=50)
    
    def create_ultra_footer(self):
        """Create ultra-modern footer"""
        footer = ModernCard(
            self.main_frame,
            card_bg=self.colors['card'],
            height=60
        )
        footer.pack(fill='x', padx=20, pady=(10, 20))
        footer.pack_propagate(False)
        
        # Status
        self.status_label = tk.Label(
            footer.content_frame,
            text="Ready for commands",
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        self.status_label.pack(side='left', pady=15)
        
        # Time
        self.time_label = tk.Label(
            footer.content_frame,
            text="",
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        self.time_label.pack(side='right', pady=15)
    
    def setup_shadow_ai(self):
        """Initialize Shadow AI"""
        try:
            if ShadowAI:
                self.shadow_ai = ShadowAI()
                self.ai_status.set_status('success')
                self.update_status("✅ Shadow AI initialized successfully")
            else:
                self.ai_status.set_status('error')
                self.update_status("❌ Shadow AI not available")
        except Exception as e:
            self.ai_status.set_status('error')
            self.update_status(f"❌ Error initializing AI: {e}")
        
        # Voice setup
        if VOICE_ENABLED:
            self.voice_available = True
            self.voice_status.set_status('success')
        else:
            self.voice_available = False
            self.voice_status.set_status('error')
            self.voice_btn.configure(state='disabled')
        
        # System status
        self.system_status.set_status('success')
    
    def start_animations(self):
        """Start all animations"""
        self.update_time()
        self.window.after(1000, self.start_animations)
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(self, 'time_label'):
            self.time_label.configure(text=current_time)
        self.window.after(1000, self.update_time)
    
    def update_status(self, message):
        """Update status message"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
    
    def on_enter_pressed(self, event):
        """Handle Enter key"""
        if event.state & 0x4:  # Ctrl+Enter
            return
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
            messagebox.showerror("Error", "Voice recognition not available")
            return
        
        self.voice_btn.configure(text="🎤 Listening...")
        self.voice_status.set_status('processing')
        
        def voice_thread():
            try:
                from input.voice_input import get_voice_input
                command = get_voice_input()
                if command:
                    self.window.after(0, lambda: self.add_chat_message(f"You (voice): {command}", 'user'))
                    self.window.after(0, lambda: self.process_command(command))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Voice Error", str(e)))
            finally:
                self.window.after(0, lambda: self.voice_btn.configure(text="🎤 Voice Input"))
                self.window.after(0, lambda: self.voice_status.set_status('success'))
        
        threading.Thread(target=voice_thread, daemon=True).start()
    
    def process_command(self, command):
        """Process command"""
        if not self.shadow_ai:
            self.add_chat_message("❌ Shadow AI not available", 'error')
            return
        
        self.ai_status.set_status('processing')
        
        def process_thread():
            try:
                response = self.shadow_ai.process_command(command)
                self.window.after(0, lambda: self.add_chat_message(f"🤖 Shadow AI: {response}", 'assistant'))
            except Exception as e:
                self.window.after(0, lambda: self.add_chat_message(f"❌ Error: {e}", 'error'))
            finally:
                self.window.after(0, lambda: self.ai_status.set_status('success'))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def add_chat_message(self, message, msg_type='info'):
        """Add message to chat"""
        self.chat_display.configure(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert('end', f"[{timestamp}] {message}\n\n")
        
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', 'end')
        self.chat_display.configure(state='disabled')
    
    def run(self):
        """Start the ultra GUI"""
        self.window.mainloop()

def main():
    """Main function"""
    try:
        app = ShadowAIUltraGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Shadow AI Ultra GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
