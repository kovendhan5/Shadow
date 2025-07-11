#!/usr/bin/env python3
"""
Shadow AI - Modern Minimal GUI
Beautiful, modern interface with guaranteed compatibility
"""

import sys
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import queue
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ModernShadowAI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shadow AI - Modern Interface")
        self.root.geometry("1000x700")
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#1e1e1e',      # Dark background
            'bg_secondary': '#2d2d2d',    # Slightly lighter
            'bg_accent': '#3c3c3c',       # Accent areas
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#cccccc',  # Light gray text
            'text_muted': '#888888',      # Muted text
            'accent_blue': '#007acc',     # Modern blue
            'accent_green': '#4caf50',    # Success green
            'accent_orange': '#ff9800',   # Warning orange
            'accent_red': '#f44336',      # Error red
            'border': '#404040',          # Border color
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Queue for responses
        self.response_queue = queue.Queue()
        
        # Setup modern styling
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        
        # Configure modern styles
        style.configure('Modern.TFrame', 
                       background=self.colors['bg_secondary'],
                       relief='flat')
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_accent'],
                       relief='solid',
                       borderwidth=1)
        
    def setup_ui(self):
        """Setup modern UI with beautiful design"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section with gradient-like effect
        header_frame = tk.Frame(main_container, 
                               bg=self.colors['bg_secondary'], 
                               relief="flat",
                               bd=0)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title with modern typography
        title_container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        title_container.pack(fill="x", padx=30, pady=25)
        
        title_label = tk.Label(
            title_container,
            text="🧠 Shadow AI",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_container,
            text="Modern AI Assistant • Always Ready",
            font=("Segoe UI", 12),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Status indicator with modern design
        status_container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        status_container.pack(fill="x", padx=30, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_container,
            text="🟢 Ready • Modern Interface Active",
            font=("Segoe UI", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_green']
        )
        self.status_label.pack()
        
        # Input section with modern card design
        input_card = tk.Frame(main_container, 
                             bg=self.colors['bg_secondary'],
                             relief="flat",
                             bd=0)
        input_card.pack(fill="x", pady=(0, 20))
        
        input_inner = tk.Frame(input_card, bg=self.colors['bg_secondary'])
        input_inner.pack(fill="x", padx=30, pady=25)
        
        # Input label with modern styling
        input_label = tk.Label(
            input_inner,
            text="💬 Enter your command:",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        input_label.pack(anchor="w", pady=(0, 15))
        
        # Modern input field
        input_container = tk.Frame(input_inner, bg=self.colors['bg_secondary'])
        input_container.pack(fill="x", pady=(0, 20))
        
        self.command_entry = tk.Entry(
            input_container,
            font=("Segoe UI", 13),
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor=self.colors['accent_blue'],
            highlightbackground=self.colors['border']
        )
        self.command_entry.pack(fill="x", ipady=12, ipadx=15)
        self.command_entry.bind("<Return>", self.process_command)
        
        # Placeholder text functionality
        self.placeholder_text = "Type your command here... (e.g., 'hello', 'help', 'what can you do')"
        self.command_entry.insert(0, self.placeholder_text)
        self.command_entry.config(fg=self.colors['text_muted'])
        self.command_entry.bind("<FocusIn>", self.clear_placeholder)
        self.command_entry.bind("<FocusOut>", self.restore_placeholder)
        
        # Modern button with hover effect simulation
        button_container = tk.Frame(input_inner, bg=self.colors['bg_secondary'])
        button_container.pack(fill="x")
        
        self.process_btn = tk.Button(
            button_container,
            text="🚀 Process Command",
            command=self.process_command,
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary'],
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#0056b3",
            activeforeground=self.colors['text_primary']
        )
        self.process_btn.pack(side="left", ipady=10, ipadx=20)
        
        # Clear button
        clear_btn = tk.Button(
            button_container,
            text="🗑️ Clear",
            command=self.clear_output,
            bg=self.colors['accent_red'],
            fg=self.colors['text_primary'],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#d32f2f",
            activeforeground=self.colors['text_primary']
        )
        clear_btn.pack(side="left", padx=(15, 0), ipady=10, ipadx=15)
        
        # Help button
        help_btn = tk.Button(
            button_container,
            text="❓ Help",
            command=lambda: self.process_specific_command("help"),
            bg=self.colors['accent_orange'],
            fg=self.colors['text_primary'],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#f57c00",
            activeforeground=self.colors['text_primary']
        )
        help_btn.pack(side="left", padx=(15, 0), ipady=10, ipadx=15)
        
        # Output section with modern card design
        output_card = tk.Frame(main_container, 
                              bg=self.colors['bg_secondary'],
                              relief="flat",
                              bd=0)
        output_card.pack(fill="both", expand=True)
        
        output_inner = tk.Frame(output_card, bg=self.colors['bg_secondary'])
        output_inner.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Output label
        output_label = tk.Label(
            output_inner,
            text="💬 AI Response & Activity Log:",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        output_label.pack(anchor="w", pady=(0, 15))
        
        # Modern text area with custom styling
        text_container = tk.Frame(output_inner, bg=self.colors['bg_secondary'])
        text_container.pack(fill="both", expand=True)
        
        self.response_text = scrolledtext.ScrolledText(
            text_container,
            font=("Consolas", 11),
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief="flat",
            bd=0,
            wrap=tk.WORD,
            selectbackground=self.colors['accent_blue'],
            selectforeground=self.colors['text_primary'],
            highlightthickness=0
        )
        self.response_text.pack(fill="both", expand=True)
        
        # Configure text tags for colored output
        self.response_text.tag_configure("user", 
                                        foreground=self.colors['accent_blue'], 
                                        font=("Consolas", 11, "bold"))
        self.response_text.tag_configure("ai", 
                                        foreground=self.colors['accent_green'])
        self.response_text.tag_configure("error", 
                                        foreground=self.colors['accent_red'])
        self.response_text.tag_configure("timestamp", 
                                        foreground=self.colors['text_muted'], 
                                        font=("Consolas", 9))
        self.response_text.tag_configure("system", 
                                        foreground=self.colors['accent_orange'])
        
        # Welcome message with modern styling
        welcome_msg = """🎉 Welcome to Shadow AI Modern Interface!

