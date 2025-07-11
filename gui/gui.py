#!/usr/bin/env python3
"""
Shadow AI - Basic GUI
Simple tkinter interface
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Basic GUI launcher"""
    root = tk.Tk()
    root.title("Shadow AI - Basic Interface")
    root.geometry("400x200")
    
    tk.Label(
        root,
        text="🧠 Shadow AI",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    tk.Label(
        root,
        text="This is a basic GUI placeholder.\nPlease use the GUI launcher for\nmore advanced interfaces.",
        font=("Arial", 10),
        justify="center"
    ).pack(pady=10)
    
    def open_launcher():
        try:
            from launchers.launch_gui_new import main as launcher_main
            root.destroy()
            launcher_main()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open GUI launcher: {e}")
    
    tk.Button(
        root,
        text="Open GUI Launcher",
        command=open_launcher,
        bg="#007acc",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
