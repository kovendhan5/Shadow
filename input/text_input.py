# text_input.py
import logging
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Optional

class TextInput:
    def __init__(self):
        self.root = None
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI for text input"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window initially
        self.root.title("Shadow AI Agent")
        
        # Configure window properties
        self.root.geometry("400x300")
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_command_cli(self, prompt: str = "Enter your command") -> str:
        """Get command input from command line"""
        try:
            command = input(f"🤖 {prompt}: ")
            return command.strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            return None
    
    def get_command_gui(self, prompt: str = "Enter your command") -> str:
        """Get command input from GUI dialog"""
        try:
            command = simpledialog.askstring(
                "Shadow AI Agent", 
                prompt,
                parent=self.root
            )
            return command.strip() if command else None
        except Exception as e:
            logging.error(f"Error in GUI input: {e}")
            return None
    
    def show_message(self, title: str, message: str, msg_type: str = "info"):
        """Show a message to the user"""
        try:
            if msg_type == "info":
                messagebox.showinfo(title, message, parent=self.root)
            elif msg_type == "warning":
                messagebox.showwarning(title, message, parent=self.root)
            elif msg_type == "error":
                messagebox.showerror(title, message, parent=self.root)
        except Exception as e:
            logging.error(f"Error showing message: {e}")
            print(f"{title}: {message}")
    
    def confirm_action(self, question: str) -> bool:
        """Ask for confirmation via GUI"""
        try:
            result = messagebox.askyesno(
                "Shadow AI - Confirmation", 
                question,
                parent=self.root
            )
            return result
        except Exception as e:
            logging.error(f"Error in confirmation dialog: {e}")
            # Fallback to CLI confirmation
            response = input(f"{question} (y/n): ").strip().lower()
            return response in ['y', 'yes', 'true', '1']
    
    def get_multi_line_input(self, prompt: str = "Enter your text") -> str:
        """Get multi-line text input"""
        class MultiLineDialog:
            def __init__(self, parent, prompt):
                self.result = None
                self.top = tk.Toplevel(parent)
                self.top.title("Shadow AI Agent")
                self.top.geometry("500x400")
                self.top.resizable(True, True)
                
                # Center the dialog
                self.top.update_idletasks()
                width = self.top.winfo_width()
                height = self.top.winfo_height()
                x = (self.top.winfo_screenwidth() // 2) - (width // 2)
                y = (self.top.winfo_screenheight() // 2) - (height // 2)
                self.top.geometry(f'{width}x{height}+{x}+{y}')
                
                # Create widgets
                tk.Label(self.top, text=prompt, font=("Arial", 12)).pack(pady=10)
                
                self.text_widget = tk.Text(self.top, wrap=tk.WORD, font=("Arial", 10))
                self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Buttons
                button_frame = tk.Frame(self.top)
                button_frame.pack(pady=10)
                
                tk.Button(button_frame, text="OK", command=self.ok_clicked, 
                         bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Cancel", command=self.cancel_clicked,
                         bg="#f44336", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
                
                # Focus on text widget
                self.text_widget.focus_set()
                
                # Make dialog modal
                self.top.transient(parent)
                self.top.grab_set()
                self.top.wait_window()
            
            def ok_clicked(self):
                self.result = self.text_widget.get("1.0", tk.END).strip()
                self.top.destroy()
            
            def cancel_clicked(self):
                self.result = None
                self.top.destroy()
        
        try:
            dialog = MultiLineDialog(self.root, prompt)
            return dialog.result
        except Exception as e:
            logging.error(f"Error in multi-line input: {e}")
            return None
    
    def cleanup(self):
        """Clean up GUI resources"""
        if self.root:
            self.root.quit()
            self.root.destroy()

# Create a global text input instance
text_input = TextInput()

def get_text_input(prompt: str = "Enter your command", use_gui: bool = False) -> str:
    """Get text input from user"""
    if use_gui:
        return text_input.get_command_gui(prompt)
    else:
        return text_input.get_command_cli(prompt)

def get_multiline_input(prompt: str = "Enter your text") -> str:
    """Get multi-line text input"""
    return text_input.get_multi_line_input(prompt)

def show_message(title: str, message: str, msg_type: str = "info"):
    """Show a message to the user"""
    text_input.show_message(title, message, msg_type)

def confirm_action(question: str, use_gui: bool = False) -> bool:
    """Ask for confirmation"""
    if use_gui:
        return text_input.confirm_action(question)
    else:
        response = input(f"{question} (y/n): ").strip().lower()
        return response in ['y', 'yes', 'true', '1']
