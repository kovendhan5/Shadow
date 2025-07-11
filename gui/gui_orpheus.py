#!/usr/bin/env python3
"""
Shadow AI - Orpheus GUI
Emotional AI interface with empathy features (Placeholder)
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Orpheus GUI placeholder - redirects to Premium GUI"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    response = messagebox.askyesno(
        "Orpheus Emotional AI", 
        "Orpheus Emotional AI GUI is currently under development.\nWould you like to launch the Premium GUI instead?"
    )
    
    if response:
        try:
            from gui.gui_premium import main as premium_main
            root.destroy()
            premium_main()
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch Premium GUI: {e}")
    else:
        root.destroy()

if __name__ == "__main__":
    main()
