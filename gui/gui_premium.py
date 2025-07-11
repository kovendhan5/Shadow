#!/usr/bin/env python3
"""
Shadow AI - Premium GUI
Elegant glassmorphism design with advanced features
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.gpt_agent import GPTAgent, process_command
from input.voice_input import get_voice_input, speak_response
from config import VOICE_ENABLED

class ShadowPremiumGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shadow AI - Premium Interface")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize AI agent
        self.ai_agent = GPTAgent()
        self.voice_enabled = VOICE_ENABLED
        
        # Queue for thread communication
        self.response_queue = queue.Queue()
        
        # Command history
        self.command_history = []
        self.history_index = -1
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Setup custom styles for premium look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Premium.TFrame', background='#1a1a2e', relief='flat')
        style.configure('Card.TFrame', background='#16213e', relief='solid', borderwidth=1)
        style.configure('Premium.TLabel', background='#1a1a2e', foreground='#ffffff', font=('Arial', 10))
        style.configure('Title.TLabel', background='#1a1a2e', foreground='#4fc3f7', font=('Arial', 16, 'bold'))
        style.configure('Premium.TButton', background='#4fc3f7', foreground='#ffffff', font=('Arial', 10, 'bold'))
        
    def setup_ui(self):
        """Setup the premium user interface"""
        # Main container with glassmorphism effect
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_frame, bg="#16213e", relief="solid", bd=1)
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Title section
        title_frame = tk.Frame(header_frame, bg="#16213e")
        title_frame.pack(fill="x", padx=20, pady=15)
        
        # Animated title
        title_label = tk.Label(
            title_frame,
            text="🧠 Shadow AI Premium",
            font=("Arial", 24, "bold"),
            bg="#16213e",
            fg="#4fc3f7"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced AI Assistant • Premium Experience",
            font=("Arial", 12),
            bg="#16213e",
            fg="#81c784"
        )
        subtitle_label.pack()
        
        # Status bar with indicators
        status_frame = tk.Frame(header_frame, bg="#16213e")
        status_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 AI Agent Ready • Premium Mode Active",
            font=("Arial", 10),
            bg="#16213e",
            fg="#a5d6a7"
        )
        self.status_label.pack(side="left")
        
        # System info
        system_label = tk.Label(
            status_frame,
            text=f"v1.0 • {datetime.now().strftime('%Y-%m-%d')}",
            font=("Arial", 9),
            bg="#16213e",
            fg="#78909c"
        )
        system_label.pack(side="right")
        
        # Input section with card design
        input_card = tk.Frame(main_frame, bg="#16213e", relief="solid", bd=1)
        input_card.pack(fill="x", pady=(0, 15))
        
        input_inner = tk.Frame(input_card, bg="#16213e")
        input_inner.pack(fill="x", padx=20, pady=20)
        
        input_label = tk.Label(
            input_inner,
            text="💬 Command Interface",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#ffffff"
        )
        input_label.pack(anchor="w", pady=(0, 10))
        
        # Command input with enhanced styling
        input_frame = tk.Frame(input_inner, bg="#16213e")
        input_frame.pack(fill="x", pady=(0, 15))
        
        self.command_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg="#263238",
            fg="#ffffff",
            insertbackground="#4fc3f7",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor="#4fc3f7"
        )
        self.command_entry.pack(fill="x", ipady=8)
        self.command_entry.bind("<Return>", self.process_command)
        self.command_entry.bind("<Up>", self.navigate_history)
        self.command_entry.bind("<Down>", self.navigate_history)
        
        # Placeholder text effect
        self.command_entry.insert(0, "Enter your command here... (e.g., 'Create a presentation about AI')")
        self.command_entry.config(fg="#78909c")
        self.command_entry.bind("<FocusIn>", self.clear_placeholder)
        self.command_entry.bind("<FocusOut>", self.restore_placeholder)
        
        # Enhanced button panel
        button_frame = tk.Frame(input_inner, bg="#16213e")
        button_frame.pack(fill="x")
        
        # Process button with hover effect
        self.process_btn = tk.Button(
            button_frame,
            text="🚀 Execute Command",
            command=self.process_command,
            bg="#4fc3f7",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            activebackground="#29b6f6",
            activeforeground="#ffffff"
        )
        self.process_btn.pack(side="left", padx=(0, 10), ipady=5, ipadx=10)
        
        # Voice button
        if self.voice_enabled:
            self.voice_btn = tk.Button(
                button_frame,
                text="🎤 Voice Input",
                command=self.voice_input,
                bg="#81c784",
                fg="#ffffff",
                font=("Arial", 11, "bold"),
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                activebackground="#66bb6a",
                activeforeground="#ffffff"
            )
            self.voice_btn.pack(side="left", padx=(0, 10), ipady=5, ipadx=10)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Output",
            command=self.clear_output,
            bg="#f06292",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            activebackground="#ec407a",
            activeforeground="#ffffff"
        )
        clear_btn.pack(side="left", padx=(0, 10), ipady=5, ipadx=10)
        
        # History button
        history_btn = tk.Button(
            button_frame,
            text="📋 History",
            command=self.show_history,
            bg="#ba68c8",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            activebackground="#ab47bc",
            activeforeground="#ffffff"
        )
        history_btn.pack(side="left", ipady=5, ipadx=10)
        
        # Output section with card design
        output_card = tk.Frame(main_frame, bg="#16213e", relief="solid", bd=1)
        output_card.pack(fill="both", expand=True)
        
        output_inner = tk.Frame(output_card, bg="#16213e")
        output_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        output_label = tk.Label(
            output_inner,
            text="💬 AI Response & Activity Log",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#ffffff"
        )
        output_label.pack(anchor="w", pady=(0, 10))
        
        # Enhanced response text area
        text_frame = tk.Frame(output_inner, bg="#16213e")
        text_frame.pack(fill="both", expand=True)
        
        self.response_text = scrolledtext.ScrolledText(
            text_frame,
            font=("Consolas", 11),
            bg="#263238",
            fg="#ffffff",
            insertbackground="#4fc3f7",
            relief="flat",
            borderwidth=0,
            wrap=tk.WORD,
            selectbackground="#4fc3f7",
            selectforeground="#000000"
        )
        self.response_text.pack(fill="both", expand=True)
        
        # Configure text tags for colored output
        self.response_text.tag_configure("user", foreground="#4fc3f7", font=("Consolas", 11, "bold"))
        self.response_text.tag_configure("ai", foreground="#81c784", font=("Consolas", 11))
        self.response_text.tag_configure("error", foreground="#f06292", font=("Consolas", 11))
        self.response_text.tag_configure("timestamp", foreground="#78909c", font=("Consolas", 9))
        
        # Welcome message
        self.add_response(
            "🚀 Shadow AI Premium Interface Initialized!\n\n"
            "Welcome to the most advanced personal AI assistant experience. "
            "I'm equipped with cutting-edge capabilities to handle any computer task.\n\n"
            "✨ PREMIUM FEATURES:\n"
            "• Advanced natural language processing\n"
            "• Intelligent task automation\n"
            "• Context-aware responses\n"
            "• Voice interaction support\n"
            "• Command history navigation\n"
            "• Enhanced visual feedback\n\n"
            "🎯 EXAMPLE COMMANDS:\n"
            "• 'Create a professional presentation about machine learning'\n"
            "• 'Research and summarize the latest AI trends'\n"
            "• 'Automate my daily workflow tasks'\n"
            "• 'Write and send a follow-up email'\n\n"
            "Ready to transform your productivity? What shall we accomplish today?",
            "ai"
        )
        
    def clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.command_entry.get() == "Enter your command here... (e.g., 'Create a presentation about AI')":
            self.command_entry.delete(0, tk.END)
            self.command_entry.config(fg="#ffffff")
    
    def restore_placeholder(self, event):
        """Restore placeholder text if empty"""
        if not self.command_entry.get():
            self.command_entry.insert(0, "Enter your command here... (e.g., 'Create a presentation about AI')")
            self.command_entry.config(fg="#78909c")
    
    def navigate_history(self, event):
        """Navigate command history with arrow keys"""
        if not self.command_history:
            return
        
        if event.keysym == "Up":
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
        elif event.keysym == "Down":
            if self.history_index > -1:
                self.history_index -= 1
        
        if self.history_index >= 0:
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[-(self.history_index + 1)])
            self.command_entry.config(fg="#ffffff")
        else:
            self.command_entry.delete(0, tk.END)
            self.restore_placeholder(event)
    
    def add_response(self, message, tag="ai"):
        """Add response to the text area with formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.response_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.response_text.insert(tk.END, f"{message}\n\n", tag)
        self.response_text.see(tk.END)
        
    def update_status(self, status):
        """Update status label with enhanced styling"""
        status_icons = {
            "ready": "🟢",
            "processing": "🟡",
            "listening": "🎤",
            "error": "🔴",
            "success": "✅"
        }
        
        for key, icon in status_icons.items():
            if key in status.lower():
                status = f"{icon} {status}"
                break
        
        self.status_label.config(text=status)
        
    def process_command(self, event=None):
        """Process the entered command"""
        command = self.command_entry.get().strip()
        if not command or command == "Enter your command here... (e.g., 'Create a presentation about AI')":
            return
        
        # Add to history
        if command not in self.command_history:
            self.command_history.append(command)
        self.history_index = -1
        
        # Clear input
        self.command_entry.delete(0, tk.END)
        self.restore_placeholder(None)
        
        # Show processing status
        self.update_status("Processing command...")
        self.process_btn.config(state="disabled", text="⏳ Processing...")
        
        # Add user command to display
        self.add_response(f"👤 User: {command}", "user")
        
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
                self.add_response(f"🤖 Shadow AI: {response}", "ai")
                if self.voice_enabled:
                    # Speak response in background
                    thread = threading.Thread(target=speak_response, args=(response,))
                    thread.daemon = True
                    thread.start()
                self.update_status("Command executed successfully")
            else:
                self.add_response(f"❌ Error: {response}", "error")
                self.update_status("Error occurred")
                
            # Reset UI
            self.process_btn.config(state="normal", text="🚀 Execute Command")
            
        except queue.Empty:
            # No response yet, check again
            self.root.after(100, self.check_response)
    
    def voice_input(self):
        """Handle voice input with enhanced feedback"""
        if not self.voice_enabled:
            self.add_response("❌ Voice input is not available", "error")
            return
            
        self.update_status("Listening for voice input...")
        self.voice_btn.config(state="disabled", text="🎤 Listening...")
        
        # Get voice input in background thread
        thread = threading.Thread(target=self._voice_input_thread)
        thread.daemon = True
        thread.start()
        
        # Check for voice input result
        self.root.after(100, self.check_voice_input)
    
    def _voice_input_thread(self):
        """Get voice input in background thread"""
        try:
            command = get_voice_input("What would you like me to do?")
            self.response_queue.put(("voice", command))
        except Exception as e:
            self.response_queue.put(("voice_error", str(e)))
    
    def check_voice_input(self):
        """Check for voice input result"""
        try:
            result_type, result = self.response_queue.get_nowait()
            
            if result_type == "voice" and result:
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, result)
                self.command_entry.config(fg="#ffffff")
                self.add_response(f"🎤 Voice Input Captured: {result}", "user")
            elif result_type == "voice_error":
                self.add_response(f"❌ Voice Input Error: {result}", "error")
            
            # Reset voice button
            if self.voice_enabled:
                self.voice_btn.config(state="normal", text="🎤 Voice Input")
            self.update_status("Ready")
            
        except queue.Empty:
            # No result yet, check again
            self.root.after(100, self.check_voice_input)
    
    def show_history(self):
        """Show command history dialog"""
        if not self.command_history:
            self.add_response("📋 No command history available", "ai")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Command History")
        history_window.geometry("600x400")
        history_window.configure(bg="#1a1a2e")
        
        # History list
        history_frame = tk.Frame(history_window, bg="#16213e", relief="solid", bd=1)
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(
            history_frame,
            text="📋 Command History",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=10)
        
        history_text = scrolledtext.ScrolledText(
            history_frame,
            font=("Consolas", 10),
            bg="#263238",
            fg="#ffffff",
            relief="flat",
            borderwidth=0
        )
        history_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for i, cmd in enumerate(reversed(self.command_history), 1):
            history_text.insert(tk.END, f"{i:2d}. {cmd}\n")
    
    def clear_output(self):
        """Clear the output text area"""
        self.response_text.delete(1.0, tk.END)
        self.add_response("✨ Output cleared. Premium interface ready for new commands!", "ai")
    
    def run(self):
        """Run the premium GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Premium GUI closed by user")

def main():
    """Main function to run the premium GUI"""
    try:
        app = ShadowPremiumGUI()
        app.run()
    except Exception as e:
        print(f"Error starting Premium GUI: {e}")
        messagebox.showerror("Error", f"Failed to start Shadow AI Premium GUI: {e}")

if __name__ == "__main__":
    main()
