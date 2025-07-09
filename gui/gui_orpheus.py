#!/usr/bin/env python3
"""
Shadow AI - Orpheus Emotional GUI
Beautiful GUI with integrated emotional AI conversations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import logging
import math
from datetime import datetime
import sys
import os
from typing import Optional, Dict, Any

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import ShadowAI
    from config import VOICE_ENABLED
    from brain.orpheus_ai import EmotionalAI, EmotionType, chat_with_orpheus, get_orpheus_emotional_state, reset_orpheus_conversation, get_orpheus_greeting
except ImportError as e:
    logging.error(f"Import error: {e}")
    ShadowAI = None
    VOICE_ENABLED = False
    EmotionalAI = None

class EmotionalIndicator(tk.Canvas):
    """Visual indicator for emotional states with animated colors"""
    
    def __init__(self, parent, size=60, **kwargs):
        super().__init__(parent, width=size, height=size, highlightthickness=0, **kwargs)
        
        self.size = size
        self.center = size // 2
        self.current_emotion = "calm"
        self.intensity = 0.5
        self.animation_step = 0
        self.is_animating = False
        
        # Emotion color mapping
        self.emotion_colors = {
            "happy": "#FFD700",      # Gold
            "sad": "#4169E1",        # Royal Blue
            "excited": "#FF6347",    # Tomato
            "calm": "#98FB98",       # Pale Green
            "curious": "#DDA0DD",    # Plum
            "empathetic": "#F0E68C", # Khaki
            "confident": "#FF4500",  # Orange Red
            "playful": "#FF69B4",    # Hot Pink
            "thoughtful": "#9370DB", # Medium Purple
            "encouraging": "#32CD32", # Lime Green
            "surprised": "#FFFF00",  # Yellow
            "concerned": "#CD853F"   # Peru
        }
        
        self.draw_emotion()
    
    def set_emotion(self, emotion: str, intensity: float = 0.5):
        """Set the current emotion and intensity"""
        self.current_emotion = emotion.lower()
        self.intensity = max(0.0, min(1.0, intensity))
        self.start_animation()
    
    def draw_emotion(self):
        """Draw the emotional indicator"""
        self.delete("all")
        
        color = self.emotion_colors.get(self.current_emotion, "#98FB98")
        
        # Calculate pulsing effect based on intensity
        pulse = 1.0
        if self.is_animating:
            pulse = 0.8 + 0.4 * (0.5 + 0.5 * math.sin(self.animation_step * 0.3))
        
        # Main circle
        radius = int(self.center - 10)
        scaled_radius = int(radius * pulse * (0.5 + 0.5 * self.intensity))
        
        self.create_oval(
            self.center - scaled_radius,
            self.center - scaled_radius,
            self.center + scaled_radius,
            self.center + scaled_radius,
            fill=color,
            outline="white",
            width=2,
            tags="emotion"
        )
        
        # Inner glow effect
        inner_radius = int(scaled_radius * 0.6)
        self.create_oval(
            self.center - inner_radius,
            self.center - inner_radius,
            self.center + inner_radius,
            self.center + inner_radius,
            fill="white",
            outline="",
            stipple="gray25",
            tags="glow"
        )
        
        # Emotion text
        self.create_text(
            self.center,
            self.center + scaled_radius + 15,
            text=self.current_emotion.title(),
            font=("Segoe UI", 10, "bold"),
            fill=color,
            tags="text"
        )
    
    def start_animation(self):
        """Start the pulsing animation"""
        self.is_animating = True
        self.animate()
    
    def stop_animation(self):
        """Stop the animation"""
        self.is_animating = False
    
    def animate(self):
        """Animation loop"""
        if not self.is_animating:
            return
        
        self.animation_step += 1
        self.draw_emotion()
        
        # Stop animation after a few seconds
        if self.animation_step > 60:
            self.is_animating = False
            self.animation_step = 0
        
        if self.is_animating:
            self.after(100, self.animate)

class OrpheusGUI:
    """Orpheus Emotional AI GUI"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.shadow_ai = None
        self.orpheus_ai = None
        self.voice_available = False
        
        # Mode selection
        self.current_mode = "orpheus"  # "orpheus" or "shadow"
        
        self.setup_window()
        self.create_widgets()
        self.setup_ai_systems()
        self.start_with_greeting()
    
    def setup_window(self):
        """Configure the main window"""
        self.window.title("Shadow AI - Orpheus Emotional Interface")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 600)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#F8F9FA',
            'bg_secondary': '#FFFFFF',
            'bg_accent': '#E3F2FD',
            'orpheus_primary': '#6A1B9A',
            'orpheus_secondary': '#8E24AA',
            'shadow_primary': '#1976D2',
            'shadow_secondary': '#2196F3',
            'text_primary': '#212121',
            'text_secondary': '#757575',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336'
        }
        
        self.window.configure(bg=self.colors['bg_primary'])
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Header
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create the header section"""
        header = tk.Frame(self.window, bg=self.colors['orpheus_primary'], height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Title section
        title_frame = tk.Frame(header, bg=self.colors['orpheus_primary'])
        title_frame.pack(side='left', fill='y', padx=20, pady=20)
        
        # Main title
        title_label = tk.Label(
            title_frame,
            text="🎭 Orpheus",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['orpheus_primary'],
            fg='white'
        )
        title_label.pack(anchor='w')
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Emotional AI Companion",
            font=('Segoe UI', 12),
            bg=self.colors['orpheus_primary'],
            fg='#E1BEE7'
        )
        subtitle_label.pack(anchor='w')
        
        # Emotional indicator section
        emotion_frame = tk.Frame(header, bg=self.colors['orpheus_primary'])
        emotion_frame.pack(side='right', fill='y', padx=20, pady=20)
        
        # Emotional state display
        self.emotion_indicator = EmotionalIndicator(
            emotion_frame,
            size=60,
            bg=self.colors['orpheus_primary']
        )
        self.emotion_indicator.pack()
        
        # Mode toggle
        mode_frame = tk.Frame(header, bg=self.colors['orpheus_primary'])
        mode_frame.pack(side='right', fill='y', padx=20, pady=30)
        
        self.mode_button = tk.Button(
            mode_frame,
            text="Switch to Shadow AI",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=self.colors['orpheus_primary'],
            command=self.toggle_mode,
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        self.mode_button.pack()
    
    def create_main_content(self):
        """Create the main content area"""
        main_frame = tk.Frame(self.window, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Chat display area
        chat_frame = tk.LabelFrame(
            main_frame,
            text="💬 Conversation",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            pady=10
        )
        chat_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            state='disabled',
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure text tags for different message types
        self.setup_chat_tags()
        
        # Input area
        self.create_input_area(main_frame)
        
        # Side panel
        self.create_side_panel(main_frame)
    
    def setup_chat_tags(self):
        """Setup text tags for chat formatting"""
        self.chat_display.tag_configure('user', foreground=self.colors['shadow_primary'], font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('orpheus', foreground=self.colors['orpheus_primary'], font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('shadow', foreground=self.colors['shadow_primary'], font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_configure('emotion', foreground=self.colors['orpheus_secondary'], font=('Segoe UI', 9, 'italic'))
        self.chat_display.tag_configure('timestamp', foreground=self.colors['text_secondary'], font=('Segoe UI', 9))
    
    def create_input_area(self, parent):
        """Create the input area"""
        input_frame = tk.LabelFrame(
            parent,
            text="💭 Your Message",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            pady=10
        )
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Text input
        self.text_input = tk.Text(
            input_frame,
            height=4,
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text_primary'],
            relief='solid',
            borderwidth=1,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.text_input.pack(fill='x', padx=10, pady=(0, 10))
        self.text_input.bind('<Return>', self.on_enter_pressed)
        
        # Button frame
        button_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Send button
        self.send_btn = tk.Button(
            button_frame,
            text="💬 Send Message",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['orpheus_primary'],
            fg='white',
            command=self.send_message,
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        self.send_btn.pack(side='right', padx=(5, 0))
        
        # Voice button
        self.voice_btn = tk.Button(
            button_frame,
            text="🎤 Voice",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['success'],
            fg='white',
            command=self.send_voice_message,
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        self.voice_btn.pack(side='right', padx=(5, 0))
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=('Segoe UI', 11),
            bg=self.colors['text_secondary'],
            fg='white',
            command=self.clear_chat,
            padx=15,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left')
    
    def create_side_panel(self, parent):
        """Create the side panel with emotional status"""
        side_frame = tk.Frame(parent, bg=self.colors['bg_primary'], width=250)
        side_frame.pack(side='right', fill='y', padx=(20, 0))
        side_frame.pack_propagate(False)
        
        # Emotional status card
        status_frame = tk.LabelFrame(
            side_frame,
            text="🎭 Emotional State",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            pady=10
        )
        status_frame.pack(fill='x', pady=(0, 20))
        
        # Current emotion display
        self.emotion_text = tk.Label(
            status_frame,
            text="Calm & Ready",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['orpheus_primary'],
            wraplength=200
        )
        self.emotion_text.pack(pady=10)
        
        # Mood description
        self.mood_text = tk.Label(
            status_frame,
            text="Ready for meaningful conversation",
            font=('Segoe UI', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            wraplength=200,
            justify='center'
        )
        self.mood_text.pack(pady=(0, 10))
        
        # Conversation stats
        stats_frame = tk.LabelFrame(
            side_frame,
            text="📊 Conversation Stats",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            pady=10
        )
        stats_frame.pack(fill='x', pady=(0, 20))
        
        self.stats_text = tk.Label(
            stats_frame,
            text="Messages: 0\nStarted: Not yet",
            font=('Segoe UI', 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            justify='left'
        )
        self.stats_text.pack(pady=10, padx=10)
        
        # Quick actions
        actions_frame = tk.LabelFrame(
            side_frame,
            text="⚡ Quick Actions",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            pady=10
        )
        actions_frame.pack(fill='x')
        
        # Reset conversation button
        reset_btn = tk.Button(
            actions_frame,
            text="🔄 New Conversation",
            font=('Segoe UI', 10),
            bg=self.colors['warning'],
            fg='white',
            command=self.reset_conversation,
            padx=10,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        reset_btn.pack(fill='x', padx=10, pady=5)
        
        # Export conversation button
        export_btn = tk.Button(
            actions_frame,
            text="💾 Export Chat",
            font=('Segoe UI', 10),
            bg=self.colors['shadow_primary'],
            fg='white',
            command=self.export_conversation,
            padx=10,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        export_btn.pack(fill='x', padx=10, pady=(0, 10))
    
    def create_footer(self):
        """Create the footer"""
        footer = tk.Frame(self.window, bg=self.colors['orpheus_secondary'], height=40)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(
            footer,
            text="Ready to chat",
            font=('Segoe UI', 10),
            bg=self.colors['orpheus_secondary'],
            fg='white'
        )
        self.status_label.pack(side='left', padx=20, pady=10)
        
        # Time label
        self.time_label = tk.Label(
            footer,
            text="",
            font=('Segoe UI', 10),
            bg=self.colors['orpheus_secondary'],
            fg='white'
        )
        self.time_label.pack(side='right', padx=20, pady=10)
        
        self.update_time()
    
    def setup_ai_systems(self):
        """Initialize AI systems"""
        # Setup Orpheus
        try:
            if EmotionalAI:
                self.orpheus_ai = EmotionalAI()
                self.update_status("✅ Orpheus emotional AI ready")
                logging.info("Orpheus AI initialized successfully")
            else:
                self.update_status("❌ Orpheus AI not available")
                logging.error("Orpheus AI not available")
        except Exception as e:
            self.update_status(f"❌ Orpheus error: {e}")
            logging.error(f"Error initializing Orpheus: {e}")
        
        # Setup Shadow AI
        try:
            if ShadowAI:
                self.shadow_ai = ShadowAI()
                logging.info("Shadow AI initialized successfully")
            else:
                logging.error("Shadow AI not available")
        except Exception as e:
            logging.error(f"Error initializing Shadow AI: {e}")
        
        # Setup voice
        if VOICE_ENABLED:
            self.voice_available = True
        else:
            self.voice_available = False
            self.voice_btn.configure(state='disabled')
    
    def start_with_greeting(self):
        """Start conversation with a greeting"""
        if self.orpheus_ai:
            greeting = get_orpheus_greeting()
            self.add_chat_message("Orpheus", greeting, "orpheus")
            self.update_emotional_display()
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        if event.state & 0x4:  # Control is held
            return  # Allow newline
        self.send_message()
        return 'break'
    
    def send_message(self):
        """Send a text message"""
        message = self.text_input.get('1.0', 'end-1c').strip()
        if not message:
            return
        
        self.text_input.delete('1.0', 'end')
        self.add_chat_message("You", message, "user")
        
        if self.current_mode == "orpheus" and self.orpheus_ai:
            self.process_orpheus_message(message)
        elif self.current_mode == "shadow" and self.shadow_ai:
            self.process_shadow_message(message)
        else:
            self.add_chat_message("System", "AI not available", "error")
    
    def send_voice_message(self):
        """Send a voice message"""
        if not self.voice_available:
            messagebox.showerror("Error", "Voice recognition not available")
            return
        
        self.voice_btn.configure(text="🎤 Listening...")
        self.update_status("Listening for voice input...")
        
        def voice_thread():
            try:
                from input.voice_input import get_voice_input
                message = get_voice_input()
                if message:
                    self.window.after(0, lambda: self.add_chat_message("You (voice)", message, "user"))
                    if self.current_mode == "orpheus" and self.orpheus_ai:
                        self.window.after(0, lambda: self.process_orpheus_message(message))
                    elif self.current_mode == "shadow" and self.shadow_ai:
                        self.window.after(0, lambda: self.process_shadow_message(message))
                else:
                    self.window.after(0, lambda: self.update_status("No voice detected"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Voice Error", str(e)))
            finally:
                self.window.after(0, lambda: self.voice_btn.configure(text="🎤 Voice"))
                self.window.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=voice_thread, daemon=True).start()
    
    def process_orpheus_message(self, message: str):
        """Process message with Orpheus emotional AI"""
        self.update_status("Orpheus is thinking...")
        
        def process_thread():
            try:
                response = chat_with_orpheus(message)
                self.window.after(0, lambda: self.add_chat_message("Orpheus", response, "orpheus"))
                self.window.after(0, lambda: self.update_emotional_display())
                self.window.after(0, lambda: self.update_conversation_stats())
            except Exception as e:
                self.window.after(0, lambda: self.add_chat_message("Error", f"Orpheus error: {e}", "error"))
            finally:
                self.window.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def process_shadow_message(self, message: str):
        """Process message with Shadow AI"""
        self.update_status("Shadow AI processing...")
        
        def process_thread():
            try:
                response = self.shadow_ai.process_command(message)
                self.window.after(0, lambda: self.add_chat_message("Shadow AI", response, "shadow"))
            except Exception as e:
                self.window.after(0, lambda: self.add_chat_message("Error", f"Shadow AI error: {e}", "error"))
            finally:
                self.window.after(0, lambda: self.update_status("Ready"))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def add_chat_message(self, sender: str, message: str, msg_type: str):
        """Add a message to the chat display"""
        self.chat_display.configure(state='normal')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add timestamp
        self.chat_display.insert('end', f"[{timestamp}] ", 'timestamp')
        
        # Add sender and message
        self.chat_display.insert('end', f"{sender}: ", msg_type)
        self.chat_display.insert('end', f"{message}\n\n")
        
        # Add emotional context for Orpheus
        if msg_type == "orpheus" and self.orpheus_ai:
            emotion_state = get_orpheus_emotional_state()
            self.chat_display.insert('end', f"💭 {emotion_state}\n\n", 'emotion')
        
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')
    
    def update_emotional_display(self):
        """Update the emotional state display"""
        if self.orpheus_ai:
            emotion_state = get_orpheus_emotional_state()
            
            # Parse emotion state
            parts = emotion_state.split(' - ')
            if len(parts) >= 2:
                emotion_part = parts[0]
                mood = parts[1]
                
                # Extract emotion and intensity
                if '(' in emotion_part:
                    emotion = emotion_part.split('(')[0].strip()
                    intensity_str = emotion_part.split('intensity: ')[1].split(')')[0] if 'intensity:' in emotion_part else "0.5"
                    intensity = float(intensity_str)
                else:
                    emotion = emotion_part
                    intensity = 0.5
                
                # Update displays
                self.emotion_text.configure(text=emotion)
                self.mood_text.configure(text=mood)
                self.emotion_indicator.set_emotion(emotion.lower(), intensity)
    
    def update_conversation_stats(self):
        """Update conversation statistics"""
        if self.orpheus_ai:
            try:
                from brain.orpheus_ai import get_conversation_summary
                stats = get_conversation_summary()
                
                stats_text = f"Messages: {stats.get('total_messages', 0)}\n"
                if stats.get('conversation_started'):
                    start_time = datetime.fromisoformat(stats['conversation_started']).strftime("%H:%M")
                    stats_text += f"Started: {start_time}"
                else:
                    stats_text += "Started: Not yet"
                
                self.stats_text.configure(text=stats_text)
            except Exception as e:
                logging.error(f"Error updating stats: {e}")
    
    def toggle_mode(self):
        """Toggle between Orpheus and Shadow AI"""
        if self.current_mode == "orpheus":
            self.current_mode = "shadow"
            self.mode_button.configure(text="Switch to Orpheus")
            self.window.title("Shadow AI - Command Interface")
            # Update colors to blue theme
            self.update_theme("shadow")
        else:
            self.current_mode = "orpheus"
            self.mode_button.configure(text="Switch to Shadow AI")
            self.window.title("Shadow AI - Orpheus Emotional Interface")
            # Update colors to purple theme
            self.update_theme("orpheus")
    
    def update_theme(self, theme: str):
        """Update the GUI theme"""
        if theme == "orpheus":
            primary = self.colors['orpheus_primary']
            secondary = self.colors['orpheus_secondary']
        else:
            primary = self.colors['shadow_primary']
            secondary = self.colors['shadow_secondary']
        
        # Update header
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') in [self.colors['orpheus_primary'], self.colors['shadow_primary']]:
                widget.configure(bg=primary)
                self.update_widget_colors(widget, primary, secondary)
        
        # Update footer
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') in [self.colors['orpheus_secondary'], self.colors['shadow_secondary']]:
                widget.configure(bg=secondary)
                self.update_widget_colors(widget, primary, secondary)
    
    def update_widget_colors(self, parent, primary, secondary):
        """Recursively update widget colors"""
        for child in parent.winfo_children():
            try:
                if hasattr(child, 'configure'):
                    if isinstance(child, tk.Label) and child.cget('bg') == parent.cget('bg'):
                        child.configure(bg=primary)
                    elif isinstance(child, tk.Button) and child.cget('bg') == self.colors['orpheus_primary']:
                        child.configure(bg=primary)
                
                if hasattr(child, 'winfo_children'):
                    self.update_widget_colors(child, primary, secondary)
            except:
                pass
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', 'end')
        self.chat_display.configure(state='disabled')
        
        if self.current_mode == "orpheus":
            reset_orpheus_conversation()
            self.start_with_greeting()
    
    def reset_conversation(self):
        """Reset the conversation"""
        if messagebox.askyesno("Reset Conversation", "Start a new conversation? This will clear the current chat."):
            self.clear_chat()
            self.update_status("Conversation reset")
    
    def export_conversation(self):
        """Export the conversation to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orpheus_conversation_{timestamp}.txt"
            
            chat_content = self.chat_display.get('1.0', 'end')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Orpheus Conversation Export\n")
                f.write(f"Exported: {datetime.now().isoformat()}\n")
                f.write(f"Mode: {self.current_mode}\n")
                f.write("=" * 50 + "\n\n")
                f.write(chat_content)
            
            messagebox.showinfo("Export Successful", f"Conversation exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export conversation: {e}")
    
    def update_status(self, message: str):
        """Update the status bar"""
        self.status_label.configure(text=message)
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.window.after(1000, self.update_time)
    
    def run(self):
        """Start the GUI"""
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            self.window.quit()

def main():
    """Main function"""
    try:
        app = OrpheusGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Orpheus GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
