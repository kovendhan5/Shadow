#!/usr/bin/env python3
"""
Quick Orpheus Launcher
Simple GUI to launch different Orpheus modes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading

class OrpheusLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎭 Orpheus Emotional AI Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg="#1a1a2e")
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_gui()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")
    
    def setup_gui(self):
        """Setup the launcher GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎭 Orpheus Emotional AI",
            font=("Arial", 24, "bold"),
            fg="#ff6b6b",
            bg="#1a1a2e"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Emotionally Intelligent Conversations",
            font=("Arial", 12),
            fg="#4ecdc4",
            bg="#1a1a2e"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1a1a2e")
        button_frame.pack(fill="both", expand=True)
        
        # Buttons configuration
        buttons = [
            ("🎨 Beautiful GUI", "Launch the full Orpheus emotional interface", self.launch_gui),
            ("🎬 Interactive Demo", "Try Orpheus with example conversations", self.launch_demo),
            ("🔧 Quick Test", "Verify Orpheus is working correctly", self.run_test),
            ("📚 User Guide", "Learn about Orpheus emotional AI", self.show_guide),
        ]
        
        for i, (text, tooltip, command) in enumerate(buttons):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                fg="white",
                bg="#16537e",
                activebackground="#1e6ba8",
                activeforeground="white",
                relief="flat",
                padx=20,
                pady=10,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=5)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1e6ba8"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#16537e"))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg="#1a1a2e")
        status_frame.pack(fill="x", pady=(20, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="🎭 Orpheus is ready for emotional conversations",
            font=("Arial", 10),
            fg="#95a5a6",
            bg="#1a1a2e"
        )
        self.status_label.pack()
        
        # Exit button
        exit_btn = tk.Button(
            main_frame,
            text="❌ Exit",
            command=self.root.quit,
            font=("Arial", 10),
            fg="#e74c3c",
            bg="#1a1a2e",
            relief="flat",
            cursor="hand2"
        )
        exit_btn.pack(pady=(10, 0))
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        self.root.update()
    
    def launch_gui(self):
        """Launch Orpheus GUI"""
        self.update_status("🚀 Launching Orpheus GUI...")
        try:
            subprocess.Popen([sys.executable, "gui_orpheus.py"])
            self.update_status("✅ Orpheus GUI launched successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GUI: {e}")
            self.update_status("❌ Failed to launch GUI")
    
    def launch_demo(self):
        """Launch Orpheus demo"""
        self.update_status("🎬 Starting Orpheus demo...")
        try:
            subprocess.Popen([sys.executable, "demo_orpheus.py"])
            self.update_status("✅ Demo launched successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch demo: {e}")
            self.update_status("❌ Failed to launch demo")
    
    def run_test(self):
        """Run Orpheus test"""
        def test_thread():
            self.update_status("🔧 Testing Orpheus...")
            try:
                result = subprocess.run([sys.executable, "test_orpheus.py"], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.update_status("✅ Orpheus test completed successfully!")
                    messagebox.showinfo("Test Results", "Orpheus is working correctly!")
                else:
                    self.update_status("❌ Test failed")
                    messagebox.showerror("Test Failed", result.stderr or "Test failed")
            except subprocess.TimeoutExpired:
                self.update_status("⏰ Test timed out")
                messagebox.showwarning("Timeout", "Test took too long to complete")
            except Exception as e:
                self.update_status("❌ Test error")
                messagebox.showerror("Error", f"Test error: {e}")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def show_guide(self):
        """Show user guide"""
        guide_text = """🎭 Orpheus Emotional AI Quick Guide

🌟 WHAT IS ORPHEUS?
Orpheus is an emotionally intelligent AI that understands and responds to your emotions.

🚀 HOW TO USE:
1. Click "Beautiful GUI" for the full visual experience
2. Start typing messages to Orpheus
3. Watch the emotion indicator change as you chat
4. Switch between Orpheus and Shadow AI modes

💝 EMOTIONS SUPPORTED:
Happy, Sad, Excited, Calm, Curious, Empathetic, 
Confident, Playful, Thoughtful, Encouraging, and more!

🎨 FEATURES:
• Real-time emotion recognition
• Beautiful animated visual indicators  
• Conversation export and analytics
• Dual AI mode (Emotional + Functional)

📝 TIPS:
• Use emotional words in your messages
• Try different moods to see Orpheus adapt
• Ask questions for engaging conversations
• Export conversations to save your chats

🔧 REQUIREMENTS:
• Gemini API key configured in .env file
• Python 3.7+ with required packages

Happy chatting with Orpheus! 🎭✨"""
        
        # Create guide window
        guide_window = tk.Toplevel(self.root)
        guide_window.title("📚 Orpheus User Guide")
        guide_window.geometry("600x500")
        guide_window.configure(bg="#1a1a2e")
        guide_window.resizable(False, False)
        
        # Center guide window
        guide_window.transient(self.root)
        guide_window.grab_set()
        
        # Guide text
        text_widget = tk.Text(
            guide_window,
            wrap="word",
            font=("Arial", 11),
            bg="#2c2c54",
            fg="white",
            relief="flat",
            padx=20,
            pady=20
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", guide_text)
        text_widget.config(state="disabled")
        
        # Close button
        close_btn = tk.Button(
            guide_window,
            text="Close",
            command=guide_window.destroy,
            font=("Arial", 10),
            bg="#16537e",
            fg="white",
            relief="flat",
            padx=20
        )
        close_btn.pack(pady=(0, 20))
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        launcher = OrpheusLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error starting launcher: {e}")
        import traceback
        traceback.print_exc()
