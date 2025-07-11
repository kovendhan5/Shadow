#!/usr/bin/env python3
"""
Shadow AI - Working GUI
Simple, reliable, and functional interface
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.gpt_agent import GPTAgent, process_command
from input.voice_input import get_voice_input, speak_response
from input.text_input import show_message
from config import VOICE_ENABLED

class ShadowWorkingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shadow AI - Working Interface")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize AI agent
        self.ai_agent = GPTAgent()
        self.voice_enabled = VOICE_ENABLED
        
        # Queue for thread communication
        self.response_queue = queue.Queue()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="🧠 Shadow AI - Working Interface",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack()
        
        # Status
        self.status_label = tk.Label(
            title_frame,
            text="Ready • AI Agent Initialized",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        self.status_label.pack()
        
        # Input frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            input_frame,
            text="Enter your command:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        # Command input
        self.command_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            relief="solid",
            borderwidth=1
        )
        self.command_entry.pack(fill="x", pady=5)
        self.command_entry.bind("<Return>", self.process_command)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Process button
        self.process_btn = tk.Button(
            button_frame,
            text="🚀 Process Command",
            command=self.process_command,
            bg="#007acc",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="solid",
            borderwidth=0,
            cursor="hand2"
        )
        self.process_btn.pack(side="left", padx=(0, 5))
        
        # Voice button
        if self.voice_enabled:
            self.voice_btn = tk.Button(
                button_frame,
                text="🎤 Voice Input",
                command=self.voice_input,
                bg="#28a745",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="solid",
                borderwidth=0,
                cursor="hand2"
            )
            self.voice_btn.pack(side="left", padx=(0, 5))
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_output,
            bg="#dc3545",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="solid",
            borderwidth=0,
            cursor="hand2"
        )
        clear_btn.pack(side="left")
        
        # Output frame
        output_frame = tk.Frame(self.root, bg="#f0f0f0")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(
            output_frame,
            text="Response:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor="w")
        
        # Response text area
        self.response_text = scrolledtext.ScrolledText(
            output_frame,
            font=("Consolas", 10),
            bg="white",
            fg="#333",
            relief="solid",
            borderwidth=1,
            wrap=tk.WORD
        )
        self.response_text.pack(fill="both", expand=True, pady=5)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#f0f0f0")
        footer_frame.pack(fill="x", padx=10, pady=5)
        
        footer_label = tk.Label(
            footer_frame,
            text="Shadow AI v1.0 - Your Personal AI Assistant",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#999"
        )
        footer_label.pack()
        
        # Welcome message
        self.add_response("🧠 Shadow AI Working Interface Initialized!\n\nI'm ready to help you with any computer task. Try commands like:\n• 'Open notepad and write a note'\n• 'Take a screenshot'\n• 'Search for information about AI'\n\nWhat would you like me to do?")
        
    def add_response(self, message):
        """Add response to the text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.response_text.insert(tk.END, f"[{timestamp}] {message}\n\n")
        self.response_text.see(tk.END)
        
    def update_status(self, status):
        """Update status label"""
        self.status_label.config(text=status)
        
    def process_command(self, event=None):
        """Process the entered command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.command_entry.delete(0, tk.END)
        
        # Show processing status
        self.update_status("Processing command...")
        self.process_btn.config(state="disabled", text="⏳ Processing...")
        
        # Add user command to display
        self.add_response(f"User: {command}")
        
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
                self.add_response(f"Shadow AI: {response}")
                if self.voice_enabled:
                    # Speak response in background
                    thread = threading.Thread(target=speak_response, args=(response,))
                    thread.daemon = True
                    thread.start()
            else:
                self.add_response(f"Error: {response}")
                
            # Reset UI
            self.update_status("Ready")
            self.process_btn.config(state="normal", text="🚀 Process Command")
            
        except queue.Empty:
            # No response yet, check again
            self.root.after(100, self.check_response)
    
    def voice_input(self):
        """Handle voice input"""
        if not self.voice_enabled:
            messagebox.showwarning("Voice Disabled", "Voice input is not available")
            return
            
        self.update_status("Listening...")
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
                self.command_entry.insert(0, result)
                self.add_response(f"Voice Input: {result}")
            elif result_type == "voice_error":
                self.add_response(f"Voice Input Error: {result}")
            
            # Reset voice button
            self.voice_btn.config(state="normal", text="🎤 Voice Input")
            self.update_status("Ready")
            
        except queue.Empty:
            # No result yet, check again
            self.root.after(100, self.check_voice_input)
    
    def clear_output(self):
        """Clear the output text area"""
        self.response_text.delete(1.0, tk.END)
        self.add_response("Output cleared. Ready for new commands!")
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("GUI closed by user")

def main():
    """Main function to run the GUI"""
    try:
        app = ShadowWorkingGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        messagebox.showerror("Error", f"Failed to start Shadow AI GUI: {e}")

if __name__ == "__main__":
    main()
