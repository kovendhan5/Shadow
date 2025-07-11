#!/usr/bin/env python3
"""
Shadow AI - Ultra Modern GUI
Beautiful, responsive interface with modern design
"""

import sys
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import queue
from datetime import datetime
import traceback
import logging
import time
from tkinter import filedialog

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Attempt to import core components
try:
    from brain.gpt_agent import LLM_CLIENT, get_llm_client
    from brain.universal_processor import process_universal_command
    from brain.universal_executor import execute_universal_task
    from config import Config
    AI_AVAILABLE = LLM_CLIENT is not None
except ImportError as e:
    print(f"Error importing modules: {e}. Some features may not be available.")
    LLM_CLIENT = None
    AI_AVAILABLE = False
    # Define dummy functions if imports fail
    def process_universal_command(command):
        return None
    class DummyTask:
        def __init__(self, desc):
            self.description = desc
    def execute_universal_task(task):
        class DummyResult:
            def __init__(self):
                self.success = False
                self.error_message = "AI components not loaded."
                self.execution_time = 0
                self.warnings = []
                self.step_results = []
        return DummyResult()

class UltraModernShadowAI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shadow AI - Ultra Modern Interface")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        
        # Ultra modern color palette
        self.theme = {
            'bg_primary': '#0D1117',      # GitHub dark
            'bg_secondary': '#161B22',    # Darker panels
            'bg_tertiary': '#21262D',     # Cards/inputs
            'bg_accent': '#30363D',       # Hover states
            'text_primary': '#F0F6FC',    # Primary text
            'text_secondary': '#8B949E',  # Secondary text
            'text_muted': '#6E7681',      # Muted text
            'accent_blue': '#58A6FF',     # Primary accent
            'accent_green': '#3FB950',    # Success
            'accent_purple': '#A5A5FF',   # Info
            'accent_orange': '#FF8C00',   # Warning
            'accent_red': '#F85149',      # Error
            'border': '#30363D',          # Borders
            'shadow': '#010409',          # Shadows
        }
        
        self.root.configure(bg=self.theme['bg_primary'])
        
        # Font configuration
        self.fonts = {
            'title': ('Segoe UI', 22, 'bold'),
            'subtitle': ('Segoe UI', 11, 'normal'),
            'body': ('Segoe UI', 10, 'normal'),
            'button': ('Segoe UI', 10, 'bold'),
            'monospace': ('Consolas', 9, 'normal')
        }
        
        # Response queue for threading
        self.response_queue = queue.Queue()
        
        # Animation variables
        self.animation_id = None
        self.dots = ""
        
        self.setup_ui()
        self.center_window()
        
        # Start with welcome message
        self.show_welcome_animation()
        
        # Check AI status
        self.update_ai_status()
        
    def update_ai_status(self):
        """Update the AI status indicator."""
        global AI_AVAILABLE
        if AI_AVAILABLE:
            self.status_label.config(text="Status: AI Online", fg=self.theme['accent_green'])
            self.status_dot.config(fg=self.theme['accent_green'])
        else:
            self.status_label.config(text="Status: AI Offline (Check API Key)", fg=self.theme['accent_orange'])
            self.status_dot.config(fg=self.theme['accent_orange'])
            self.insert_response("⚠️ **Warning:** AI client not available. Functionality will be limited. Please ensure your `GEMINI_API_KEY` is correctly set in the `.env` file.", "warning")

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        """Setup ultra modern UI"""
        # Main container with modern styling
        main_frame = tk.Frame(self.root, bg=self.theme['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header with gradient-like effect
        self.create_header(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Output section  
        self.create_output_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Footer
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Create modern header section"""
        header_frame = tk.Frame(parent, bg=self.theme['bg_secondary'], relief="flat")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Inner header with padding
        header_inner = tk.Frame(header_frame, bg=self.theme['bg_secondary'])
        header_inner.pack(fill="x", padx=25, pady=20)
        
        # Title section
        title_frame = tk.Frame(header_inner, bg=self.theme['bg_secondary'])
        title_frame.pack(fill="x")
        
        # Main title with modern styling
        title_label = tk.Label(
            title_frame,
            text="🧠 Shadow AI",
            font=self.fonts['title'],
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary'],
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text=" Ultra Modern Interface",
            font=self.fonts['subtitle'],
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary'],
            anchor="w"
        )
        subtitle_label.pack(side="left", anchor="s", pady=(0, 2), padx=5)
        
        # Settings button
        settings_btn = tk.Button(
            title_frame,
            text="⚙️ Settings",
            font=self.fonts['button'],
            bg=self.theme['bg_accent'],
            fg=self.theme['text_primary'],
            relief="flat",
            command=self.open_settings,
            padx=10, pady=2
        )
        settings_btn.pack(side="right", padx=10)
        
        # Status bar
        status_frame = tk.Frame(header_inner, bg=self.theme['bg_secondary'])
        status_frame.pack(fill="x", pady=(15, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Ready • Ultra Modern Interface Active",
            font=("Segoe UI", 11),
            bg=self.theme['bg_secondary'],
            fg=self.theme['accent_green']
        )
        self.status_label.pack(side="left")
        
        # Version info
        version_label = tk.Label(
            status_frame,
            text="v2.0 • Modern Edition",
            font=("Segoe UI", 9),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_muted']
        )
        version_label.pack(side="right")
        
    def create_input_section(self, parent):
        """Create modern input section"""
        input_card = tk.Frame(parent, bg=self.theme['bg_secondary'], relief="flat")
        input_card.pack(fill="x", pady=(0, 15))
        
        input_inner = tk.Frame(input_card, bg=self.theme['bg_secondary'])
        input_inner.pack(fill="x", padx=25, pady=20)
        
        # Input label
        input_label = tk.Label(
            input_inner,
            text="Your Command:",
            font=self.fonts['body'],
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        input_label.pack(fill="x", padx=20, pady=(15, 5), anchor="w")
        
        # File upload button
        upload_btn = tk.Button(
            input_inner,
            text="📁 Upload File to Knowledge Base",
            font=self.fonts['button'],
            bg=self.theme['accent_purple'],
            fg=self.theme['bg_primary'],
            relief="flat",
            command=self.upload_file,
            padx=10, pady=2
        )
        upload_btn.pack(padx=20, pady=(0, 10), anchor="w")
        
        # Text entry with placeholder
        self.entry = scrolledtext.ScrolledText(
            input_inner,
            height=4,
            bg=self.theme['bg_tertiary'],
            fg=self.theme['text_primary'],
            insertbackground=self.theme['accent_blue'],
            relief="flat",
            borderwidth=1,
            font=self.fonts['body'],
            wrap="word"
        )
        self.entry.pack(fill="x", padx=20, pady=(0, 15), expand=True)
        self.entry.bind("<Return>", self.handle_send)
        
        # Placeholder logic
        self.placeholder = "Type any command... e.g., 'Open notepad and write a poem about robots'"
        self.entry.insert("1.0", self.placeholder)
        self.entry.bind("<FocusIn>", self.on_entry_focus)
        self.entry.bind("<FocusOut>", self.on_entry_unfocus)
        
        # Send button with modern styling
        send_button = tk.Button(
            input_inner,
            text="🚀 Send Command",
            font=self.fonts['button'],
            bg=self.theme['accent_blue'],
            fg=self.theme['bg_primary'],
            activebackground=self.theme['accent_green'],
            activeforeground=self.theme['bg_primary'],
            command=self.handle_send,
            relief="flat",
            pady=8,
            padx=15
        )
        send_button.pack(pady=(0, 20), padx=20, anchor="e")
        
    def create_output_section(self, parent):
        """Create modern output section"""
        output_card = tk.Frame(parent, bg=self.theme['bg_secondary'], relief="flat")
        output_card.pack(fill="both", expand=True)
        
        output_inner = tk.Frame(output_card, bg=self.theme['bg_secondary'])
        output_inner.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Output label
        output_label = tk.Label(
            output_inner,
            text="System Response:",
            font=self.fonts['body'],
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        output_label.pack(fill="x", padx=20, pady=(15, 5), anchor="w")
        
        # Scrolled text for output with modern styling
        self.output_text = scrolledtext.ScrolledText(
            output_inner,
            state='disabled',
            bg=self.theme['bg_tertiary'],
            fg=self.theme['text_primary'],
            font=self.fonts['monospace'],
            relief="flat",
            borderwidth=1,
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configure tags for styling
        self.output_text.tag_config("user", foreground=self.theme['accent_blue'], font=(self.fonts['monospace'][0], self.fonts['monospace'][1], 'bold'))
        self.output_text.tag_config("ai", foreground=self.theme['text_primary'])
        self.output_text.tag_config("info", foreground=self.theme['accent_purple'])
        self.output_text.tag_config("warning", foreground=self.theme['accent_orange'], font=(self.fonts['monospace'][0], self.fonts['monospace'][1], 'bold'))
        self.output_text.tag_config("error", foreground=self.theme['accent_red'], font=(self.fonts['monospace'][0], self.fonts['monospace'][1], 'bold'))
        self.output_text.tag_config("success", foreground=self.theme['accent_green'], font=(self.fonts['monospace'][0], self.fonts['monospace'][1], 'bold'))
        self.output_text.tag_config("muted", foreground=self.theme['text_muted'])
        self.output_text.tag_config("bold", font=(self.fonts['monospace'][0], self.fonts['monospace'][1], 'bold'))
        
    def create_status_bar(self, parent):
        """Create a status bar at the bottom."""
        status_frame = tk.Frame(parent, bg=self.theme['bg_secondary'], relief="flat")
        status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        self.status_dot = tk.Label(
            status_frame,
            text="●",
            font=('Segoe UI', 12),
            bg=self.theme['bg_secondary']
        )
        self.status_dot.pack(side="left", padx=(15, 5), pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Initializing...",
            font=self.fonts['body'],
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary'],
            anchor="w"
        )
        self.status_label.pack(side="left", pady=5)
        
    def create_footer(self, parent):
        """Create modern footer"""
        footer_frame = tk.Frame(parent, bg=self.theme['bg_secondary'], height=30)
        footer_frame.pack(fill="x", side="bottom")
        
        footer_label = tk.Label(
            footer_frame,
            text="Shadow AI © 2025 - Your Universal Assistant",
            font=self.fonts['body'],
            fg=self.theme['text_muted'],
            bg=self.theme['bg_primary']
        )
        footer_label.pack(pady=10)
        
    def on_entry_focus(self, event):
        """Handle placeholder text when entry gains focus"""
        if self.entry.get("1.0", "end-1c").strip() == self.placeholder:
            self.entry.delete("1.0", "end")
            self.entry.config(fg=self.theme['text_primary'])
            
    def on_entry_unfocus(self, event):
        """Handle placeholder text when entry loses focus"""
        if not self.entry.get("1.0", "end-1c").strip():
            self.entry.insert("1.0", self.placeholder)
            self.entry.config(fg=self.theme['text_muted'])
            
    def handle_send(self, event=None):
        """Handle sending a command"""
        command = self.entry.get("1.0", "end-1c").strip()
        
        if command and command != self.placeholder:
            self.insert_response(f"> {command}", "user")
            self.entry.delete("1.0", "end")
            
            # Start processing animation
            self.start_animation()
            
            # Process command in a separate thread
            threading.Thread(target=self.process_command_thread, args=(command,), daemon=True).start()
            
        return "break" # Prevents default newline insertion
        
    def process_command_thread(self, command):
        """Process command in a thread to avoid freezing the GUI"""
        global AI_AVAILABLE
        try:
            if not AI_AVAILABLE:
                # Fallback for when AI is not available
                response = self.get_pattern_based_response(command)
                self.response_queue.put(response)
                return

            # Use Universal Processor to understand the command
            task = process_universal_command(command)
            
            if not task:
                self.response_queue.put({
                    "type": "error",
                    "content": "I couldn't understand that command. Please try rephrasing."
                })
                return
            
            # Show task summary to user
            summary = (
                f"**Task Analysis:**\n"
                f"- **Description:** {task.description}\n"
                f"- **Complexity:** {task.complexity.value}\n"
                f"- **Risk Level:** {task.risk_level}\n"
                f"- **Steps:** {len(task.steps)}\n\n"
                f"Executing task..."
            )
            self.response_queue.put({"type": "info", "content": summary})
            
            # Execute the task using Universal Executor
            result = execute_universal_task(task)
            
            if result.success:
                response_content = f"✅ **Task completed successfully** in {result.execution_time:.1f} seconds."
                if result.warnings:
                    response_content += f" (with {len(result.warnings)} warnings)"
                
                self.response_queue.put({"type": "success", "content": response_content})
                
                if result.warnings:
                    warnings_str = "\n".join([f"- {w}" for w in result.warnings])
                    self.response_queue.put({"type": "warning", "content": f"**Warnings:**\n{warnings_str}"})
            else:
                error_message = result.error_message or "Unknown error"
                response_content = f"❌ **Task failed:** {error_message}"
                self.response_queue.put({"type": "error", "content": response_content})
                
                if result.step_results:
                    steps_summary = []
                    for step in result.step_results:
                        status = "✅" if step.get("success") else "❌"
                        action = step.get("action", "Unknown action")
                        error = f" -> Error: {step.get('error')}" if not step.get("success") else ""
                        steps_summary.append(f"{status} {action}{error}")
                    self.response_queue.put({"type": "info", "content": f"**Execution Details:**\n" + "\n".join(steps_summary)})

        except Exception as e:
            logging.error(f"Error processing command: {e}\n{traceback.format_exc()}")
            self.response_queue.put({
                "type": "error",
                "content": f"A critical error occurred: {e}"
            })
            
    def get_pattern_based_response(self, command):
        """Simple pattern-based responses for when AI is offline"""
        command_lower = command.lower()
        response = {
            "type": "ai",
            "content": "I'm currently in a limited mode. I can still try to help with basic tasks."
        }
        if "hello" in command_lower or "hi" in command_lower:
            response['content'] = "Hello! How can I assist you today?"
        elif "time" in command_lower:
            now = datetime.now().strftime("%H:%M:%S")
            response['content'] = f"The current time is {now}."
        elif "date" in command_lower:
            today = datetime.now().strftime("%Y-%m-%d")
            response['content'] = f"Today's date is {today}."
        elif "open notepad" in command_lower:
            try:
                os.system("start notepad")
                response = {"type": "success", "content": "Opening Notepad..."}
            except Exception as e:
                response = {"type": "error", "content": f"Failed to open Notepad: {e}"}
        
        return response

    def check_queue(self):
        """Check the queue for responses from the processing thread"""
        try:
            response_data = self.response_queue.get_nowait()
            self.stop_animation()
            
            if isinstance(response_data, dict):
                self.insert_response(response_data.get('content', ''), response_data.get('type', 'ai'))
            else:
                self.insert_response(str(response_data), 'ai')
                
        except queue.Empty:
            pass # No response yet
        finally:
            self.root.after(100, self.check_queue)
            
    def insert_response(self, text, tag='ai'):
        """Insert a response into the output text area with proper styling"""
        self.output_text.config(state='normal')
        
        # Simple markdown-to-tag conversion
        lines = text.split('\n')
        for line in lines:
            if line.startswith("✅") or line.startswith("❌") or line.startswith("⚠️") or line.startswith("🧠") or line.startswith(">"):
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 1: # Bold text
                        self.output_text.insert('end', part, (tag, 'bold'))
                    else:
                        self.output_text.insert('end', part, tag)
                self.output_text.insert('end', '\n')
            elif '**' in line: # Handle bolding within a line
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        self.output_text.insert('end', part, (tag, 'bold'))
                    else:
                        self.output_text.insert('end', part, tag)
                self.output_text.insert('end', '\n')
            else:
                self.output_text.insert('end', line + '\n', tag)
        
        self.output_text.insert('end', '\n', 'ai') # Add spacing
        self.output_text.config(state='disabled')
        self.output_text.see('end')
        
    def start_animation(self):
        """Start the 'processing' animation"""
        self.animation_id = None
        self.dots = ""
        self.animate()
        
    def animate(self):
        """Animate the 'processing' dots"""
        self.output_text.config(state='normal')
        
        # Find and delete the old animation text
        pos = self.output_text.search("Processing", "end-2l", "end", regexp=True)
        if pos:
            self.output_text.delete(pos, f"{pos}+{len('Processing...')}c")
            
        # Add new animation text
        self.dots = self.dots + "." if len(self.dots) < 3 else ""
        self.output_text.insert('end', f"Processing{self.dots}\n", "muted")
        self.output_text.see('end')
        self.output_text.config(state='disabled')
        
        self.animation_id = self.root.after(500, self.animate)
        
    def stop_animation(self):
        """Stop the 'processing' animation"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
            
            # Clean up the "Processing..." message from the text widget
            self.output_text.config(state='normal')
            pos = self.output_text.search("Processing", "end-2l", "end", regexp=True)
            if pos:
                self.output_text.delete(pos, f"{pos}+{len('Processing...')}c")
            self.output_text.config(state='disabled')
            
    def show_welcome_animation(self):
        """Show a welcome message with a typing effect"""
        welcome_message = "🧠 **Welcome to Shadow AI!**\nI'm your universal assistant. Tell me what you need, from writing code to managing your files or browsing the web. I'm ready to help!"
        
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        
        # Use a thread to simulate typing
        threading.Thread(target=self._type_message, args=(welcome_message, "info"), daemon=True).start()

    def _type_message(self, message, tag):
        """Internal method to simulate typing effect"""
        self.output_text.config(state='normal')
        
        # Simple markdown parsing for typing effect
        in_bold = False
        buffer = ""
        
        for char in message:
            if char == '*':
                if buffer:
                    current_tags = (tag, 'bold') if in_bold else tag
                    self.output_text.insert('end', buffer, current_tags)
                    self.output_text.see('end')
                    buffer = ""
                in_bold = not in_bold
            else:
                buffer += char
            
            time.sleep(0.01) # Typing speed
        
        if buffer:
            current_tags = (tag, 'bold') if in_bold else tag
            self.output_text.insert('end', buffer, current_tags)
        
        self.output_text.insert('end', '\n\n')
        self.output_text.config(state='disabled')
        self.output_text.see('end')

    def upload_file(self):
        """Handle file upload to knowledge base"""
        file_path = filedialog.askopenfilename(title="Select file to add to knowledge base")
        if file_path:
            kb_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base')
            os.makedirs(kb_dir, exist_ok=True)
            try:
                import shutil
                dest = os.path.join(kb_dir, os.path.basename(file_path))
                shutil.copy2(file_path, dest)
                self.insert_response(f"✅ File '{os.path.basename(file_path)}' added to knowledge base.", "success")
            except Exception as e:
                self.insert_response(f"❌ Failed to add file: {e}", "error")

    def open_settings(self):
        """Open settings dialog for LLM and theme selection"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("400x300")
        settings_win.configure(bg=self.theme['bg_secondary'])
        
        # LLM selection
        llm_label = tk.Label(settings_win, text="Select LLM Provider:", font=self.fonts['body'], bg=self.theme['bg_secondary'], fg=self.theme['text_primary'])
        llm_label.pack(pady=(20, 5), anchor="w", padx=20)
        llm_var = tk.StringVar(value="Gemini")
        llm_options = ["Gemini", "OpenAI", "Claude", "Ollama (local)"]
        llm_menu = ttk.Combobox(settings_win, textvariable=llm_var, values=llm_options, state="readonly")
        llm_menu.pack(padx=20, fill="x")
        
        # Theme selection
        theme_label = tk.Label(settings_win, text="Theme:", font=self.fonts['body'], bg=self.theme['bg_secondary'], fg=self.theme['text_primary'])
        theme_label.pack(pady=(20, 5), anchor="w", padx=20)
        theme_var = tk.StringVar(value="Dark")
        theme_options = ["Dark", "Light"]
        theme_menu = ttk.Combobox(settings_win, textvariable=theme_var, values=theme_options, state="readonly")
        theme_menu.pack(padx=20, fill="x")
        
        # Save button
        save_btn = tk.Button(settings_win, text="Save", font=self.fonts['button'], bg=self.theme['accent_green'], fg=self.theme['bg_primary'], relief="flat", command=settings_win.destroy)
        save_btn.pack(pady=30)

def main():
    """Main entry point"""
    try:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Check for API key and log a warning if not found
        if not AI_AVAILABLE:
            logging.warning("LLM client not available: Gemini API key not found or is a placeholder. Please set GEMINI_API_KEY in .env file")
            logging.warning("AI not available - using pattern-based processing")

        app = UltraModernShadowAI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start Ultra Modern Interface: {e}")
        traceback.print_exc()
        messagebox.showerror("Error", f"Failed to start Shadow AI: {e}")

if __name__ == "__main__":
    main()
