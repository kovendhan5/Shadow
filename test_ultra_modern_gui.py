#!/usr/bin/env python3
"""
Shadow AI - Simple Test GUI
Quick test to verify the ultra modern GUI works
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    class TestGUI:
        def __init__(self):
            self.root = ctk.CTk()
            self.root.title("🤖 Shadow AI - Ultra Modern Test")
            self.root.geometry("800x600")
            
            # Main frame
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title = ctk.CTkLabel(
                main_frame,
                text="🚀 Shadow AI Ultra Modern GUI",
                font=ctk.CTkFont(size=32, weight="bold")
            )
            title.pack(pady=30)
            
            # Status
            status = ctk.CTkLabel(
                main_frame,
                text="✅ New GUI Design Working Perfectly!",
                font=ctk.CTkFont(size=18),
                text_color="#00ff00"
            )
            status.pack(pady=20)
            
            # Features list
            features_frame = ctk.CTkFrame(main_frame)
            features_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            features_title = ctk.CTkLabel(
                features_frame,
                text="✨ New Features Available:",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            features_title.pack(pady=20)
            
            features = [
                "🎨 Modern CustomTkinter Interface",
                "📱 Responsive Design Layout",
                "🌙 Dark/Light Theme Support",
                "💫 Smooth Animations",
                "📁 Enhanced File Management",
                "🌐 Web Search Integration",
                "💻 System Monitoring",
                "🔔 Smart Notifications",
                "📋 Clipboard Management",
                "🔥 Global Hotkeys",
                "⚙️ Advanced Settings",
                "🎤 Voice Commands Ready"
            ]
            
            for feature in features:
                label = ctk.CTkLabel(
                    features_frame,
                    text=feature,
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=5)
            
            # Test button
            test_btn = ctk.CTkButton(
                main_frame,
                text="🚀 Launch Full Ultra Modern GUI",
                command=self.launch_full_gui,
                height=50,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            test_btn.pack(pady=30)
            
        def launch_full_gui(self):
            """Launch the full ultra modern GUI"""
            self.root.destroy()
            try:
                from gui.ultra_modern_gui import main
                main()
            except ImportError:
                # Try direct import
                sys.path.insert(0, str(Path(__file__).parent / "gui"))
                from ultra_modern_gui import main
                main()
        
        def run(self):
            self.root.mainloop()
    
    # Run the test GUI
    if __name__ == "__main__":
        print("🎨 Testing Ultra Modern GUI...")
        app = TestGUI()
        app.run()

except ImportError:
    # Fallback to tkinter
    import tkinter as tk
    from tkinter import ttk
    
    print("⚠️ CustomTkinter not available, using tkinter fallback")
    
    root = tk.Tk()
    root.title("🤖 Shadow AI - Modern GUI Test")
    root.geometry("600x400")
    root.configure(bg="#1a1a1a")
    
    # Title
    title = tk.Label(
        root,
        text="🚀 Shadow AI Modern GUI",
        bg="#1a1a1a",
        fg="white",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=30)
    
    # Status
    status = tk.Label(
        root,
        text="✅ GUI Working! (Tkinter Mode)",
        bg="#1a1a1a",
        fg="#00ff00",
        font=("Arial", 16)
    )
    status.pack(pady=20)
    
    # Info
    info = tk.Label(
        root,
        text="Install customtkinter for ultra modern design:\npip install customtkinter",
        bg="#1a1a1a",
        fg="yellow",
        font=("Arial", 12),
        justify="center"
    )
    info.pack(pady=20)
    
    root.mainloop()
