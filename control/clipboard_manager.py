#!/usr/bin/env python3
"""
Clipboard Management Module for Shadow AI
Provides advanced clipboard operations and history
"""

import logging
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

class ClipboardManager:
    """Advanced clipboard management with history"""
    
    def __init__(self):
        self.clipboard_history = []
        self.max_history = 100
        self.history_file = Path("logs/clipboard_history.json")
        self.history_file.parent.mkdir(exist_ok=True)
        
        # Try to import clipboard libraries
        self.clipboard_available = self._setup_clipboard()
        
        # Load history if available
        self.load_history()
    
    def _setup_clipboard(self) -> bool:
        """Setup clipboard functionality"""
        try:
            import pyperclip
            self.pyperclip = pyperclip
            return True
        except ImportError:
            try:
                import win32clipboard
                self.win32clipboard = win32clipboard
                self.use_win32 = True
                return True
            except ImportError:
                logging.warning("No clipboard library available. Install pyperclip or pywin32")
                return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            if not self.clipboard_available:
                logging.error("Clipboard functionality not available")
                return False
            
            if hasattr(self, 'pyperclip'):
                self.pyperclip.copy(text)
            elif hasattr(self, 'win32clipboard'):
                self.win32clipboard.OpenClipboard()
                self.win32clipboard.EmptyClipboard()
                self.win32clipboard.SetClipboardText(text)
                self.win32clipboard.CloseClipboard()
            
            # Add to history
            self.add_to_history(text, "copy")
            logging.info(f"Copied to clipboard: {text[:50]}...")
            return True
            
        except Exception as e:
            logging.error(f"Error copying to clipboard: {e}")
            return False
    
    def paste_from_clipboard(self) -> str:
        """Get text from clipboard"""
        try:
            if not self.clipboard_available:
                logging.error("Clipboard functionality not available")
                return ""
            
            if hasattr(self, 'pyperclip'):
                text = self.pyperclip.paste()
            elif hasattr(self, 'win32clipboard'):
                self.win32clipboard.OpenClipboard()
                text = self.win32clipboard.GetClipboardData()
                self.win32clipboard.CloseClipboard()
            else:
                return ""
            
            # Add to history
            self.add_to_history(text, "paste")
            logging.info(f"Pasted from clipboard: {text[:50]}...")
            return text
            
        except Exception as e:
            logging.error(f"Error pasting from clipboard: {e}")
            return ""
    
    def get_clipboard_content(self) -> str:
        """Get current clipboard content without adding to history"""
        try:
            if not self.clipboard_available:
                return ""
            
            if hasattr(self, 'pyperclip'):
                return self.pyperclip.paste()
            elif hasattr(self, 'win32clipboard'):
                self.win32clipboard.OpenClipboard()
                text = self.win32clipboard.GetClipboardData()
                self.win32clipboard.CloseClipboard()
                return text
            else:
                return ""
                
        except Exception as e:
            logging.error(f"Error getting clipboard content: {e}")
            return ""
    
    def clear_clipboard(self) -> bool:
        """Clear clipboard content"""
        try:
            if not self.clipboard_available:
                return False
            
            if hasattr(self, 'pyperclip'):
                self.pyperclip.copy("")
            elif hasattr(self, 'win32clipboard'):
                self.win32clipboard.OpenClipboard()
                self.win32clipboard.EmptyClipboard()
                self.win32clipboard.CloseClipboard()
            
            self.add_to_history("", "clear")
            logging.info("Clipboard cleared")
            return True
            
        except Exception as e:
            logging.error(f"Error clearing clipboard: {e}")
            return False
    
    def add_to_history(self, content: str, operation: str):
        """Add item to clipboard history"""
        try:
            # Don't add empty content or duplicates
            if not content or (self.clipboard_history and self.clipboard_history[-1].get('content') == content):
                return
            
            history_item = {
                'timestamp': datetime.now().isoformat(),
                'content': content[:1000],  # Limit content length
                'operation': operation,
                'length': len(content)
            }
            
            self.clipboard_history.append(history_item)
            
            # Keep only last max_history items
            if len(self.clipboard_history) > self.max_history:
                self.clipboard_history = self.clipboard_history[-self.max_history:]
            
            # Save to file
            self.save_history()
            
        except Exception as e:
            logging.error(f"Error adding to clipboard history: {e}")
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """Get clipboard history"""
        return self.clipboard_history[-limit:]
    
    def search_history(self, query: str, limit: int = 10) -> List[Dict]:
        """Search clipboard history"""
        try:
            query = query.lower()
            results = []
            
            for item in reversed(self.clipboard_history):
                if query in item['content'].lower():
                    results.append(item)
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            logging.error(f"Error searching clipboard history: {e}")
            return []
    
    def restore_from_history(self, index: int) -> bool:
        """Restore clipboard content from history"""
        try:
            if 0 <= index < len(self.clipboard_history):
                content = self.clipboard_history[-(index + 1)]['content']
                return self.copy_to_clipboard(content)
            else:
                logging.error(f"Invalid history index: {index}")
                return False
                
        except Exception as e:
            logging.error(f"Error restoring from history: {e}")
            return False
    
    def copy_file_path(self, file_path: str) -> bool:
        """Copy file path to clipboard"""
        try:
            file_path = str(Path(file_path).resolve())
            return self.copy_to_clipboard(file_path)
            
        except Exception as e:
            logging.error(f"Error copying file path: {e}")
            return False
    
    def copy_file_content(self, file_path: str) -> bool:
        """Copy file content to clipboard"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.copy_to_clipboard(content)
            
        except Exception as e:
            logging.error(f"Error copying file content: {e}")
            return False
    
    def save_clipboard_to_file(self, file_path: str) -> bool:
        """Save clipboard content to file"""
        try:
            content = self.get_clipboard_content()
            if content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.info(f"Saved clipboard to: {file_path}")
                return True
            else:
                logging.warning("No content in clipboard to save")
                return False
                
        except Exception as e:
            logging.error(f"Error saving clipboard to file: {e}")
            return False
    
    def copy_formatted_text(self, text: str, format_type: str = 'upper') -> bool:
        """Copy text with formatting applied"""
        try:
            if format_type == 'upper':
                formatted_text = text.upper()
            elif format_type == 'lower':
                formatted_text = text.lower()
            elif format_type == 'title':
                formatted_text = text.title()
            elif format_type == 'reverse':
                formatted_text = text[::-1]
            elif format_type == 'no_spaces':
                formatted_text = text.replace(' ', '')
            elif format_type == 'underscore':
                formatted_text = text.replace(' ', '_')
            elif format_type == 'dash':
                formatted_text = text.replace(' ', '-')
            else:
                formatted_text = text
            
            return self.copy_to_clipboard(formatted_text)
            
        except Exception as e:
            logging.error(f"Error copying formatted text: {e}")
            return False
    
    def copy_system_info(self, info_type: str) -> bool:
        """Copy system information to clipboard"""
        try:
            import platform
            import os
            
            if info_type == 'hostname':
                content = platform.node()
            elif info_type == 'username':
                content = os.getenv('USERNAME', 'Unknown')
            elif info_type == 'os':
                content = f"{platform.system()} {platform.release()}"
            elif info_type == 'python_version':
                content = platform.python_version()
            elif info_type == 'current_time':
                content = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif info_type == 'current_path':
                content = str(Path.cwd())
            else:
                content = f"Unknown system info type: {info_type}"
            
            return self.copy_to_clipboard(content)
            
        except Exception as e:
            logging.error(f"Error copying system info: {e}")
            return False
    
    def save_history(self):
        """Save clipboard history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.clipboard_history, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving clipboard history: {e}")
    
    def load_history(self):
        """Load clipboard history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.clipboard_history = json.load(f)
                logging.info(f"Loaded {len(self.clipboard_history)} clipboard history items")
        except Exception as e:
            logging.error(f"Error loading clipboard history: {e}")
            self.clipboard_history = []
    
    def clear_history(self) -> bool:
        """Clear clipboard history"""
        try:
            self.clipboard_history.clear()
            self.save_history()
            logging.info("Clipboard history cleared")
            return True
        except Exception as e:
            logging.error(f"Error clearing clipboard history: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get clipboard usage statistics"""
        try:
            stats = {
                'total_items': len(self.clipboard_history),
                'operations': {},
                'average_length': 0,
                'longest_content': 0,
                'most_recent': None
            }
            
            if self.clipboard_history:
                # Count operations
                for item in self.clipboard_history:
                    op = item['operation']
                    stats['operations'][op] = stats['operations'].get(op, 0) + 1
                
                # Calculate averages
                total_length = sum(item['length'] for item in self.clipboard_history)
                stats['average_length'] = total_length // len(self.clipboard_history)
                stats['longest_content'] = max(item['length'] for item in self.clipboard_history)
                stats['most_recent'] = self.clipboard_history[-1]['timestamp']
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting clipboard statistics: {e}")
            return {}

# Global instance
clipboard_manager = ClipboardManager()

# Convenience functions
def copy_text(text: str) -> bool:
    """Quick copy to clipboard"""
    return clipboard_manager.copy_to_clipboard(text)

def paste_text() -> str:
    """Quick paste from clipboard"""
    return clipboard_manager.paste_from_clipboard()

def clear_clipboard() -> bool:
    """Quick clear clipboard"""
    return clipboard_manager.clear_clipboard()

def get_clipboard() -> str:
    """Quick get clipboard content"""
    return clipboard_manager.get_clipboard_content()
