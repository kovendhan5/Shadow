#!/usr/bin/env python3
"""
Shadow AI - Enhanced Ultra Modern GUI
The most advanced, animated, and visually stunning interface for Shadow AI
Features: particle effects, advanced animations, holographic elements, dynamic themes
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
from typing import Dict, Any, Optional, List
import logging
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import ShadowAI
    from config import VOICE_ENABLED
    SHADOW_AI_AVAILABLE = True
except ImportError as e:
    logging.error(f"Import error: {e}")
    SHADOW_AI_AVAILABLE = False
    VOICE_ENABLED = False

# Lazy import voice functionality
VOICE_AVAILABLE = False
_voice_module = None

def lazy_import_voice():
    global VOICE_AVAILABLE, _voice_module
    if _voice_module is None and VOICE_ENABLED:
        try:
            from input import voice_input
            _voice_module = voice_input
            VOICE_AVAILABLE = True
        except:
            VOICE_AVAILABLE = False
    return VOICE_AVAILABLE

class Particle:
    """Individual particle for particle effects"""
    def __init__(self, x, y, vx=None, vy=None, life=100, color="#4ecdc4"):
        self.x = x
        self.y = y
        self.vx = vx or random.uniform(-2, 2)
        self.vy = vy or random.uniform(-2, 2)
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.uniform(1, 3)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # Gravity
        self.life -= 1
        return self.life > 0
    
    def get_alpha(self):
        return self.life / self.max_life

class ParticleSystem:
    """Advanced particle system for visual effects"""
    def __init__(self, canvas, max_particles=50):
        self.canvas = canvas
        self.particles = []
        self.max_particles = max_particles
    
    def add_particle(self, x, y, **kwargs):
        if len(self.particles) < self.max_particles:
            self.particles.append(Particle(x, y, **kwargs))
    
    def add_burst(self, x, y, count=10, **kwargs):
        """Add a burst of particles"""
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-3, 3)
            self.add_particle(x, y, vx=vx, vy=vy, **kwargs)
    
    def update(self):
        """Update all particles and remove dead ones"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self):
        """Draw all particles"""
        for particle in self.particles:
            alpha = particle.get_alpha()
            if alpha > 0:
                # Calculate color with alpha
                color = particle.color
                size = particle.size * alpha
                self.canvas.create_oval(
                    particle.x - size, particle.y - size,
                    particle.x + size, particle.y + size,
                    fill=color, outline="", tags="particle"
                )

