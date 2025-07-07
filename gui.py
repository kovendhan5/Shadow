# gui.py
"""
Shadow AI GUI Interface
A simple graphical interface for Shadow AI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import logging
import os
from typing import Dict, Any
from main import ShadowAI
from task_manager import task_manager
from config import VOICE_ENABLED

class ShadowGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.shadow_ai = ShadowAI()
        self.is_running = False
        self.voice_enabled = VOICE_ENABLED
        self.current_task_id = None
        self.setup_ui()
        self.setup_logging()
    
    def setup_ui(self):
        """Setup the main UI"""
        self.root.title("🧠 Shadow AI Agent")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧠 Shadow AI Agent", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Command Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Command entry
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(input_frame, textvariable=self.command_var, 
                                      font=('Arial', 12))
        self.command_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.command_entry.bind('<Return>', self.execute_command)
        
        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=1)
        
        # Execute button
        self.execute_btn = ttk.Button(buttons_frame, text="Execute", 
                                     command=self.execute_command)
        self.execute_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Voice button
        self.voice_btn = ttk.Button(buttons_frame, text="🎤 Voice", 
                                   command=self.toggle_voice, state='disabled')
        self.voice_btn.grid(row=0, column=1, padx=(0, 5))
        
        if self.voice_enabled:
            self.voice_btn.config(state='normal')
        
        # Clear button
        clear_btn = ttk.Button(buttons_frame, text="Clear", 
                              command=self.clear_command)
        clear_btn.grid(row=0, column=2)
        
        # Main content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Output tab
        self.setup_output_tab()
        
        # Tasks tab
        self.setup_tasks_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Focus on command entry
        self.command_entry.focus_set()
    
    def setup_output_tab(self):
        """Setup the output tab"""
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="Output")
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                    font=('Consolas', 10))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Add welcome message
        welcome_msg = """Welcome to Shadow AI Agent! 🧠

You can use natural language commands to control your computer. Here are some examples:

• "Open notepad" - Opens Notepad application
• "Write a leave letter for tomorrow" - Creates a leave letter document
• "Search for iPhone on Flipkart" - Opens browser and searches Flipkart
• "Take a screenshot" - Captures screen and saves to desktop
• "Create a resume template" - Generates a professional resume

Type your command above and press Enter or click Execute to get started!

