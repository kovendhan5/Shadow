#!/usr/bin/env python3
"""
Shadow AI - Cyberpunk GUI
Futuristic neon-themed interface with cyberpunk aesthetics
"""

import sys
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import queue
from datetime import datetime
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.gpt_agent import GPTAgent, process_command
from input.voice_input import get_voice_input, speak_response
from config import VOICE_ENABLED

class ShadowCyberpunkGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shadow AI - Cyberpunk Interface")
        self.root.geometry("1100x800")
        self.root.configure(bg="#0a0a0a")
        
        # Initialize AI agent
        self.ai_agent = GPTAgent()
        self.voice_enabled = VOICE_ENABLED
        
        # Queue for thread communication
        self.response_queue = queue.Queue()
        
        # Cyberpunk colors
        self.neon_green = "#00ff41"
        self.neon_pink = "#ff0080"
        self.neon_blue = "#0080ff"
        self.neon_cyan = "#00ffff"
        self.dark_bg = "#0a0a0a"
        self.panel_bg = "#1a1a1a"
        self.text_bg = "#000000"
        
        # Animation variables
        self.blink_state = True
        self.current_neon_color = self.neon_green
        
        self.setup_ui()
        self.start_animations()
        
    def setup_ui(self):
        """Setup the cyberpunk user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.dark_bg)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with neon effects
        header_frame = tk.Frame(main_frame, bg=self.panel_bg, relief="solid", bd=2, highlightbackground=self.neon_green, highlightthickness=1)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # ASCII art title
        title_frame = tk.Frame(header_frame, bg=self.panel_bg)
        title_frame.pack(fill="x", padx=15, pady=15)
        
        ascii_title = tk.Label(
            title_frame,
            text="╔═══════════════════════════════════════════════════════════════╗\n"
                 "║  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗ █████╗ ██╗ ║\n"
                 "║  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔══██╗██║ ║\n"
                 "║  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████║██║ ║\n"
                 "║  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██╔══██║██║ ║\n"
                 "║  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝██║  ██║██║ ║\n"
                 "║  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝ ║\n"
                 "╚═══════════════════════════════════════════════════════════════╝",
            font=("Courier", 8),
            bg=self.panel_bg,
            fg=self.neon_green,
            justify="center"
        )
        ascii_title.pack()
        
        # Cyberpunk subtitle
        self.subtitle_label = tk.Label(
            title_frame,
            text=">>> NEURAL INTERFACE INITIALIZED <<<",
            font=("Courier", 12, "bold"),
            bg=self.panel_bg,
            fg=self.neon_cyan
        )
        self.subtitle_label.pack(pady=(5, 0))
        
        # System status with blinking effect
        status_frame = tk.Frame(header_frame, bg=self.panel_bg)
        status_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.status_label = tk.Label(
            status_frame,
            text="[ONLINE] SHADOW AI NEURAL NETWORK ACTIVE",
            font=("Courier", 10, "bold"),
            bg=self.panel_bg,
            fg=self.neon_green
        )
        self.status_label.pack(side="left")
        
        # System time
        self.time_label = tk.Label(
            status_frame,
            text=f"TIMESTAMP: {datetime.now().strftime('%H:%M:%S')}",
            font=("Courier", 10),
            bg=self.panel_bg,
            fg=self.neon_blue
        )
        self.time_label.pack(side="right")
        
        # Input terminal
        input_frame = tk.Frame(main_frame, bg=self.panel_bg, relief="solid", bd=2, highlightbackground=self.neon_pink, highlightthickness=1)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_inner = tk.Frame(input_frame, bg=self.panel_bg)
        input_inner.pack(fill="x", padx=15, pady=15)
        
        # Terminal prompt
        prompt_frame = tk.Frame(input_inner, bg=self.panel_bg)
        prompt_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(
            prompt_frame,
            text="root@shadow:~#",
            font=("Courier", 12, "bold"),
            bg=self.panel_bg,
            fg=self.neon_green
        ).pack(side="left")
        
        tk.Label(
            prompt_frame,
            text="NEURAL_COMMAND_INTERFACE",
            font=("Courier", 12, "bold"),
            bg=self.panel_bg,
            fg=self.neon_cyan
        ).pack(side="left", padx=(10, 0))
        
        # Command input
        self.command_entry = tk.Entry(
            input_inner,
            font=("Courier", 12),
            bg=self.text_bg,
            fg=self.neon_green,
            insertbackground=self.neon_green,
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor=self.neon_green,
            selectbackground=self.neon_green,
            selectforeground=self.text_bg
        )
        self.command_entry.pack(fill="x", ipady=5, pady=(0, 10))
        self.command_entry.bind("<Return>", self.process_command)
        
        # Cyberpunk buttons
        button_frame = tk.Frame(input_inner, bg=self.panel_bg)
        button_frame.pack(fill="x")
        
        self.process_btn = tk.Button(
            button_frame,
            text="[ EXECUTE ]",
            command=self.process_command,
            bg=self.text_bg,
            fg=self.neon_green,
            font=("Courier", 10, "bold"),
            relief="solid",
            bd=1,
            activebackground=self.neon_green,
            activeforeground=self.text_bg,
            cursor="hand2"
        )
        self.process_btn.pack(side="left", padx=(0, 10), ipady=3, ipadx=10)
        
        if self.voice_enabled:
            self.voice_btn = tk.Button(
                button_frame,
                text="[ NEURAL_MIC ]",
                command=self.voice_input,
                bg=self.text_bg,
                fg=self.neon_pink,
                font=("Courier", 10, "bold"),
                relief="solid",
                bd=1,
                activebackground=self.neon_pink,
                activeforeground=self.text_bg,
                cursor="hand2"
            )
            self.voice_btn.pack(side="left", padx=(0, 10), ipady=3, ipadx=10)
        
        clear_btn = tk.Button(
            button_frame,
            text="[ PURGE ]",
            command=self.clear_output,
            bg=self.text_bg,
            fg=self.neon_blue,
            font=("Courier", 10, "bold"),
            relief="solid",
            bd=1,
            activebackground=self.neon_blue,
            activeforeground=self.text_bg,
            cursor="hand2"
        )
        clear_btn.pack(side="left", ipady=3, ipadx=10)
        
        # Matrix-style output terminal
        output_frame = tk.Frame(main_frame, bg=self.panel_bg, relief="solid", bd=2, highlightbackground=self.neon_cyan, highlightthickness=1)
        output_frame.pack(fill="both", expand=True)
        
        output_inner = tk.Frame(output_frame, bg=self.panel_bg)
        output_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Terminal header
        terminal_header = tk.Label(
            output_inner,
            text=">>> NEURAL RESPONSE MATRIX <<<",
            font=("Courier", 12, "bold"),
            bg=self.panel_bg,
            fg=self.neon_cyan
        )
        terminal_header.pack(pady=(0, 10))
        
        # Response terminal
        self.response_text = scrolledtext.ScrolledText(
            output_inner,
            font=("Courier", 10),
            bg=self.text_bg,
            fg=self.neon_green,
            insertbackground=self.neon_green,
            relief="flat",
            borderwidth=0,
            wrap=tk.WORD,
            selectbackground=self.neon_green,
            selectforeground=self.text_bg
        )
        self.response_text.pack(fill="both", expand=True)
        
        # Configure text tags for different message types
        self.response_text.tag_configure("user", foreground=self.neon_pink, font=("Courier", 10, "bold"))
        self.response_text.tag_configure("ai", foreground=self.neon_green, font=("Courier", 10))
        self.response_text.tag_configure("system", foreground=self.neon_blue, font=("Courier", 10, "bold"))
        self.response_text.tag_configure("error", foreground="#ff4444", font=("Courier", 10, "bold"))
        self.response_text.tag_configure("timestamp", foreground="#666666", font=("Courier", 8))
        
        # Welcome message
        self.add_response(
            "SHADOW AI CYBERPUNK INTERFACE v2.1\n"
            "NEURAL NETWORK SYNCHRONIZATION: COMPLETE\n"
            "QUANTUM PROCESSING CORES: ONLINE\n"
            "CYBER-SECURITY PROTOCOLS: ACTIVE\n\n"
            ">>> WELCOME TO THE FUTURE <<<\n\n"
            "I am your cybernetic AI companion, enhanced with quantum-neural processing.\n"
            "Direct neural interface established. Ready to process any digital operation.\n\n"
            "AVAILABLE PROTOCOLS:\n"
            "• NEURAL_WRITE: 'Create document about quantum computing'\n"
            "• CYBER_SEARCH: 'Hack into research databases for AI trends'\n"
            "• MATRIX_CONTROL: 'Execute system automation sequence'\n"
            "• DATA_MINE: 'Extract information from web networks'\n\n"
            "WARNING: ALL OPERATIONS ARE LOGGED IN THE NEURAL MATRIX\n"
            "Enter command to initialize neural processing...",
            "system"
        )
        
    def start_animations(self):
        """Start cyberpunk animations"""
        self.animate_subtitle()
        self.update_time()
        self.cycle_neon_colors()
        
    def animate_subtitle(self):
        """Animate subtitle with blinking effect"""
        if self.blink_state:
            self.subtitle_label.config(text=">>> NEURAL INTERFACE INITIALIZED <<<")
        else:
            self.subtitle_label.config(text=">>> NEURAL INTERFACE ACTIVE <<<")
        
        self.blink_state = not self.blink_state
        self.root.after(2000, self.animate_subtitle)
        
    def update_time(self):
        """Update cyberpunk timestamp"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=f"TIMESTAMP: {current_time}")
        self.root.after(1000, self.update_time)
        
    def cycle_neon_colors(self):
        """Cycle through neon colors for visual effects"""
        colors = [self.neon_green, self.neon_pink, self.neon_blue, self.neon_cyan]
        self.current_neon_color = random.choice(colors)
        
        # Update random border colors
        if hasattr(self, 'response_text'):
            # Subtle color cycling
            pass
            
        self.root.after(5000, self.cycle_neon_colors)
        
    def add_response(self, message, tag="ai"):
        """Add response to terminal with cyberpunk formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        self.response_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        if tag == "user":
            self.response_text.insert(tk.END, "USER_INPUT> ", "user")
        elif tag == "ai":
            self.response_text.insert(tk.END, "SHADOW_AI> ", "ai")
        elif tag == "system":
            self.response_text.insert(tk.END, "SYSTEM> ", "system")
        elif tag == "error":
            self.response_text.insert(tk.END, "ERROR> ", "error")
            
        self.response_text.insert(tk.END, f"{message}\n\n", tag)
        self.response_text.see(tk.END)
        
    def update_status(self, status):
        """Update status with cyberpunk styling"""
        status_messages = {
            "ready": "[ONLINE] SHADOW AI NEURAL NETWORK ACTIVE",
            "processing": "[PROCESSING] QUANTUM CORES COMPUTING...",
            "listening": "[INPUT] NEURAL MIC INTERFACE ACTIVE",
            "error": "[ERROR] SYSTEM MALFUNCTION DETECTED",
            "success": "[SUCCESS] OPERATION COMPLETED"
        }
        
        for key, msg in status_messages.items():
            if key in status.lower():
                self.status_label.config(text=msg)
                return
        
        self.status_label.config(text=f"[STATUS] {status.upper()}")
        
    def process_command(self, event=None):
        """Process command with cyberpunk effects"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.command_entry.delete(0, tk.END)
        
        # Show processing status
        self.update_status("processing")
        self.process_btn.config(state="disabled", text="[ COMPUTING... ]")
        
        # Add user command to display
        self.add_response(command, "user")
        
        # Process in background thread
        thread = threading.Thread(target=self._process_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
        
        # Check for response
        self.root.after(100, self.check_response)
        
    def _process_command_thread(self, command):
        """Process command in background thread"""
        try:
            response = process_command(command)
            self.response_queue.put(("success", response))
        except Exception as e:
            self.response_queue.put(("error", str(e)))
    
    def check_response(self):
        """Check for response from processing thread"""
        try:
            result_type, response = self.response_queue.get_nowait()
            
            if result_type == "success":
                self.add_response(response, "ai")
                if self.voice_enabled:
                    # Speak response in background
                    thread = threading.Thread(target=speak_response, args=(response,))
                    thread.daemon = True
                    thread.start()
                self.update_status("success")
            else:
                self.add_response(f"NEURAL_ERROR: {response}", "error")
                self.update_status("error")
                
            # Reset UI
            self.process_btn.config(state="normal", text="[ EXECUTE ]")
            
        except queue.Empty:
            # No response yet, check again
            self.root.after(100, self.check_response)
    
    def voice_input(self):
        """Handle voice input with cyberpunk styling"""
        if not self.voice_enabled:
            self.add_response("NEURAL_MIC interface not available in this configuration", "error")
            return
            
        self.update_status("listening")
        self.voice_btn.config(state="disabled", text="[ LISTENING... ]")
        
        # Get voice input in background thread
        thread = threading.Thread(target=self._voice_input_thread)
        thread.daemon = True
        thread.start()
        
        # Check for voice input result
        self.root.after(100, self.check_voice_input)
    
    def _voice_input_thread(self):
        """Get voice input in background thread"""
        try:
            command = get_voice_input("Neural interface listening...")
            self.response_queue.put(("voice", command))
        except Exception as e:
            self.response_queue.put(("voice_error", str(e)))
    
    def check_voice_input(self):
        """Check for voice input result"""
        try:
            result_type, result = self.response_queue.get_nowait()
            
            if result_type == "voice" and result:
                self.command_entry.insert(0, result)
                self.add_response(f"NEURAL_INPUT_CAPTURED: {result}", "system")
            elif result_type == "voice_error":
                self.add_response(f"NEURAL_MIC_ERROR: {result}", "error")
            
            # Reset voice button
            if self.voice_enabled:
                self.voice_btn.config(state="normal", text="[ NEURAL_MIC ]")
            self.update_status("ready")
            
        except queue.Empty:
            # No result yet, check again
            self.root.after(100, self.check_voice_input)
    
    def clear_output(self):
        """Clear output terminal"""
        self.response_text.delete(1.0, tk.END)
        self.add_response("NEURAL MATRIX PURGED. READY FOR NEW OPERATIONS.", "system")
    
    def run(self):
        """Run the cyberpunk GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Cyberpunk GUI terminated by user")

def main():
    """Main function to run the cyberpunk GUI"""
    try:
        app = ShadowCyberpunkGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Cyberpunk GUI: {e}")
        messagebox.showerror("System Error", f"Failed to initialize cyberpunk interface: {e}")

if __name__ == "__main__":
    main()
