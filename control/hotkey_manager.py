#!/usr/bin/env python3
"""
Hotkey Management System for Shadow AI
Provides customizable keyboard shortcuts for quick actions
"""

import logging
import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Callable, Optional, Any

class HotkeyManager:
    """Customizable hotkey system for Shadow AI"""
    
    def __init__(self):
        self.hotkeys = {}
        self.hotkey_thread = None
        self.is_listening = False
        self.config_file = Path("config/hotkeys.json")
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Try to import keyboard library
        self.keyboard_available = self._setup_keyboard()
        
        # Default hotkeys
        self.default_hotkeys = {
            'ctrl+shift+s': 'take_screenshot',
            'ctrl+shift+n': 'open_notepad',
            'ctrl+shift+c': 'copy_current_selection',
            'ctrl+shift+v': 'paste_clipboard',
            'ctrl+shift+h': 'show_help',
            'ctrl+shift+q': 'show_quick_menu'
        }
        
        # Load configuration
        self.load_config()
        
        # Available actions
        self.actions = {}
        self.register_default_actions()
    
    def _setup_keyboard(self) -> bool:
        """Setup keyboard monitoring"""
        try:
            import keyboard
            self.keyboard = keyboard
            return True
        except ImportError:
            try:
                import pynput.keyboard as pynput_kb
                self.pynput_keyboard = pynput_kb
                self.use_pynput = True
                return True
            except ImportError:
                logging.warning("No keyboard library available. Install keyboard or pynput for hotkey support")
                return False
    
    def register_action(self, name: str, function: Callable, description: str = ""):
        """Register an action that can be bound to hotkeys"""
        self.actions[name] = {
            'function': function,
            'description': description,
            'usage_count': 0,
            'last_used': None
        }
        logging.info(f"Registered action: {name}")
    
    def register_default_actions(self):
        """Register default Shadow AI actions"""
        from datetime import datetime
        
        def take_screenshot():
            try:
                from control.desktop import desktop_controller
                result = desktop_controller.take_screenshot()
                if result:
                    from control.notifications import notify_success
                    notify_success(f"Screenshot saved: {result}")
                return result
            except Exception as e:
                logging.error(f"Hotkey screenshot error: {e}")
                return False
        
        def open_notepad():
            try:
                from control.desktop import desktop_controller
                result = desktop_controller.open_notepad()
                if result:
                    from control.notifications import notify_success
                    notify_success("Notepad opened")
                return result
            except Exception as e:
                logging.error(f"Hotkey notepad error: {e}")
                return False
        
        def copy_current_selection():
            try:
                if hasattr(self, 'keyboard'):
                    self.keyboard.send('ctrl+c')
                    time.sleep(0.1)
                    from control.clipboard_manager import clipboard_manager
                    content = clipboard_manager.get_clipboard_content()
                    if content:
                        from control.notifications import notify_success
                        notify_success(f"Copied: {content[:30]}...")
                    return True
                return False
            except Exception as e:
                logging.error(f"Hotkey copy error: {e}")
                return False
        
        def paste_clipboard():
            try:
                if hasattr(self, 'keyboard'):
                    self.keyboard.send('ctrl+v')
                    from control.notifications import notify_success
                    notify_success("Content pasted")
                    return True
                return False
            except Exception as e:
                logging.error(f"Hotkey paste error: {e}")
                return False
        
        def show_help():
            try:
                help_text = self.get_hotkey_help()
                from control.notifications import notification_manager
                notification_manager.show_notification("🔥 Hotkeys", help_text, duration=10000)
                return True
            except Exception as e:
                logging.error(f"Hotkey help error: {e}")
                return False
        
        def show_quick_menu():
            try:
                from control.notifications import notification_manager
                menu_text = "Quick Menu:\n• Ctrl+Shift+S: Screenshot\n• Ctrl+Shift+N: Notepad\n• Ctrl+Shift+C: Copy\n• Ctrl+Shift+V: Paste"
                notification_manager.show_notification("🚀 Quick Menu", menu_text, duration=8000)
                return True
            except Exception as e:
                logging.error(f"Hotkey menu error: {e}")
                return False
        
        def toggle_voice_mode():
            try:
                # This would toggle voice mode if implemented
                from control.notifications import notification_manager
                notification_manager.show_notification("🎤 Voice Mode", "Voice mode toggled")
                return True
            except Exception as e:
                logging.error(f"Hotkey voice toggle error: {e}")
                return False
        
        def quick_web_search():
            try:
                from control.clipboard_manager import clipboard_manager
                query = clipboard_manager.get_clipboard_content()
                if query:
                    from control.web_search import web_search
                    result = web_search.search_web(query)
                    if result:
                        from control.notifications import notify_success
                        notify_success(f"Web search: {query[:30]}...")
                    return result
                return False
            except Exception as e:
                logging.error(f"Hotkey web search error: {e}")
                return False
        
        def system_info():
            try:
                from control.system_info import system_diagnostics
                cpu_info = system_diagnostics.get_cpu_info()
                mem_info = system_diagnostics.get_memory_info()
                
                info_text = f"CPU: {cpu_info.get('cpu_percent_total', 'N/A')}%\nMemory: {mem_info.get('percentage', 'N/A')}%"
                from control.notifications import notification_manager
                notification_manager.show_notification("💻 System Info", info_text)
                return True
            except Exception as e:
                logging.error(f"Hotkey system info error: {e}")
                return False
        
        # Register all actions
        self.register_action('take_screenshot', take_screenshot, "Take a screenshot")
        self.register_action('open_notepad', open_notepad, "Open Notepad")
        self.register_action('copy_current_selection', copy_current_selection, "Copy current selection")
        self.register_action('paste_clipboard', paste_clipboard, "Paste from clipboard")
        self.register_action('show_help', show_help, "Show hotkey help")
        self.register_action('show_quick_menu', show_quick_menu, "Show quick action menu")
        self.register_action('toggle_voice_mode', toggle_voice_mode, "Toggle voice mode")
        self.register_action('quick_web_search', quick_web_search, "Search web with clipboard content")
        self.register_action('system_info', system_info, "Show system information")
    
    def add_hotkey(self, hotkey: str, action_name: str) -> bool:
        """Add a new hotkey"""
        try:
            if action_name not in self.actions:
                logging.error(f"Action '{action_name}' not registered")
                return False
            
            # Remove existing hotkey if any
            self.remove_hotkey(hotkey)
            
            self.hotkeys[hotkey] = action_name
            
            if self.keyboard_available and self.is_listening:
                self._register_system_hotkey(hotkey, action_name)
            
            self.save_config()
            logging.info(f"Added hotkey: {hotkey} -> {action_name}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding hotkey: {e}")
            return False
    
    def remove_hotkey(self, hotkey: str) -> bool:
        """Remove a hotkey"""
        try:
            if hotkey in self.hotkeys:
                if self.keyboard_available and self.is_listening:
                    self._unregister_system_hotkey(hotkey)
                
                del self.hotkeys[hotkey]
                self.save_config()
                logging.info(f"Removed hotkey: {hotkey}")
                return True
            else:
                logging.warning(f"Hotkey not found: {hotkey}")
                return False
                
        except Exception as e:
            logging.error(f"Error removing hotkey: {e}")
            return False
    
    def start_listening(self) -> bool:
        """Start listening for hotkeys"""
        try:
            if not self.keyboard_available:
                logging.error("Keyboard library not available")
                return False
            
            if self.is_listening:
                logging.info("Already listening for hotkeys")
                return True
            
            self.is_listening = True
            
            if hasattr(self, 'keyboard'):
                # Register all hotkeys
                for hotkey, action_name in self.hotkeys.items():
                    self._register_system_hotkey(hotkey, action_name)
                
                logging.info(f"Started listening for {len(self.hotkeys)} hotkeys")
            
            return True
            
        except Exception as e:
            logging.error(f"Error starting hotkey listener: {e}")
            return False
    
    def stop_listening(self) -> bool:
        """Stop listening for hotkeys"""
        try:
            if not self.is_listening:
                return True
            
            self.is_listening = False
            
            if hasattr(self, 'keyboard'):
                # Unregister all hotkeys
                for hotkey in self.hotkeys.keys():
                    self._unregister_system_hotkey(hotkey)
            
            logging.info("Stopped listening for hotkeys")
            return True
            
        except Exception as e:
            logging.error(f"Error stopping hotkey listener: {e}")
            return False
    
    def _register_system_hotkey(self, hotkey: str, action_name: str):
        """Register hotkey with system"""
        try:
            if hasattr(self, 'keyboard'):
                def callback():
                    self._execute_action(action_name)
                
                self.keyboard.add_hotkey(hotkey, callback)
                
        except Exception as e:
            logging.error(f"Error registering system hotkey {hotkey}: {e}")
    
    def _unregister_system_hotkey(self, hotkey: str):
        """Unregister hotkey from system"""
        try:
            if hasattr(self, 'keyboard'):
                self.keyboard.remove_hotkey(hotkey)
                
        except Exception as e:
            logging.error(f"Error unregistering system hotkey {hotkey}: {e}")
    
    def _execute_action(self, action_name: str):
        """Execute hotkey action"""
        try:
            if action_name in self.actions:
                action = self.actions[action_name]
                
                # Update usage statistics
                action['usage_count'] += 1
                action['last_used'] = time.time()
                
                # Execute action in separate thread to avoid blocking
                def run_action():
                    try:
                        result = action['function']()
                        logging.info(f"Hotkey action '{action_name}' executed: {result}")
                    except Exception as e:
                        logging.error(f"Error executing hotkey action '{action_name}': {e}")
                
                threading.Thread(target=run_action, daemon=True).start()
            else:
                logging.error(f"Action not found: {action_name}")
                
        except Exception as e:
            logging.error(f"Error executing hotkey action: {e}")
    
    def get_hotkey_help(self) -> str:
        """Get help text for hotkeys"""
        help_lines = ["🔥 Shadow AI Hotkeys:"]
        
        for hotkey, action_name in self.hotkeys.items():
            if action_name in self.actions:
                description = self.actions[action_name]['description']
                help_lines.append(f"• {hotkey}: {description}")
        
        return "\n".join(help_lines)
    
    def list_hotkeys(self) -> List[Dict]:
        """List all configured hotkeys"""
        hotkey_list = []
        
        for hotkey, action_name in self.hotkeys.items():
            if action_name in self.actions:
                action = self.actions[action_name]
                hotkey_list.append({
                    'hotkey': hotkey,
                    'action': action_name,
                    'description': action['description'],
                    'usage_count': action['usage_count'],
                    'last_used': action['last_used']
                })
        
        return hotkey_list
    
    def get_usage_statistics(self) -> Dict:
        """Get hotkey usage statistics"""
        stats = {
            'total_hotkeys': len(self.hotkeys),
            'total_actions': len(self.actions),
            'most_used_action': None,
            'total_usage': 0,
            'listening': self.is_listening
        }
        
        max_usage = 0
        for action_name, action in self.actions.items():
            usage_count = action['usage_count']
            stats['total_usage'] += usage_count
            
            if usage_count > max_usage:
                max_usage = usage_count
                stats['most_used_action'] = {
                    'name': action_name,
                    'count': usage_count,
                    'description': action['description']
                }
        
        return stats
    
    def reset_default_hotkeys(self) -> bool:
        """Reset to default hotkeys"""
        try:
            self.stop_listening()
            self.hotkeys = self.default_hotkeys.copy()
            self.save_config()
            self.start_listening()
            logging.info("Reset to default hotkeys")
            return True
            
        except Exception as e:
            logging.error(f"Error resetting default hotkeys: {e}")
            return False
    
    def save_config(self):
        """Save hotkey configuration"""
        try:
            config = {
                'hotkeys': self.hotkeys,
                'listening': self.is_listening
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
                
        except Exception as e:
            logging.error(f"Error saving hotkey config: {e}")
    
    def load_config(self):
        """Load hotkey configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.hotkeys = config.get('hotkeys', self.default_hotkeys.copy())
                was_listening = config.get('listening', False)
                
                if was_listening and self.keyboard_available:
                    self.start_listening()
                    
                logging.info(f"Loaded {len(self.hotkeys)} hotkeys from config")
            else:
                self.hotkeys = self.default_hotkeys.copy()
                self.save_config()
                
        except Exception as e:
            logging.error(f"Error loading hotkey config: {e}")
            self.hotkeys = self.default_hotkeys.copy()

# Global instance
hotkey_manager = HotkeyManager()

# Convenience functions
def add_hotkey(hotkey: str, action_name: str) -> bool:
    """Quick add hotkey"""
    return hotkey_manager.add_hotkey(hotkey, action_name)

def remove_hotkey(hotkey: str) -> bool:
    """Quick remove hotkey"""
    return hotkey_manager.remove_hotkey(hotkey)

def start_hotkeys() -> bool:
    """Quick start listening"""
    return hotkey_manager.start_listening()

def stop_hotkeys() -> bool:
    """Quick stop listening"""
    return hotkey_manager.stop_listening()
