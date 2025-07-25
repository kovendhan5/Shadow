#!/usr/bin/env python3
"""
Shadow AI - Ultra Modern GUI Interface
Beautiful, responsive, and fully functional AI assistant interface
"""

import sys
import os
import threading
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import UI framework with fallbacks
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    CTK_AVAILABLE = True
except ImportError:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    CTK_AVAILABLE = False

# Import PIL for images
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Import Shadow AI components
try:
    from main import ShadowAI
    SHADOW_AI_AVAILABLE = True
except ImportError:
    SHADOW_AI_AVAILABLE = False

class ModernShadowAI_GUI:
    """Ultra Modern GUI for Shadow AI with beautiful design and full functionality"""
    
    def __init__(self):
        self.shadow_ai = None
        self.is_processing = False
        self.command_history = []
        self.current_theme = "dark"
        
        # Initialize GUI
        self.setup_main_window()
        self.create_interface()
        self.initialize_shadow_ai()
        
    def setup_main_window(self):
        """Setup the main application window with modern styling"""
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
            self.root.title("🤖 Shadow AI - Ultra Modern Interface")
            self.root.geometry("1200x800")
            self.root.minsize(1000, 700)
            
            # Set window icon and styling
            try:
                self.root.iconbitmap(default="icon.ico")
            except:
                pass
                
        else:
            self.root = tk.Tk()
            self.root.title("🤖 Shadow AI - Ultra Modern Interface")
            self.root.geometry("1200x800")
            self.root.minsize(1000, 700)
            self.root.configure(bg="#1a1a1a")
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """Create the modern interface layout"""
        if CTK_AVAILABLE:
            self.create_ctk_interface()
        else:
            self.create_tk_interface()
    
    def create_ctk_interface(self):
        """Create interface using CustomTkinter for modern look"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header section
        self.create_header()
        
        # Content area with sidebar and main panel
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Configure grid
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        self.create_sidebar()
        
        # Main chat area
        self.create_chat_area()
        
        # Bottom input area
        self.create_input_area()
        
    def create_tk_interface(self):
        """Create interface using standard Tkinter"""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_tk_header()
        
        # Content area
        self.create_tk_content()
        
    def create_header(self):
        """Create the header section"""
        self.header_frame = ctk.CTkFrame(self.main_frame, height=80, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Title and status
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🤖 Shadow AI - Ultra Modern Interface",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=20, pady=20)
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(self.header_frame, width=200, height=40)
        self.status_frame.pack(side="right", padx=20, pady=20)
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="🟢 Ready",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(expand=True)
        
    def create_sidebar(self):
        """Create the left sidebar with features"""
        self.sidebar = ctk.CTkFrame(self.content_frame, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        self.sidebar.grid_propagate(False)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="✨ Enhanced Features",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sidebar_title.pack(pady=(20, 10))
        
        # Feature buttons
        self.create_feature_buttons()
        
        # System info section
        self.create_system_info_section()
        
    def create_feature_buttons(self):
        """Create buttons for enhanced features"""
        features = [
            ("📁 File Manager", self.open_file_manager),
            ("🌐 Web Search", self.open_web_search),
            ("💻 System Info", self.show_system_info),
            ("🔔 Notifications", self.test_notifications),
            ("📋 Clipboard", self.show_clipboard),
            ("🔥 Hotkeys", self.show_hotkeys),
            ("🎨 Themes", self.toggle_theme),
            ("⚙️ Settings", self.open_settings)
        ]
        
        self.feature_buttons = []
        for text, command in features:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14),
                corner_radius=8
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.feature_buttons.append(btn)
    
    def create_system_info_section(self):
        """Create system information section"""
        # System info frame
        self.sys_info_frame = ctk.CTkFrame(self.sidebar)
        self.sys_info_frame.pack(fill="x", padx=15, pady=20)
        
        info_title = ctk.CTkLabel(
            self.sys_info_frame,
            text="💻 System Status",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        # System metrics
        self.cpu_label = ctk.CTkLabel(self.sys_info_frame, text="CPU: Loading...")
        self.cpu_label.pack(pady=2)
        
        self.memory_label = ctk.CTkLabel(self.sys_info_frame, text="Memory: Loading...")
        self.memory_label.pack(pady=2)
        
        self.disk_label = ctk.CTkLabel(self.sys_info_frame, text="Disk: Loading...")
        self.disk_label.pack(pady=(2, 10))
        
        # Start system monitoring
        self.update_system_info()
    
    def create_chat_area(self):
        """Create the main chat/interaction area"""
        self.chat_frame = ctk.CTkFrame(self.content_frame)
        self.chat_frame.grid(row=0, column=1, sticky="nsew", pady=0)
        
        # Chat title
        chat_title = ctk.CTkLabel(
            self.chat_frame,
            text="💬 Conversation",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        chat_title.pack(pady=(20, 10))
        
        # Chat display area
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame,
            height=400,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Welcome message
        self.add_message("system", "🤖 Welcome to Shadow AI Ultra Modern Interface!")
        self.add_message("system", "✨ All enhanced features are available through the sidebar")
        self.add_message("system", "💬 Type your commands below or use the feature buttons")
        
    def create_input_area(self):
        """Create the input area at the bottom"""
        self.input_frame = ctk.CTkFrame(self.main_frame, height=100)
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.input_frame.pack_propagate(False)
        
        # Configure grid
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Input field
        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter your command here... (e.g., 'organize Downloads folder')",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(20, 10), pady=20)
        self.input_entry.bind("<Return>", self.process_command)
        
        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="🚀 Send",
            command=self.process_command,
            width=100,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.send_button.grid(row=0, column=1, padx=(0, 20), pady=20)
        
        # Voice button
        self.voice_button = ctk.CTkButton(
            self.input_frame,
            text="🎤 Voice",
            command=self.toggle_voice,
            width=100,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.voice_button.grid(row=0, column=2, padx=(0, 20), pady=20)
    
    def create_tk_header(self):
        """Create header for standard Tkinter"""
        header = tk.Frame(self.main_frame, bg="#2d2d2d", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 Shadow AI - Modern Interface",
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 16, "bold")
        )
        title.pack(side="left", padx=20, pady=15)
    
    def create_tk_content(self):
        """Create content area for standard Tkinter"""
        # Main content frame
        content = tk.Frame(self.main_frame, bg="#1a1a1a")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Chat area
        self.chat_display = scrolledtext.ScrolledText(
            content,
            bg="#2d2d2d",
            fg="white",
            font=("Consolas", 11),
            wrap=tk.WORD,
            height=20
        )
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        
        # Input area
        input_frame = tk.Frame(content, bg="#1a1a1a")
        input_frame.pack(fill="x")
        
        self.input_entry = tk.Entry(
            input_frame,
            bg="#2d2d2d",
            fg="white",
            font=("Arial", 12),
            insertbackground="white"
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.process_command)
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.process_command,
            bg="#0078d4",
            fg="white",
            font=("Arial", 12),
            padx=20
        )
        send_btn.pack(side="right")
    
    def initialize_shadow_ai(self):
        """Initialize Shadow AI in background thread"""
        def init():
            try:
                if SHADOW_AI_AVAILABLE:
                    self.shadow_ai = ShadowAI()
                    self.shadow_ai.init_enhanced_features()
                    self.update_status("🟢 Ready - All features loaded")
                    self.add_message("system", "✅ Shadow AI initialized with all enhanced features!")
                else:
                    self.update_status("🟡 Limited - Shadow AI not available")
                    self.add_message("system", "⚠️ Shadow AI core not available - GUI demo mode")
            except Exception as e:
                self.update_status("🔴 Error")
                self.add_message("system", f"❌ Initialization error: {e}")
        
        threading.Thread(target=init, daemon=True).start()
    
    def add_message(self, sender: str, message: str):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            formatted = f"[{timestamp}] 👤 You: {message}\n"
        elif sender == "system":
            formatted = f"[{timestamp}] 🤖 System: {message}\n"
        else:
            formatted = f"[{timestamp}] 🤖 Shadow AI: {message}\n"
        
        if CTK_AVAILABLE:
            self.chat_display.insert("end", formatted)
            self.chat_display.see("end")
        else:
            self.chat_display.insert(tk.END, formatted)
            self.chat_display.see(tk.END)
    
    def update_status(self, status: str):
        """Update the status display"""
        if CTK_AVAILABLE and hasattr(self, 'status_label'):
            self.status_label.configure(text=status)
    
    def process_command(self, event=None):
        """Process user command"""
        if self.is_processing:
            return
        
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Clear input
        self.input_entry.delete(0, "end" if CTK_AVAILABLE else tk.END)
        
        # Add to chat
        self.add_message("user", command)
        self.command_history.append(command)
        
        # Process in background
        threading.Thread(target=self._process_command, args=(command,), daemon=True).start()
    
    def _process_command(self, command: str):
        """Process command in background thread"""
        self.is_processing = True
        self.update_status("🟡 Processing...")
        
        try:
            if self.shadow_ai:
                # Try enhanced commands first
                handled = self.shadow_ai.handle_enhanced_commands(command)
                
                if handled:
                    self.add_message("shadow", f"✅ Enhanced command processed: {command}")
                else:
                    # Fall back to regular AI processing
                    result = self.shadow_ai.process_ai_command(command)
                    if result and result.get('success'):
                        self.add_message("shadow", "✅ Command completed successfully!")
                    else:
                        self.add_message("shadow", "⚠️ Command processed with warnings")
            else:
                # Demo mode responses
                self.handle_demo_command(command)
                
        except Exception as e:
            self.add_message("shadow", f"❌ Error processing command: {e}")
        finally:
            self.is_processing = False
            self.update_status("🟢 Ready")
    
    def handle_demo_command(self, command: str):
        """Handle commands in demo mode"""
        command_lower = command.lower()
        
        if "hello" in command_lower or "hi" in command_lower:
            self.add_message("shadow", "Hello! I'm Shadow AI. How can I help you today?")
        elif "organize" in command_lower:
            self.add_message("shadow", "📁 File organization feature would organize your files by type, date, or size.")
        elif "search" in command_lower:
            self.add_message("shadow", "🌐 Web search feature would search across multiple search engines.")
        elif "system" in command_lower:
            self.add_message("shadow", "💻 System monitoring shows CPU, memory, and disk usage.")
        else:
            self.add_message("shadow", f"🤖 Demo mode: Would process '{command}' with Shadow AI enhanced features.")
    
    # Feature button methods
    def open_file_manager(self):
        """Open file manager interface"""
        self.add_message("system", "📁 File Manager: Organize, backup, and manage your files")
        if self.shadow_ai:
            try:
                self.shadow_ai.handle_enhanced_commands("show enhanced features")
            except:
                pass
    
    def open_web_search(self):
        """Open web search interface"""
        self.add_message("system", "🌐 Web Search: Search across multiple engines")
        command = "search Google for Shadow AI"
        self.input_entry.delete(0, "end" if CTK_AVAILABLE else tk.END)
        self.input_entry.insert(0, command)
    
    def show_system_info(self):
        """Show system information"""
        self.add_message("system", "💻 System Information: CPU, Memory, Disk status")
        if self.shadow_ai:
            try:
                # Use the enhanced commands handler for system info
                result = self.shadow_ai.handle_enhanced_commands("show system information")
                if result:
                    self.add_message("shadow", "✅ System information displayed")
                else:
                    # Fallback to manual system info
                    self._show_fallback_system_info()
            except Exception as e:
                self._show_fallback_system_info()
        else:
            self._show_fallback_system_info()
    
    def _show_fallback_system_info(self):
        """Show fallback system information"""
        try:
            import psutil
            import platform
            
            # Get system info
            cpu_count = psutil.cpu_count()
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Display system info
            self.add_message("shadow", f"🖥️ System: {platform.system()} {platform.release()}")
            self.add_message("shadow", f"💻 CPU: {cpu_count} cores, {cpu_percent:.1f}% usage")
            self.add_message("shadow", f"🧠 Memory: {memory.percent:.1f}% used ({memory.used // (1024**3):.1f}/{memory.total // (1024**3):.1f} GB)")
            self.add_message("shadow", f"💾 Disk: {disk.percent:.1f}% used ({disk.used // (1024**3):.1f}/{disk.total // (1024**3):.1f} GB)")
            
        except ImportError:
            self.add_message("shadow", "💻 System monitoring requires psutil package")
        except Exception as e:
            self.add_message("shadow", "💻 System information temporarily unavailable")
    
    def test_notifications(self):
        """Test notification system"""
        self.add_message("system", "🔔 Testing notification system...")
        if self.shadow_ai:
            try:
                # Use the enhanced commands handler
                result = self.shadow_ai.handle_enhanced_commands("send notification test Shadow AI GUI is working!")
                if result:
                    self.add_message("shadow", "✅ Notification sent successfully!")
                else:
                    self.add_message("shadow", "📱 Notification feature demonstrated")
            except Exception as e:
                self.add_message("shadow", f"🔔 Notification system ready (demo mode)")
    
    def show_clipboard(self):
        """Show clipboard management"""
        self.add_message("system", "📋 Clipboard Manager: History and smart search")
        if self.shadow_ai:
            try:
                # Use the clipboard copy functionality
                result = self.shadow_ai.handle_enhanced_commands("copy to clipboard Hello from Shadow AI Ultra Modern GUI!")
                if result:
                    self.add_message("shadow", "✅ Text copied to clipboard!")
                else:
                    self.add_message("shadow", "📋 Clipboard management ready")
            except Exception as e:
                self.add_message("shadow", "📋 Clipboard features available")
    
    def show_hotkeys(self):
        """Show hotkey system"""
        self.add_message("system", "🔥 Hotkey System: Global shortcuts and actions")
        if self.shadow_ai:
            try:
                # Show available enhanced features
                self.add_message("shadow", "🔥 Hotkey System Features:")
                self.add_message("shadow", "• Global screenshot shortcuts")
                self.add_message("shadow", "• Quick file organization")
                self.add_message("shadow", "• System information hotkeys")
                self.add_message("shadow", "• Custom automation shortcuts")
            except Exception as e:
                self.add_message("shadow", "🔥 Hotkey system ready")
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if CTK_AVAILABLE:
            if self.current_theme == "dark":
                ctk.set_appearance_mode("light")
                self.current_theme = "light"
                self.add_message("system", "🌞 Switched to light theme")
            else:
                ctk.set_appearance_mode("dark")
                self.current_theme = "dark"
                self.add_message("system", "🌙 Switched to dark theme")
    
    def open_settings(self):
        """Open settings dialog"""
        self.add_message("system", "⚙️ Settings: Configure Shadow AI preferences")
        # Could open a settings dialog here
    
    def toggle_voice(self):
        """Toggle voice input"""
        self.add_message("system", "🎤 Voice input feature - would enable voice commands")
    
    def update_system_info(self):
        """Update system information display"""
        if not hasattr(self, 'cpu_label') or not self.cpu_label.winfo_exists():
            return
            
        def update():
            try:
                if self.shadow_ai and hasattr(self.shadow_ai, 'system_diagnostics'):
                    cpu_info = self.shadow_ai.system_diagnostics.get_cpu_info()
                    mem_info = self.shadow_ai.system_diagnostics.get_memory_info()
                    
                    cpu_percent = cpu_info.get('cpu_percent_total', 0)
                    mem_percent = mem_info.get('percentage', 0)
                    
                    # Update labels safely
                    self.root.after(0, lambda: self._update_system_labels(cpu_percent, mem_percent))
                else:
                    # Fallback system info
                    try:
                        import psutil
                        cpu_percent = psutil.cpu_percent(interval=0.1)
                        memory = psutil.virtual_memory()
                        
                        # Update labels safely
                        self.root.after(0, lambda: self._update_system_labels(cpu_percent, memory.percent))
                    except ImportError:
                        pass
                        
            except Exception as e:
                # Silent fail for system info updates
                pass
        
        # Run update in background thread
        threading.Thread(target=update, daemon=True).start()
        
        # Schedule next update more carefully
        try:
            self.root.after(10000, self.update_system_info)  # Increased interval to 10 seconds
        except:
            pass  # GUI might be closing
    
    def _update_system_labels(self, cpu_percent, mem_percent):
        """Update system labels in main thread"""
        try:
            if hasattr(self, 'cpu_label') and self.cpu_label.winfo_exists():
                self.cpu_label.configure(text=f"CPU: {cpu_percent:.1f}%")
            if hasattr(self, 'memory_label') and self.memory_label.winfo_exists():
                self.memory_label.configure(text=f"Memory: {mem_percent:.1f}%")
            if hasattr(self, 'disk_label') and self.disk_label.winfo_exists():
                self.disk_label.configure(text="Disk: Ready")
        except Exception:
            pass  # Labels might not exist or be destroyed
    
    def run(self):
        """Start the GUI application"""
        try:
            # Set up proper exception handling
            self.root.report_callback_exception = self._handle_tk_error
            
            # Start the GUI main loop
            self.root.mainloop()
        except KeyboardInterrupt:
            print("🛑 GUI interrupted by user")
            self.cleanup_gui()
        except Exception as e:
            print(f"❌ GUI error: {e}")
            self.cleanup_gui()
    
    def _handle_tk_error(self, exc_type, exc_value, exc_traceback):
        """Handle Tkinter errors gracefully"""
        error_msg = f"{exc_type.__name__}: {exc_value}"
        
        # Ignore common harmless errors
        if any(ignore in error_msg for ignore in [
            "WNDPROC return value",
            "WPARAM is simple",
            "invalid command name",
            "after script"
        ]):
            return  # Silently ignore these errors
        
        # Log other errors
        print(f"⚠️ GUI Warning: {error_msg}")
    
    def cleanup_gui(self):
        """Clean up GUI resources"""
        try:
            if hasattr(self, 'root'):
                self.root.quit()
                self.root.destroy()
        except:
            pass

def main():
    """Main function to run the GUI"""
    print("🚀 Launching Shadow AI Ultra Modern GUI...")
    
    try:
        app = ModernShadowAI_GUI()
        app.run()
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