"""
        self.output_text.insert(tk.END, welcome_msg)
        self.output_text.see(tk.END)
    
    def setup_tasks_tab(self):
        """Setup the tasks tab"""
        tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tasks_frame, text="Tasks")
        
        # Tasks list
        self.tasks_tree = ttk.Treeview(tasks_frame, columns=('Status', 'Description'), 
                                      show='tree headings')
        self.tasks_tree.heading('#0', text='Task')
        self.tasks_tree.heading('Status', text='Status')
        self.tasks_tree.heading('Description', text='Description')
        
        self.tasks_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Tasks scrollbar
        tasks_scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, 
                                       command=self.tasks_tree.yview)
        tasks_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tasks_tree.configure(yscrollcommand=tasks_scrollbar.set)
        
        # Tasks buttons
        tasks_btn_frame = ttk.Frame(tasks_frame)
        tasks_btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(tasks_btn_frame, text="Refresh", 
                  command=self.refresh_tasks).grid(row=0, column=0, padx=5)
        ttk.Button(tasks_btn_frame, text="Cancel Selected", 
                  command=self.cancel_selected_task).grid(row=0, column=1, padx=5)
        
        tasks_frame.grid_rowconfigure(0, weight=1)
        tasks_frame.grid_columnconfigure(0, weight=1)
    
    def setup_settings_tab(self):
        """Setup the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Voice settings
        voice_frame = ttk.LabelFrame(settings_frame, text="Voice Settings", padding="10")
        voice_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.voice_enabled_var = tk.BooleanVar(value=self.voice_enabled)
        voice_check = ttk.Checkbutton(voice_frame, text="Enable Voice Input", 
                                     variable=self.voice_enabled_var,
                                     command=self.toggle_voice_setting)
        voice_check.grid(row=0, column=0, sticky=tk.W)
        
        # Safety settings
        safety_frame = ttk.LabelFrame(settings_frame, text="Safety Settings", padding="10")
        safety_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.confirmation_var = tk.BooleanVar(value=True)
        confirm_check = ttk.Checkbutton(safety_frame, text="Require Confirmation for Sensitive Actions", 
                                       variable=self.confirmation_var)
        confirm_check.grid(row=0, column=0, sticky=tk.W)
        
        # Logging settings
        logging_frame = ttk.LabelFrame(settings_frame, text="Logging", padding="10")
        logging_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Button(logging_frame, text="View Logs", 
                  command=self.view_logs).grid(row=0, column=0, padx=5)
        ttk.Button(logging_frame, text="Clear Logs", 
                  command=self.clear_logs).grid(row=0, column=1, padx=5)
        
        settings_frame.grid_columnconfigure(0, weight=1)
    
    def setup_logging(self):
        """Setup logging to capture output"""
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.see(tk.END)
        
        # Add GUI handler to root logger
        gui_handler = GUILogHandler(self.output_text)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(gui_handler)
    
    def execute_command(self, event=None):
        """Execute the command"""
        command = self.command_var.get().strip()
        if not command:
            return
        
        self.update_status("Processing command...")
        self.execute_btn.config(state='disabled')
        
        # Clear command entry
        self.command_var.set("")
        
        # Add command to output
        self.output_text.insert(tk.END, f"\n🤖 Command: {command}\n")
        self.output_text.see(tk.END)
        
        # Execute in background thread
        thread = threading.Thread(target=self._execute_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _execute_command_thread(self, command):
        """Execute command in background thread"""
        try:
            success = self.shadow_ai.run_single_command(command)
            
            # Update UI in main thread
            self.root.after(0, self._command_completed, success)
        except Exception as e:
            logging.error(f"Error executing command: {e}")
            self.root.after(0, self._command_completed, False)
    
    def _command_completed(self, success):
        """Called when command execution completes"""
        if success:
            self.update_status("Command completed successfully")
        else:
            self.update_status("Command failed")
        
        self.execute_btn.config(state='normal')
        self.refresh_tasks()
    
    def toggle_voice(self):
        """Toggle voice input"""
        if not self.voice_enabled:
            messagebox.showwarning("Voice Disabled", "Voice input is disabled in settings.")
            return
        
        # This would trigger voice input
        self.update_status("Listening...")
        self.voice_btn.config(state='disabled')
        
        # Simulate voice input (in real implementation, this would use voice recognition)
        def voice_thread():
            try:
                # Placeholder for voice recognition
                time.sleep(2)
                self.root.after(0, self._voice_completed, "voice command placeholder")
            except Exception as e:
                logging.error(f"Voice error: {e}")
                self.root.after(0, self._voice_completed, None)
        
        thread = threading.Thread(target=voice_thread)
        thread.daemon = True
        thread.start()
    
    def _voice_completed(self, command):
        """Called when voice input completes"""
        self.voice_btn.config(state='normal')
        if command:
            self.command_var.set(command)
            self.update_status("Voice command received")
        else:
            self.update_status("Voice input failed")
    
    def clear_command(self):
        """Clear the command entry"""
        self.command_var.set("")
        self.command_entry.focus_set()
    
    def toggle_voice_setting(self):
        """Toggle voice setting"""
        self.voice_enabled = self.voice_enabled_var.get()
        if self.voice_enabled:
            self.voice_btn.config(state='normal')
        else:
            self.voice_btn.config(state='disabled')
    
    def refresh_tasks(self):
        """Refresh the tasks list"""
        # Clear existing items
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        # Add tasks
        tasks = task_manager.list_tasks()
        for task in tasks:
            self.tasks_tree.insert('', tk.END, text=task['name'], 
                                  values=(task['status'], task['description']))
    
    def cancel_selected_task(self):
        """Cancel the selected task"""
        selection = self.tasks_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task to cancel.")
            return
        
        # Get task info (simplified for demo)
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this task?"):
            messagebox.showinfo("Task Cancelled", "Task has been cancelled.")
            self.refresh_tasks()
    
    def view_logs(self):
        """View log file"""
        try:
            log_file = "logs/shadow.log"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    content = f.read()
                
                # Create log viewer window
                log_window = tk.Toplevel(self.root)
                log_window.title("Shadow AI Logs")
                log_window.geometry("800x600")
                
                log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, 
                                                   font=('Consolas', 9))
                log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                log_text.insert(tk.END, content)
                log_text.see(tk.END)
            else:
                messagebox.showinfo("No Logs", "No log file found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open logs: {e}")
    
    def clear_logs(self):
        """Clear log file"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all logs?"):
            try:
                log_file = "logs/shadow.log"
                if os.path.exists(log_file):
                    with open(log_file, 'w') as f:
                        f.write("")
                    messagebox.showinfo("Logs Cleared", "All logs have been cleared.")
                else:
                    messagebox.showinfo("No Logs", "No log file found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear logs: {e}")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
    
    def run(self):
        """Run the GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Shadow AI?"):
            self.shadow_ai.cleanup()
            self.root.destroy()

def main():
    """Main function for GUI"""
    gui = ShadowGUI()
    gui.run()

if __name__ == "__main__":
    main()
