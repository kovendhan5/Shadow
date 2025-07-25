#!/usr/bin/env python3
"""
Shadow AI GUI Launcher
Simple launcher for all available GUI interfaces
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class GUILauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Shadow AI - GUI Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg='#2b2b2b')
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the launcher UI"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🤖 Shadow AI - GUI Launcher",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Choose your preferred interface",
            font=("Arial", 12),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # GUI Options Frame
        options_frame = tk.Frame(self.root, bg='#2b2b2b')
        options_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Available GUIs
        self.gui_options = [
            {
                'name': '🎨 Modern GUI',
                'description': 'Clean, professional interface with modern design',
                'file': 'gui/modern_gui.py',
                'color': '#4CAF50'
            },
            {
                'name': '🚀 Enhanced Modern GUI', 
                'description': 'Advanced modern interface with enhanced features',
                'file': 'gui/enhanced_modern_gui.py',
                'color': '#2196F3'
            },
            {
                'name': '🎯 Basic GUI',
                'description': 'Simple, lightweight interface for basic operations',
                'file': 'gui/gui.py',
                'color': '#FF9800'
            },
            {
                'name': '🎭 Cyberpunk GUI (Launcher)',
                'description': 'Futuristic neon-themed interface',
                'launcher': 'launchers/launch_cyberpunk.bat',
                'color': '#9C27B0'
            },
            {
                'name': '💎 Premium GUI (Launcher)',
                'description': 'Premium interface with advanced features',
                'launcher': 'launchers/launch_premium.bat',
                'color': '#FF5722'
            },
            {
                'name': '🦾 Ultra Modern GUI (Launcher)',
                'description': 'Ultra-modern interface with all features',
                'launcher': 'launchers/launch_ultra_modern.bat',
                'color': '#607D8B'
            }
        ]
        
        # Create buttons for each GUI
        for i, gui in enumerate(self.gui_options):
            self.create_gui_button(options_frame, gui, i)
        
        # Command Line Option
        cli_frame = tk.Frame(self.root, bg='#2b2b2b')
        cli_frame.pack(pady=10, padx=20, fill='x')
        
        cli_button = tk.Button(
            cli_frame,
            text="💻 Command Line Interface",
            font=("Arial", 12, "bold"),
            bg='#333333',
            fg='#ffffff',
            activebackground='#555555',
            activeforeground='#ffffff',
            relief='flat',
            padx=20,
            pady=10,
            command=self.launch_cli
        )
        cli_button.pack(fill='x')
        
        # Info Label
        info_label = tk.Label(
            self.root,
            text="💡 Tip: Each GUI offers different features and styling options",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#888888'
        )
        info_label.pack(pady=10)
    
    def create_gui_button(self, parent, gui_info, index):
        """Create a button for each GUI option"""
        # Button frame
        btn_frame = tk.Frame(parent, bg='#2b2b2b')
        btn_frame.pack(fill='x', pady=5)
        
        # Main button
        button = tk.Button(
            btn_frame,
            text=gui_info['name'],
            font=("Arial", 12, "bold"),
            bg=gui_info['color'],
            fg='#ffffff',
            activebackground=self.lighten_color(gui_info['color']),
            activeforeground='#ffffff',
            relief='flat',
            padx=20,
            pady=8,
            command=lambda: self.launch_gui(gui_info)
        )
        button.pack(side='left', fill='x', expand=True)
        
        # Description label
        desc_label = tk.Label(
            btn_frame,
            text=gui_info['description'],
            font=("Arial", 9),
            bg='#2b2b2b',
            fg='#aaaaaa',
            anchor='w'
        )
        desc_label.pack(side='left', padx=(10, 0))
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effect"""
        # Simple color lightening
        color_map = {
            '#4CAF50': '#66BB6A',
            '#2196F3': '#42A5F5', 
            '#FF9800': '#FFB74D',
            '#9C27B0': '#BA68C8',
            '#FF5722': '#FF7043',
            '#607D8B': '#78909C'
        }
        return color_map.get(color, color)
    
    def launch_gui(self, gui_info):
        """Launch the selected GUI"""
        try:
            if 'file' in gui_info:
                # Python file
                file_path = gui_info['file']
                if os.path.exists(file_path):
                    subprocess.Popen([sys.executable, file_path])
                    messagebox.showinfo("🚀 Launching", f"Starting {gui_info['name']}...")
                else:
                    messagebox.showerror("❌ Error", f"GUI file not found: {file_path}")
            elif 'launcher' in gui_info:
                # Batch launcher
                launcher_path = gui_info['launcher']
                if os.path.exists(launcher_path):
                    subprocess.Popen(launcher_path, shell=True)
                    messagebox.showinfo("🚀 Launching", f"Starting {gui_info['name']}...")
                else:
                    messagebox.showerror("❌ Error", f"Launcher not found: {launcher_path}")
        
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to launch {gui_info['name']}: {str(e)}")
    
    def launch_cli(self):
        """Launch command line interface"""
        try:
            subprocess.Popen([sys.executable, 'launch_working.py'])
            messagebox.showinfo("🚀 Launching", "Starting Command Line Interface...")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to launch CLI: {str(e)}")
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🚀 Starting Shadow AI GUI Launcher...")
    launcher = GUILauncher()
    launcher.run()

if __name__ == "__main__":
    main()