I'm your intelligent personal assistant, ready to help with any task.

✨ KEY FEATURES:
• Natural language processing
• Task automation capabilities  
• Modern, responsive interface
• Built-in help and guidance

🚀 QUICK START COMMANDS:
• 'hello' - Greet me
• 'help' - See all available commands
• 'what can you do' - Learn about my capabilities
• 'configure' - Setup instructions

💡 TIP: I work even without API keys configured! Try asking me anything.

What would you like me to help you with today?"""
        
        self.add_response(welcome_msg, "system")
        
    def clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.command_entry.get() == self.placeholder_text:
            self.command_entry.delete(0, tk.END)
            self.command_entry.config(fg=self.colors['text_primary'])
    
    def restore_placeholder(self, event):
        """Restore placeholder text if empty"""
        if not self.command_entry.get():
            self.command_entry.insert(0, self.placeholder_text)
            self.command_entry.config(fg=self.colors['text_muted'])
    
    def add_response(self, message, tag="ai"):
        """Add response to output with modern formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.response_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.response_text.insert(tk.END, f"{message}\n\n", tag)
        self.response_text.see(tk.END)
    
    def clear_output(self):
        """Clear the output area"""
        self.response_text.delete(1.0, tk.END)
        self.add_response("✨ Output cleared. Ready for new commands!", "system")
    
    def process_specific_command(self, command):
        """Process a specific command"""
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, command)
        self.command_entry.config(fg=self.colors['text_primary'])
        self.process_command()
    
    def update_status(self, status, color_key="text_secondary"):
        """Update status with color"""
        self.status_label.config(text=status, fg=self.colors[color_key])
        
    def process_command(self, event=None):
        """Process user command with modern feedback"""
        command = self.command_entry.get().strip()
        if not command or command == self.placeholder_text:
            return
        
        # Clear input and restore proper styling
        self.command_entry.delete(0, tk.END)
        self.restore_placeholder(None)
        
        # Add user message with modern styling
        self.add_response(f"👤 User: {command}", "user")
        
        # Update UI for processing
        self.update_status("🟡 Processing command...", "accent_orange")
        self.process_btn.config(text="⏳ Processing...", state="disabled")
        
        # Get response
        response = self.get_builtin_response(command)
        
        if response:
            self.add_response(f"🤖 Shadow AI: {response}", "ai")
            self.update_status("🟢 Ready • Modern Interface Active", "accent_green")
            self.process_btn.config(text="🚀 Process Command", state="normal")
        else:
            # Try AI processing in background
            try:
                thread = threading.Thread(target=self._ai_process_thread, args=(command,))
                thread.daemon = True
                thread.start()
                self.root.after(100, self.check_ai_response)
            except Exception as e:
                self.add_response(f"🤖 Shadow AI: I understand you want me to '{command}'. While I'm working on processing this with full AI capabilities, let me help you with what I can do right now. Try 'help' for available commands!", "ai")
                self.update_status("� Ready • Modern Interface Active", "accent_green")
                self.process_btn.config(text="🚀 Process Command", state="normal")
    
    def get_builtin_response(self, command):
        """Enhanced built-in responses with modern personality"""
        command_lower = command.lower()
        
        if command_lower in ['hello', 'hi', 'hey', 'greetings']:
            return """Hello! 👋 I'm Shadow AI, your modern personal assistant.

I'm here to help you with anything you need. I have a friendly personality and can assist with:
• Answering questions and providing information
• Helping you understand Shadow AI capabilities  
• Guiding you through setup and configuration
• General conversation and assistance

What would you like to explore together?"""
        
        elif command_lower in ['help', 'what can you do', 'commands', '?']:
            return """🎯 Shadow AI Capabilities & Commands:

📋 BASIC COMMANDS:
• 'hello' - Friendly greeting and introduction
• 'help' - Show this help message  
• 'what is shadow ai' - Learn about the system
• 'configure' or 'setup' - Configuration guidance
• 'interfaces' - See available UI options
• 'clear' - Clear the conversation

🤖 AI FEATURES (when configured):
• Natural language task processing
• Computer automation and control
• Document creation and editing
• Web browsing and research
• Voice interaction support

💡 TIPS:
• I work even without API keys configured!
• Try asking me questions naturally
• Use the Clear button to reset our conversation
• The Help button gives you quick access to this info

What would you like me to help you with?"""
        
        elif 'shadow ai' in command_lower or 'what is' in command_lower:
            return """🧠 About Shadow AI:

Shadow AI is a comprehensive personal AI assistant designed to be your intelligent computer companion. Here's what makes it special:

✨ KEY FEATURES:
• Universal task automation - Control any aspect of your computer
• Multiple beautiful interfaces - Choose your preferred style
• Natural language processing - Talk to me like a human
• Document creation - Letters, reports, presentations
• Web automation - Browsing, research, form filling
• Voice interaction - Speak commands naturally

🎨 INTERFACE OPTIONS:
• Modern (current) - Beautiful, responsive design
• Premium - Elegant glassmorphism effects
• Cyberpunk - Futuristic neon aesthetics  
• Working - Simple, reliable interface

🔧 SETUP:
To unlock full AI capabilities, configure your API key in the .env file and restart the application.

Ready to transform your productivity?"""
        
        elif 'configure' in command_lower or 'setup' in command_lower or 'api' in command_lower:
            return """⚙️ Shadow AI Configuration Guide:

🔑 SETUP STEPS:
1. Open the .env file in your Shadow AI folder
2. Find the line: GEMINI_API_KEY=your_gemini_key_here
3. Replace 'your_gemini_key_here' with your actual Gemini API key
4. Save the file and restart Shadow AI

🆓 GET A FREE API KEY:
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your .env file

💡 ALTERNATIVE:
You can also use OpenAI API keys by configuring OPENAI_API_KEY in the same file.

🎯 AFTER SETUP:
• Full AI processing capabilities
• Advanced task automation
• Natural language understanding
• Voice interaction support

Need help with any of these steps?"""
        
        elif 'interface' in command_lower or 'gui' in command_lower or 'ui' in command_lower:
            return """🎨 Shadow AI Interface Options:

🖥️ AVAILABLE INTERFACES:
• Modern GUI (current) - What you're using now! Clean, beautiful design
• Premium GUI - Elegant glassmorphism with advanced features
• Cyberpunk GUI - Futuristic neon theme with animations
• Working GUI - Simple, reliable interface
• Command Line - Terminal-based interaction

🚀 HOW TO SWITCH:
• Run: python launchers\\launch_gui_new.py
• Or use the main launcher: launch.bat
• Or directly: python gui\\gui_premium.py

✨ MODERN INTERFACE FEATURES:
• Dark theme optimized for long use
• Responsive design that scales beautifully
• Intuitive controls and clear feedback
• Built-in help and guidance
• Placeholder text to guide you

Each interface has its own personality while maintaining full functionality!"""
        
        elif command_lower in ['thanks', 'thank you', 'thx']:
            return """You're very welcome! 😊 

I'm always happy to help. Feel free to ask me anything else - whether it's about Shadow AI features, configuration help, or just having a conversation.

Is there anything else you'd like to explore or learn about?"""
        
        elif command_lower in ['bye', 'goodbye', 'exit', 'quit']:
            return """Goodbye! 👋 

Thanks for using Shadow AI. I hope I was helpful today!

Remember, I'm always here when you need assistance. Just restart the interface anytime you want to continue our conversation.

Have a great day! ✨"""
        
        return None
    
    def _ai_process_thread(self, command):
        """Try to process with real AI in background"""
        try:
            from brain.gpt_agent import process_command
            response = process_command(command)
            self.response_queue.put(("success", response))
        except Exception as e:
            self.response_queue.put(("error", str(e)))
    
    def check_ai_response(self):
        """Check for AI response with modern feedback"""
        try:
            result_type, response = self.response_queue.get_nowait()
            
            if result_type == "success":
                self.add_response(f"🤖 Shadow AI: {response}", "ai")
                self.update_status("🟢 Ready • AI Processing Complete", "accent_green")
            else:
                self.add_response(f"🤖 Shadow AI: I tried to process your request with full AI capabilities, but I'm currently running in basic mode. I can still help you with built-in commands and guidance. Try 'help' to see what I can do!", "ai")
                self.update_status("🟢 Ready • Basic Mode Active", "accent_green")
            
            self.process_btn.config(text="🚀 Process Command", state="normal")
            
        except queue.Empty:
            self.root.after(100, self.check_ai_response)
    
    def run(self):
        """Run the modern GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Modern GUI closed")

def main():
    """Main function"""
    try:
        app = ModernShadowAI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to start: {e}")

if __name__ == "__main__":
    main()