class HolographicButton(tk.Canvas):
    """Advanced holographic-style button with glow effects"""
    def __init__(self, parent, text, command=None, width=200, height=60, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.is_hovered = False
        self.is_pressed = False
        self.glow_intensity = 0
        self.pulse_phase = 0
        
        # Configure colors
        self.bg_color = "#0f1419"
        self.border_color = "#4ecdc4"
        self.glow_color = "#00ffff"
        self.text_color = "#ffffff"
        
        self.configure(bg=self.bg_color)
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button()
        self.start_animation()
    
    def draw_button(self):
        """Draw the holographic button"""
        self.delete("all")
        
        # Calculate glow effect
        glow_offset = int(self.glow_intensity * 5)
        pulse_offset = int(math.sin(self.pulse_phase) * 2)
        
        # Background with glow
        for i in range(glow_offset, 0, -1):
            alpha = (glow_offset - i) / glow_offset * 0.3
            color = self.glow_color if self.is_hovered else self.border_color
            self.create_rectangle(
                5 - i, 5 - i, self.width - 5 + i, self.height - 5 + i,
                outline=color, width=1, tags="glow"
            )
        
        # Main button border
        border_width = 2 + pulse_offset
        self.create_rectangle(
            5, 5, self.width - 5, self.height - 5,
            outline=self.border_color, width=border_width, tags="border"
        )
        
        # Inner gradient effect
        for i in range(5):
            alpha = (5 - i) / 5 * 0.1
            self.create_rectangle(
                5 + i, 5 + i, self.width - 5 - i, self.height - 5 - i,
                outline=self.border_color, width=1, tags="gradient"
            )
        
        # Text with glow
        text_y = self.height // 2
        text_color = self.glow_color if self.is_hovered else self.text_color
        
        # Text shadow/glow
        if self.is_hovered:
            for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                self.create_text(
                    self.width // 2 + offset[0], text_y + offset[1],
                    text=self.text, fill=self.glow_color, font=("Arial", 11, "bold"),
                    tags="text_glow"
                )
        
        # Main text
        self.create_text(
            self.width // 2, text_y,
            text=self.text, fill=text_color, font=("Arial", 12, "bold"),
            tags="text"
        )
    
    def on_enter(self, event):
        self.is_hovered = True
        self.animate_glow_in()
    
    def on_leave(self, event):
        self.is_hovered = False
        self.animate_glow_out()
    
    def on_press(self, event):
        self.is_pressed = True
        if self.command:
            self.command()
    
    def on_release(self, event):
        self.is_pressed = False
    
    def animate_glow_in(self):
        """Animate glow effect in"""
        if self.glow_intensity < 1.0:
            self.glow_intensity += 0.1
            self.draw_button()
            self.after(20, self.animate_glow_in)
    
    def animate_glow_out(self):
        """Animate glow effect out"""
        if self.glow_intensity > 0:
            self.glow_intensity -= 0.1
            self.draw_button()
            self.after(20, self.animate_glow_out)
    
    def start_animation(self):
        """Start continuous pulse animation"""
        self.pulse_phase += 0.1
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase = 0
        
        self.draw_button()
        self.after(50, self.start_animation)

class NeuralNetworkVisualization(tk.Canvas):
    """Animated neural network visualization"""
    def __init__(self, parent, width=300, height=200, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.nodes = []
        self.connections = []
        self.animation_phase = 0
        
        self.configure(bg="#0a0a0a")
        
        self.create_network()
        self.start_animation()
    
    def create_network(self):
        """Create neural network structure"""
        # Create nodes in layers
        layers = [4, 6, 4, 2]  # Input, hidden1, hidden2, output
        layer_spacing = self.width // (len(layers) + 1)
        
        for layer_idx, node_count in enumerate(layers):
            x = layer_spacing * (layer_idx + 1)
            node_spacing = self.height // (node_count + 1)
            
            layer_nodes = []
            for node_idx in range(node_count):
                y = node_spacing * (node_idx + 1)
                layer_nodes.append((x, y))
            
            self.nodes.append(layer_nodes)
        
        # Create connections
        for layer_idx in range(len(self.nodes) - 1):
            for node1 in self.nodes[layer_idx]:
                for node2 in self.nodes[layer_idx + 1]:
                    self.connections.append((node1, node2, random.random()))
    
    def draw_network(self):
        """Draw the neural network"""
        self.delete("all")
        
        # Draw connections with pulsing effect
        for (x1, y1), (x2, y2), weight in self.connections:
            pulse = math.sin(self.animation_phase + weight * 10) * 0.5 + 0.5
            alpha = 0.3 + pulse * 0.7
            
            # Color based on weight and pulse
            intensity = int(255 * alpha * weight)
            color = f"#{intensity:02x}{intensity//2:02x}{intensity//3:02x}"
            
            self.create_line(x1, y1, x2, y2, fill=color, width=1, tags="connection")
        
        # Draw nodes
        for layer_nodes in self.nodes:
            for x, y in layer_nodes:
                # Pulsing node effect
                pulse = math.sin(self.animation_phase + x * 0.1) * 0.3 + 0.7
                radius = 5 * pulse
                
                # Outer glow
                self.create_oval(
                    x - radius - 2, y - radius - 2,
                    x + radius + 2, y + radius + 2,
                    fill="#4ecdc4", outline="", tags="node_glow"
                )
                
                # Inner node
                self.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill="#00ffff", outline="#4ecdc4", width=1, tags="node"
                )
    
    def start_animation(self):
        """Start neural network animation"""
        self.animation_phase += 0.1
        if self.animation_phase > 2 * math.pi:
            self.animation_phase = 0
        
        self.draw_network()
        self.after(100, self.start_animation)

class EnhancedModernGUI:
    """Ultra-modern, enhanced GUI with advanced animations and effects"""
    
    def __init__(self):
        # Initialize state
        self.is_processing = False
        self.current_task = None
        self.voice_mode = False
        self.theme_mode = "cyber"  # cyber, matrix, hologram, neon
        
        # Animation variables
        self.pulse_value = 0
        self.typing_dots = 0
        self.progress_value = 0
        self.matrix_drops = []
        self.hologram_lines = []
        
        # Initialize Shadow AI
        self.shadow_ai = None
        if SHADOW_AI_AVAILABLE:
            try:
                self.shadow_ai = ShadowAI()
                logging.info("Shadow AI initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Shadow AI: {e}")
        
        # Create main window
        self.create_main_window()
        self.setup_gui()
        self.start_background_animations()
        
        # Initialize particle system
        self.particle_system = ParticleSystem(self.main_canvas, max_particles=100)
        
    def create_main_window(self):
        """Create and configure the main window"""
        self.root = tk.Tk()
        self.root.title("🚀 Shadow AI - Enhanced Ultra Interface")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)
        
        # Center window
        self.center_window()
        
        # Configure style
        self.setup_styles()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
    
    def setup_styles(self):
        """Setup custom styles"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure custom styles
        self.style.configure("Cyber.TFrame", 
                           background="#0a0a0a", 
                           borderwidth=1,
                           relief="solid")
        
        self.style.configure("Cyber.TLabel",
                           background="#0a0a0a",
                           foreground="#4ecdc4",
                           font=("Arial", 12))
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0a0a0a")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create animated background canvas
        self.create_background_canvas()
        
        # Create header with advanced title
        self.create_header()
        
        # Create main content area
        self.create_content_area()
        
        # Create sidebar with neural network
        self.create_sidebar()
        
        # Create status bar with advanced indicators
        self.create_status_bar()
    
    def create_background_canvas(self):
        """Create animated background canvas"""
        self.bg_canvas = tk.Canvas(
            self.main_frame, 
            width=1380, 
            height=880,
            highlightthickness=0,
            bg="#0a0a0a"
        )
        self.bg_canvas.place(x=0, y=0)
        
        # Initialize matrix rain effect
        self.init_matrix_rain()
    
    def init_matrix_rain(self):
        """Initialize matrix rain effect"""
        for _ in range(20):
            self.matrix_drops.append({
                'x': random.randint(0, 1380),
                'y': random.randint(-100, 0),
                'speed': random.uniform(2, 8),
                'chars': [chr(random.randint(0x30A0, 0x30FF)) for _ in range(10)]
            })
    
    def create_header(self):
        """Create animated header"""
        self.header_frame = tk.Frame(self.main_frame, bg="#0a0a0a", height=120)
        self.header_frame.pack(fill="x", pady=(0, 20))
        self.header_frame.pack_propagate(False)
        
        # Main canvas for header effects
        self.header_canvas = tk.Canvas(
            self.header_frame,
            height=120,
            highlightthickness=0,
            bg="#0a0a0a"
        )
        self.header_canvas.pack(fill="both", expand=True)
        
        # Create holographic title
        self.create_holographic_title()
        
        # Theme selector
        self.create_theme_selector()
    
    def create_holographic_title(self):
        """Create holographic-style title with effects"""
        title_text = "🚀 SHADOW AI - ENHANCED ULTRA INTERFACE"
        
        # Multiple text layers for glow effect
        for offset in range(5, 0, -1):
            self.header_canvas.create_text(
                690, 60 + offset,
                text=title_text,
                font=("Orbitron", 24, "bold"),
                fill=f"#00ffff{60-offset*10:02x}",
                tags="title_glow"
            )
        
        # Main title
        self.header_canvas.create_text(
            690, 60,
            text=title_text,
            font=("Orbitron", 24, "bold"),
            fill="#ffffff",
            tags="title_main"
        )
        
        # Animated subtitle
        self.subtitle_y = 90
        self.create_animated_subtitle()
    
    def create_animated_subtitle(self):
        """Create animated subtitle"""
        subtitles = [
            "🎭 Emotional Intelligence • 🧠 Universal Task Execution • 🎨 Advanced Visualization",
            "💫 Particle Effects • 🌊 Holographic Interface • ⚡ Real-time Processing",
            "🔮 Neural Networks • 🎪 Dynamic Themes • 🚀 Next-Gen AI Assistant"
        ]
        
        subtitle = subtitles[int(time.time() / 3) % len(subtitles)]
        
        self.header_canvas.delete("subtitle")
        self.header_canvas.create_text(
            690, self.subtitle_y,
            text=subtitle,
            font=("Arial", 12),
            fill="#4ecdc4",
            tags="subtitle"
        )
    
    def create_theme_selector(self):
        """Create theme selector buttons"""
        themes = [
            ("🌊 Cyber", "cyber"),
            ("🟢 Matrix", "matrix"),
            ("💎 Hologram", "hologram"),
            ("🌈 Neon", "neon")
        ]
        
        theme_frame = tk.Frame(self.header_frame, bg="#0a0a0a")
        theme_frame.place(x=1200, y=10)
        
        for i, (name, theme) in enumerate(themes):
            btn = HolographicButton(
                theme_frame,
                text=name,
                command=lambda t=theme: self.change_theme(t),
                width=80,
                height=30,
                bg="#0a0a0a"
            )
            btn.grid(row=i//2, column=i%2, padx=2, pady=2)
    
    def create_content_area(self):
        """Create main content area"""
        # Content container
        self.content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.content_frame.pack(fill="both", expand=True, side="left")
        
        # Create main canvas for content
        self.main_canvas = tk.Canvas(
            self.content_frame,
            highlightthickness=0,
            bg="#0f1419"
        )
        self.main_canvas.pack(fill="both", expand=True, padx=(0, 10))
        
        # Input section
        self.create_input_section()
        
        # Output section
        self.create_output_section()
        
        # Control panel
        self.create_control_panel()
    
    def create_input_section(self):
        """Create input section with holographic styling"""
        input_frame = tk.Frame(self.main_canvas, bg="#0f1419")
        input_frame.place(x=20, y=20, width=800, height=150)
        
        # Input label with glow
        input_label = tk.Label(
            input_frame,
            text="🎯 COMMAND INTERFACE",
            font=("Orbitron", 14, "bold"),
            fg="#00ffff",
            bg="#0f1419"
        )
        input_label.pack(pady=(10, 5))
        
        # Command input with holographic border
        input_container = tk.Frame(input_frame, bg="#4ecdc4", bd=2)
        input_container.pack(fill="x", padx=20, pady=5)
        
        inner_container = tk.Frame(input_container, bg="#0a0a0a", bd=1)
        inner_container.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.command_entry = tk.Text(
            inner_container,
            height=3,
            font=("Consolas", 12),
            bg="#0a0a0a",
            fg="#4ecdc4",
            insertbackground="#00ffff",
            relief="flat",
            wrap="word"
        )
        self.command_entry.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind events
        self.command_entry.bind("<Return>", self.handle_enter_key)
        self.command_entry.bind("<Control-Return>", self.process_command)
        
        # Button container
        button_frame = tk.Frame(input_frame, bg="#0f1419")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Holographic buttons
        self.execute_btn = HolographicButton(
            button_frame,
            text="⚡ EXECUTE",
            command=self.process_command,
            width=120,
            height=40,
            bg="#0f1419"
        )
        self.execute_btn.pack(side="left", padx=(0, 10))
        
        self.voice_btn = HolographicButton(
            button_frame,
            text="🎤 VOICE",
            command=self.toggle_voice_mode,
            width=100,
            height=40,
            bg="#0f1419"
        )
        self.voice_btn.pack(side="left", padx=(0, 10))
        
        self.clear_btn = HolographicButton(
            button_frame,
            text="🗑️ CLEAR",
            command=self.clear_output,
            width=100,
            height=40,
            bg="#0f1419"
        )
        self.clear_btn.pack(side="left")
    
    def create_output_section(self):
        """Create output section with advanced visualization"""
        output_frame = tk.Frame(self.main_canvas, bg="#0f1419")
        output_frame.place(x=20, y=190, width=800, height=400)
        
        # Output label
        output_label = tk.Label(
            output_frame,
            text="📊 SYSTEM OUTPUT & TASK VISUALIZATION",
            font=("Orbitron", 14, "bold"),
            fg="#00ffff",
            bg="#0f1419"
        )
        output_label.pack(pady=(10, 5))
        
        # Create tabbed output
        self.output_notebook = ttk.Notebook(output_frame, style="Cyber.TNotebook")
        self.output_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Console tab
        self.create_console_tab()
        
        # Visualization tab
        self.create_visualization_tab()
        
        # Analytics tab
        self.create_analytics_tab()
    
    def create_console_tab(self):
        """Create console output tab"""
        console_frame = tk.Frame(self.output_notebook, bg="#0a0a0a")
        self.output_notebook.add(console_frame, text="💻 Console")
        
        # Console output with holographic styling
        console_container = tk.Frame(console_frame, bg="#4ecdc4", bd=2)
        console_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        inner_console = tk.Frame(console_container, bg="#0a0a0a", bd=1)
        inner_console.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.output_text = scrolledtext.ScrolledText(
            inner_console,
            font=("Consolas", 10),
            bg="#0a0a0a",
            fg="#4ecdc4",
            insertbackground="#00ffff",
            relief="flat",
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add initial message
        self.log_message("🚀 Enhanced Shadow AI Interface Initialized")
        self.log_message("💫 Particle systems active")
        self.log_message("🎭 Holographic interface ready")
        self.log_message("⚡ Enhanced task execution engine online")
        self.log_message("🎯 Ready for advanced command processing...")
    
    def create_visualization_tab(self):
        """Create task visualization tab"""
        viz_frame = tk.Frame(self.output_notebook, bg="#0a0a0a")
        self.output_notebook.add(viz_frame, text="🎨 Visualization")
        
        # Task progress visualization
        self.progress_canvas = tk.Canvas(
            viz_frame,
            bg="#0a0a0a",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.init_visualization()
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        analytics_frame = tk.Frame(self.output_notebook, bg="#0a0a0a")
        self.output_notebook.add(analytics_frame, text="📈 Analytics")
        
        # Analytics content
        analytics_label = tk.Label(
            analytics_frame,
            text="📊 Real-time Performance Analytics",
            font=("Orbitron", 12, "bold"),
            fg="#4ecdc4",
            bg="#0a0a0a"
        )
        analytics_label.pack(pady=20)
        
        # Stats display
        self.stats_frame = tk.Frame(analytics_frame, bg="#0a0a0a")
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_stats_display()
    
    def create_sidebar(self):
        """Create sidebar with neural network visualization"""
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#0f1419", width=300)
        self.sidebar_frame.pack(side="right", fill="y", padx=(10, 0))
        self.sidebar_frame.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(
            self.sidebar_frame,
            text="🧠 NEURAL INTERFACE",
            font=("Orbitron", 12, "bold"),
            fg="#00ffff",
            bg="#0f1419"
        )
        sidebar_title.pack(pady=(20, 10))
        
        # Neural network visualization
        self.neural_viz = NeuralNetworkVisualization(
            self.sidebar_frame,
            width=280,
            height=200,
            bg="#0a0a0a"
        )
        self.neural_viz.pack(pady=10)
        
        # System status
        self.create_system_status()
        
        # Quick actions
        self.create_quick_actions()
    
    def create_system_status(self):
        """Create system status display"""
        status_frame = tk.Frame(self.sidebar_frame, bg="#0f1419")
        status_frame.pack(fill="x", padx=10, pady=20)
        
        status_title = tk.Label(
            status_frame,
            text="⚡ SYSTEM STATUS",
            font=("Orbitron", 10, "bold"),
            fg="#4ecdc4",
            bg="#0f1419"
        )
        status_title.pack()
        
        # Status indicators
        self.status_indicators = {}
        indicators = [
            ("🧠 AI Engine", "online"),
            ("🎭 Emotional AI", "ready"),
            ("🎤 Voice Input", "available" if VOICE_ENABLED else "disabled"),
            ("⚡ Task Executor", "standby"),
            ("🎨 Particle System", "active")
        ]
        
        for name, status in indicators:
            indicator_frame = tk.Frame(status_frame, bg="#0f1419")
            indicator_frame.pack(fill="x", pady=2)
            
            label = tk.Label(
                indicator_frame,
                text=name,
                font=("Arial", 9),
                fg="#4ecdc4",
                bg="#0f1419"
            )
            label.pack(side="left")
            
            status_color = "#00ff00" if status in ["online", "ready", "active", "available"] else "#ffaa00"
            status_label = tk.Label(
                indicator_frame,
                text=f"● {status}",
                font=("Arial", 9),
                fg=status_color,
                bg="#0f1419"
            )
            status_label.pack(side="right")
            
            self.status_indicators[name] = status_label
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = tk.Frame(self.sidebar_frame, bg="#0f1419")
        actions_frame.pack(fill="x", padx=10, pady=20)
        
        actions_title = tk.Label(
            actions_frame,
            text="🚀 QUICK ACTIONS",
            font=("Orbitron", 10, "bold"),
            fg="#4ecdc4",
            bg="#0f1419"
        )
        actions_title.pack(pady=(0, 10))
        
        # Quick action buttons
        quick_actions = [
            ("📝 Test Notepad", lambda: self.quick_command("open a notepad and create a new file and name it new.txt then write an article about ai")),
            ("🌐 Open Browser", lambda: self.quick_command("open google chrome")),
            ("📊 Take Screenshot", lambda: self.quick_command("take a screenshot")),
            ("🎭 Chat Orpheus", lambda: self.quick_command("start emotional conversation with orpheus")),
        ]
        
        for text, command in quick_actions:
            btn = HolographicButton(
                actions_frame,
                text=text,
                command=command,
                width=250,
                height=35,
                bg="#0f1419"
            )
            btn.pack(pady=3)
    
    def create_control_panel(self):
        """Create control panel"""
        control_frame = tk.Frame(self.main_canvas, bg="#0f1419")
        control_frame.place(x=20, y=610, width=800, height=100)
        
        # Control title
        control_title = tk.Label(
            control_frame,
            text="🎛️ ADVANCED CONTROLS",
            font=("Orbitron", 12, "bold"),
            fg="#00ffff",
            bg="#0f1419"
        )
        control_title.pack(pady=(10, 5))
        
        # Control buttons
        control_buttons_frame = tk.Frame(control_frame, bg="#0f1419")
        control_buttons_frame.pack()
        
        controls = [
            ("🔄 Reset System", self.reset_system),
            ("⚙️ Settings", self.open_settings),
            ("📋 Export Logs", self.export_logs),
            ("🎨 Particle Burst", self.create_particle_burst),
            ("🎭 Launch Orpheus", self.launch_orpheus)
        ]
        
        for i, (text, command) in enumerate(controls):
            btn = HolographicButton(
                control_buttons_frame,
                text=text,
                command=command,
                width=150,
                height=30,
                bg="#0f1419"
            )
            btn.grid(row=0, column=i, padx=5)
    
    def create_status_bar(self):
        """Create advanced status bar"""
        self.status_frame = tk.Frame(self.main_frame, bg="#0a0a0a", height=40)
        self.status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        self.status_frame.pack_propagate(False)
        
        # Status canvas for animations
        self.status_canvas = tk.Canvas(
            self.status_frame,
            height=40,
            bg="#0a0a0a",
            highlightthickness=0
        )
        self.status_canvas.pack(fill="both", expand=True)
        
        self.update_status_bar()
    
    def init_visualization(self):
        """Initialize task visualization"""
        self.progress_canvas.delete("all")
        
        # Create initial visualization elements
        self.progress_canvas.create_text(
            400, 180,
            text="🎨 Advanced Task Visualization Ready",
            font=("Orbitron", 16, "bold"),
            fill="#4ecdc4",
            tags="viz_title"
        )
        
        self.progress_canvas.create_text(
            400, 220,
            text="Execute commands to see real-time progress visualization",
            font=("Arial", 12),
            fill="#666666",
            tags="viz_subtitle"
        )
    
    def create_stats_display(self):
        """Create statistics display"""
        stats = [
            ("Commands Executed", "0"),
            ("Success Rate", "100%"),
            ("Average Execution Time", "0.0s"),
            ("Particles Generated", "0"),
            ("Neural Activity", "Optimal")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(self.stats_frame, bg="#0a0a0a")
            stat_frame.pack(fill="x", pady=5)
            
            label_widget = tk.Label(
                stat_frame,
                text=label,
                font=("Arial", 10),
                fg="#4ecdc4",
                bg="#0a0a0a"
            )
            label_widget.pack(side="left")
            
            value_widget = tk.Label(
                stat_frame,
                text=value,
                font=("Arial", 10, "bold"),
                fg="#00ffff",
                bg="#0a0a0a"
            )
            value_widget.pack(side="right")
    
    def start_background_animations(self):
        """Start all background animations"""
        self.animate_background()
        self.animate_particles()
        self.update_neural_activity()
    
    def animate_background(self):
        """Animate background effects"""
        self.bg_canvas.delete("matrix")
        
        # Animate matrix rain
        for drop in self.matrix_drops:
            drop['y'] += drop['speed']
            
            if drop['y'] > 880:
                drop['y'] = random.randint(-100, 0)
                drop['x'] = random.randint(0, 1380)
            
            # Draw characters with fading effect
            for i, char in enumerate(drop['chars']):
                y_pos = drop['y'] - i * 20
                if 0 <= y_pos <= 880:
                    alpha = 255 - (i * 25)
                    if alpha > 0:
                        color = f"#{0:02x}{alpha:02x}{0:02x}"
                        self.bg_canvas.create_text(
                            drop['x'], y_pos,
                            text=char,
                            font=("Consolas", 12),
                            fill=color,
                            tags="matrix"
                        )
        
        self.root.after(100, self.animate_background)
    
    def animate_particles(self):
        """Animate particle system"""
        self.main_canvas.delete("particle")
        self.particle_system.update()
        self.particle_system.draw()
        self.root.after(50, self.animate_particles)
    
    def update_neural_activity(self):
        """Update neural network activity indicators"""
        self.root.after(100, self.update_neural_activity)
    
    def update_status_bar(self):
        """Update status bar with animations"""
        self.status_canvas.delete("all")
        
        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_canvas.create_text(
            100, 20,
            text=f"🕒 {current_time}",
            font=("Arial", 10),
            fill="#4ecdc4",
            anchor="w"
        )
        
        # Status message
        status_text = "🚀 Enhanced Interface Active"
        if self.is_processing:
            status_text = "⚡ Processing Command..."
        
        self.status_canvas.create_text(
            400, 20,
            text=status_text,
            font=("Arial", 10),
            fill="#00ffff"
        )
        
        # System resources (animated)
        cpu_usage = 15 + math.sin(time.time()) * 5
        self.status_canvas.create_text(
            1200, 20,
            text=f"💻 CPU: {cpu_usage:.1f}%",
            font=("Arial", 10),
            fill="#4ecdc4",
            anchor="e"
        )
        
        self.root.after(1000, self.update_status_bar)
    
    # Event handlers and functionality
    def handle_enter_key(self, event):
        """Handle Enter key in command entry"""
        if event.state & 0x4:  # Ctrl+Enter
            self.process_command()
            return "break"
        else:
            # Insert newline
            return None
    
    def process_command(self):
        """Process the entered command"""
        command = self.command_entry.get("1.0", "end-1c").strip()
        if not command:
            return
        
        self.log_message(f"🎯 Command: {command}")
        self.create_particle_burst()
        
        # Start processing animation
        self.is_processing = True
        self.update_processing_visualization()
        
        # Process command in thread
        threading.Thread(target=self._process_command_thread, args=(command,), daemon=True).start()
    
    def _process_command_thread(self, command):
        """Process command in background thread"""
        try:
            if self.shadow_ai:
                result = self.shadow_ai.process_command(command)
                self.root.after(0, self._handle_command_result, result)
            else:
                # Fallback simulation
                time.sleep(2)
                result = {"success": True, "message": "Command simulated (Shadow AI not available)"}
                self.root.after(0, self._handle_command_result, result)
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self.root.after(0, self._handle_command_result, error_result)
    
    def _handle_command_result(self, result):
        """Handle command execution result"""
        self.is_processing = False
        
        if result.get("success"):
            self.log_message(f"✅ Success: {result.get('message', 'Command completed')}")
            self.create_success_particle_burst()
        else:
            self.log_message(f"❌ Error: {result.get('error', 'Unknown error')}")
            self.create_error_particle_burst()
        
        # Clear command entry
        self.command_entry.delete("1.0", "end")
    
    def update_processing_visualization(self):
        """Update processing visualization"""
        if self.is_processing:
            # Update progress visualization
            self.progress_value = (self.progress_value + 5) % 100
            
            # Add processing particles
            center_x, center_y = 400, 200
            for _ in range(3):
                angle = random.uniform(0, 2 * math.pi)
                vx = math.cos(angle) * 2
                vy = math.sin(angle) * 2
                self.particle_system.add_particle(
                    center_x, center_y,
                    vx=vx, vy=vy,
                    life=60,
                    color="#ffaa00"
                )
            
            self.root.after(100, self.update_processing_visualization)
    
    def toggle_voice_mode(self):
        """Toggle voice input mode"""
        if lazy_import_voice():
            self.voice_mode = not self.voice_mode
            if self.voice_mode:
                self.start_voice_input()
            else:
                self.log_message("🎤 Voice mode disabled")
        else:
            self.log_message("❌ Voice input not available")
    
    def start_voice_input(self):
        """Start voice input"""
        self.log_message("🎤 Voice input activated - speak your command...")
        threading.Thread(target=self._voice_input_thread, daemon=True).start()
    
    def _voice_input_thread(self):
        """Voice input thread"""
        try:
            command = _voice_module.get_voice_input("Speak your command:")
            if command:
                self.root.after(0, self._handle_voice_command, command)
            else:
                self.root.after(0, lambda: self.log_message("🎤 No voice input detected"))
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"❌ Voice input error: {e}"))
        finally:
            self.voice_mode = False
    
    def _handle_voice_command(self, command):
        """Handle voice command"""
        self.log_message(f"🎤 Voice command: {command}")
        self.command_entry.delete("1.0", "end")
        self.command_entry.insert("1.0", command)
        self.process_command()
    
    def quick_command(self, command):
        """Execute a quick command"""
        self.command_entry.delete("1.0", "end")
        self.command_entry.insert("1.0", command)
        self.process_command()
    
    def change_theme(self, theme):
        """Change the visual theme"""
        self.theme_mode = theme
        self.log_message(f"🎨 Theme changed to: {theme}")
        # Theme changing logic would go here
    
    def create_particle_burst(self):
        """Create particle burst effect"""
        center_x, center_y = 400, 300
        self.particle_system.add_burst(
            center_x, center_y,
            count=15,
            color="#4ecdc4",
            life=80
        )
    
    def create_success_particle_burst(self):
        """Create success particle burst"""
        center_x, center_y = 400, 300
        self.particle_system.add_burst(
            center_x, center_y,
            count=20,
            color="#00ff00",
            life=100
        )
    
    def create_error_particle_burst(self):
        """Create error particle burst"""
        center_x, center_y = 400, 300
        self.particle_system.add_burst(
            center_x, center_y,
            count=10,
            color="#ff0000",
            life=60
        )
    
    def reset_system(self):
        """Reset the system"""
        self.log_message("🔄 System reset initiated...")
        self.clear_output()
        self.particle_system.particles.clear()
        self.log_message("✅ System reset complete")
    
    def open_settings(self):
        """Open settings dialog"""
        self.log_message("⚙️ Settings panel (feature coming soon)")
    
    def export_logs(self):
        """Export system logs"""
        self.log_message("📋 Exporting logs (feature coming soon)")
    
    def launch_orpheus(self):
        """Launch Orpheus emotional AI"""
        try:
            import subprocess
            subprocess.Popen(["python", "gui_orpheus.py"])
            self.log_message("🎭 Orpheus emotional AI launched")
        except Exception as e:
            self.log_message(f"❌ Failed to launch Orpheus: {e}")
    
    def clear_output(self):
        """Clear output display"""
        self.output_text.delete("1.0", "end")
        self.log_message("🚀 Enhanced Shadow AI Interface Ready")
    
    def log_message(self, message):
        """Log a message to the output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.output_text.insert("end", formatted_message)
        self.output_text.see("end")
    
    def run(self):
        """Start the GUI"""
        self.log_message("🎉 Welcome to Enhanced Shadow AI!")
        self.log_message("💫 All systems online and ready for advanced operations")
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = EnhancedModernGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Enhanced Modern GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
