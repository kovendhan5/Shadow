# confirm.py
import logging
import tkinter as tk
from tkinter import messagebox
import threading
import time
from config import REQUIRE_CONFIRMATION, CONFIRMATION_TIMEOUT
from input.text_input import confirm_action as text_confirm
from input.voice_input import confirm_action as voice_confirm

class ConfirmationManager:
    def __init__(self):
        self.root = None
        self.setup_gui()
    
    def setup_gui(self):
        """Setup GUI for confirmation dialogs"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        self.root.title("Shadow AI - Confirmation")
    
    def confirm_action(self, action: str, method: str = "gui", timeout: int = CONFIRMATION_TIMEOUT) -> bool:
        """
        Ask for user confirmation before performing an action
        
        Args:
            action: Description of the action to confirm
            method: Confirmation method ('gui', 'text', 'voice', 'auto')
            timeout: Timeout in seconds for confirmation
        
        Returns:
            bool: True if confirmed, False otherwise
        """
        if not REQUIRE_CONFIRMATION:
            logging.info(f"Confirmation bypassed (disabled in config): {action}")
            return True
        
        logging.info(f"Requesting confirmation for: {action}")
        
        try:
            if method == "gui":
                return self._confirm_gui(action, timeout)
            elif method == "text":
                return self._confirm_text(action, timeout)
            elif method == "voice":
                return self._confirm_voice(action, timeout)
            elif method == "auto":
                return self._confirm_auto(action, timeout)
            else:
                logging.warning(f"Unknown confirmation method: {method}, using GUI")
                return self._confirm_gui(action, timeout)
        
        except Exception as e:
            logging.error(f"Error in confirmation: {e}")
            return False
    
    def _confirm_gui(self, action: str, timeout: int) -> bool:
        """GUI-based confirmation"""
        try:
            question = f"Shadow AI wants to perform the following action:\n\n{action}\n\nDo you want to proceed?"
            
            if timeout > 0:
                return self._confirm_gui_with_timeout(question, timeout)
            else:
                result = messagebox.askyesno("Shadow AI - Confirmation", question, parent=self.root)
                return result
        
        except Exception as e:
            logging.error(f"Error in GUI confirmation: {e}")
            return False
    
    def _confirm_gui_with_timeout(self, question: str, timeout: int) -> bool:
        """GUI confirmation with timeout"""
        result = {'confirmed': False, 'responded': False}
        
        def timeout_handler():
            time.sleep(timeout)
            if not result['responded']:
                logging.warning(f"Confirmation timeout ({timeout}s) - defaulting to False")
                result['confirmed'] = False
                result['responded'] = True
                try:
                    self.root.quit()
                except:
                    pass
        
        def show_dialog():
            try:
                confirmed = messagebox.askyesno("Shadow AI - Confirmation", question, parent=self.root)
                if not result['responded']:
                    result['confirmed'] = confirmed
                    result['responded'] = True
            except Exception as e:
                logging.error(f"Error in timeout dialog: {e}")
                result['confirmed'] = False
                result['responded'] = True
        
        # Start timeout thread
        timeout_thread = threading.Thread(target=timeout_handler)
        timeout_thread.daemon = True
        timeout_thread.start()
        
        # Show dialog
        show_dialog()
        
        # Wait for response or timeout
        start_time = time.time()
        while not result['responded'] and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        return result['confirmed']
    
    def _confirm_text(self, action: str, timeout: int) -> bool:
        """Text-based confirmation"""
        try:
            question = f"Shadow AI wants to perform: {action}\nDo you want to proceed?"
            return text_confirm(question, use_gui=False)
        except Exception as e:
            logging.error(f"Error in text confirmation: {e}")
            return False
    
    def _confirm_voice(self, action: str, timeout: int) -> bool:
        """Voice-based confirmation"""
        try:
            question = f"I want to {action}. Should I proceed?"
            return voice_confirm(question)
        except Exception as e:
            logging.error(f"Error in voice confirmation: {e}")
            return False
    
    def _confirm_auto(self, action: str, timeout: int) -> bool:
        """Auto-select best confirmation method"""
        try:
            # Try GUI first, fallback to text
            try:
                return self._confirm_gui(action, timeout)
            except:
                return self._confirm_text(action, timeout)
        except Exception as e:
            logging.error(f"Error in auto confirmation: {e}")
            return False
    
    def confirm_sensitive_action(self, action: str, details: str = None) -> bool:
        """
        Confirm sensitive actions (financial, data deletion, etc.)
        Always requires confirmation regardless of settings
        """
        full_action = action
        if details:
            full_action += f"\n\nDetails: {details}"
        
        full_action += "\n\n⚠️  THIS IS A SENSITIVE ACTION ⚠️"
        
        logging.warning(f"Sensitive action confirmation required: {action}")
        
        # Force GUI confirmation for sensitive actions
        return self._confirm_gui(full_action, CONFIRMATION_TIMEOUT)
    
    def confirm_financial_action(self, action: str, amount: str = None, merchant: str = None) -> bool:
        """Confirm financial actions with extra details"""
        details = []
        if amount:
            details.append(f"Amount: {amount}")
        if merchant:
            details.append(f"Merchant: {merchant}")
        
        detail_str = "\n".join(details) if details else None
        
        return self.confirm_sensitive_action(f"💰 FINANCIAL ACTION: {action}", detail_str)
    
    def confirm_data_action(self, action: str, data_type: str = None, location: str = None) -> bool:
        """Confirm data-related actions"""
        details = []
        if data_type:
            details.append(f"Data Type: {data_type}")
        if location:
            details.append(f"Location: {location}")
        
        detail_str = "\n".join(details) if details else None
        
        return self.confirm_sensitive_action(f"📂 DATA ACTION: {action}", detail_str)
    
    def cleanup(self):
        """Clean up GUI resources"""
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass

# Global confirmation manager instance
confirmation_manager = ConfirmationManager()

def confirm_action(action: str, method: str = "gui", timeout: int = CONFIRMATION_TIMEOUT) -> bool:
    """Ask for user confirmation before performing an action"""
    return confirmation_manager.confirm_action(action, method, timeout)

def confirm_sensitive_action(action: str, details: str = None) -> bool:
    """Confirm sensitive actions (always requires confirmation)"""
    return confirmation_manager.confirm_sensitive_action(action, details)

def confirm_financial_action(action: str, amount: str = None, merchant: str = None) -> bool:
    """Confirm financial actions"""
    return confirmation_manager.confirm_financial_action(action, amount, merchant)

def confirm_data_action(action: str, data_type: str = None, location: str = None) -> bool:
    """Confirm data-related actions"""
    return confirmation_manager.confirm_data_action(action, data_type, location)

def is_confirmation_required() -> bool:
    """Check if confirmation is required based on settings"""
    return REQUIRE_CONFIRMATION
