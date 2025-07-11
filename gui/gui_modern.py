#!/usr/bin/env python3
"""
Shadow AI - Modern GUI
Clean, professional design with modern styling
"""

import sys
import os
import customtkinter as ctk
import threading
import queue
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.gpt_agent import GPTAgent, process_command
from input.voice_input import get_voice_input, speak_response
from config import VOICE_ENABLED

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ShadowModernGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Shadow AI - Modern Interface")
        self.root.geometry("900x700")
        
        # Initialize AI agent
        self.ai_agent = GPTAgent()
        self.voice_enabled = VOICE_ENABLED
        
        # Queue for thread communication
        self.response_queue = queue.Queue()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the modern user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🧠 Shadow AI",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Modern AI Assistant Interface",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitle_label.pack()
        
        # Status
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🟢 Ready • AI Agent Initialized",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(pady=(5, 0))
        
        # Input section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="Enter your command:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        input_label.pack(fill="x", padx=20, pady=(20, 5))
        
        # Command input
        self.command_entry = ctk.CTkEntry(
            input_frame,
            height=40,
            font=ctk.CTkFont(size=13),
            placeholder_text="Type your command here... (e.g., 'Open notepad and write a note')"
        )
        self.command_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.command_entry.bind("<Return>", self.process_command)
        
        # Buttons
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.process_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Process Command",
            command=self.process_command,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.process_btn.pack(side="left", padx=(0, 10))
        
        if self.voice_enabled:
            self.voice_btn = ctk.CTkButton(
                button_frame,
                text="🎤 Voice Input",
                command=self.voice_input,
                height=35,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="green",
                hover_color="darkgreen"
            )
            self.voice_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_output,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="red",
            hover_color="darkred"
        )
        clear_btn.pack(side="left")
        
        # Output section
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="Response:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        output_label.pack(fill="x", padx=20, pady=(20, 5))
        
        # Response text area
        self.response_text = ctk.CTkTextbox(
            output_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.response_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Welcome message
        self.add_response("🧠 Shadow AI Modern Interface Initialized!\n\nWelcome to your intelligent personal assistant. I can help you with:\n\n✨ Document creation and editing\n🌐 Web browsing and research\n📱 Application control\n🎯 Task automation\n📊 Data analysis\n\nTry a command like:\n• 'Create a presentation about AI'\n• 'Find the best laptops under $1000'\n• 'Write an email to my team'\n\nWhat would you like me to do today?")
        
    def add_response(self, message):
        """Add response to the text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        current_text = self.response_text.get("1.0", "end-1c")
        if current_text:
            new_text = f"{current_text}\n\n[{timestamp}] {message}"
        else:
            new_text = f"[{timestamp}] {message}"
        
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", new_text)
        
    def update_status(self, status, color="gray60"):
        """Update status label"""
        status_icons = {
            "Ready": "🟢",
            "Processing": "🟡",
            "Listening": "🎤",
            "Error": "🔴"
        }
        
        for key, icon in status_icons.items():
            if key.lower() in status.lower():
                status = f"{icon} {status}"
                break
        
        self.status_label.configure(text=status)
        
    def process_command(self, event=None):
        """Process the entered command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.command_entry.delete(0, "end")
        
        # Show processing status
        self.update_status("Processing command...")
        self.process_btn.configure(state="disabled", text="⏳ Processing...")
        
        # Add user command to display
        self.add_response(f"👤 User: {command}")
        
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
                self.add_response(f"🤖 Shadow AI: {response}")
                if self.voice_enabled:
                    # Speak response in background
                    thread = threading.Thread(target=speak_response, args=(response,))
                    thread.daemon = True
                    thread.start()
            else:
                self.add_response(f"❌ Error: {response}")
                
            # Reset UI
            self.update_status("Ready")
            self.process_btn.configure(state="normal", text="🚀 Process Command")
            
        except queue.Empty:
            # No response yet, check again
            self.root.after(100, self.check_response)
    
    def voice_input(self):
        """Handle voice input"""
        if not self.voice_enabled:
            self.add_response("❌ Voice input is not available")
            return
            
        self.update_status("Listening...")
        self.voice_btn.configure(state="disabled", text="🎤 Listening...")
        
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
                self.add_response(f"🎤 Voice Input: {result}")
            elif result_type == "voice_error":
                self.add_response(f"❌ Voice Input Error: {result}")
            
            # Reset voice button
            if self.voice_enabled:
                self.voice_btn.configure(state="normal", text="🎤 Voice Input")
            self.update_status("Ready")
            
        except queue.Empty:
            # No result yet, check again
            self.root.after(100, self.check_voice_input)
    
    def clear_output(self):
        """Clear the output text area"""
        self.response_text.delete("1.0", "end")
        self.add_response("✨ Output cleared. Ready for new commands!")
    
    def run(self):
        """Run the GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("GUI closed by user")

def main():
    """Main function to run the GUI"""
    try:
        app = ShadowModernGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Failed to start Shadow AI GUI: {e}")

if __name__ == "__main__":
    main()
