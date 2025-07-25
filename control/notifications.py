#!/usr/bin/env python3
"""
Notification System for Shadow AI
Provides desktop notifications and alerts
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

class NotificationManager:
    """Desktop notification and alert system"""
    
    def __init__(self):
        self.notification_history = []
        self.active_notifications = []
        self.notification_settings = {
            'enabled': True,
            'sound_enabled': True,
            'duration': 5000,  # 5 seconds
            'position': 'bottom-right'
        }
        
        # Check available notification methods
        self.notification_method = self._detect_notification_method()
    
    def _detect_notification_method(self) -> str:
        """Detect the best notification method for the system"""
        try:
            # Try Windows 10+ toast notifications
            import win10toast
            return 'win10toast'
        except ImportError:
            try:
                # Try plyer (cross-platform)
                import plyer
                return 'plyer'
            except ImportError:
                # Fallback to Windows built-in msg command
                if os.name == 'nt':
                    return 'windows_msg'
                else:
                    return 'console'
    
    def show_notification(self, title: str, message: str, icon: str = None, duration: int = None) -> bool:
        """Show desktop notification"""
        try:
            if not self.notification_settings['enabled']:
                return False
            
            duration = duration or self.notification_settings['duration']
            
            notification_data = {
                'timestamp': datetime.now(),
                'title': title,
                'message': message,
                'icon': icon,
                'duration': duration
            }
            
            success = False
            
            if self.notification_method == 'win10toast':
                success = self._show_win10_toast(title, message, icon, duration)
            elif self.notification_method == 'plyer':
                success = self._show_plyer_notification(title, message, icon, duration)
            elif self.notification_method == 'windows_msg':
                success = self._show_windows_msg(title, message)
            else:
                success = self._show_console_notification(title, message)
            
            if success:
                self.notification_history.append(notification_data)
                # Keep only last 100 notifications
                if len(self.notification_history) > 100:
                    self.notification_history = self.notification_history[-100:]
            
            return success
            
        except Exception as e:
            logging.error(f"Error showing notification: {e}")
            return False
    
    def _show_win10_toast(self, title: str, message: str, icon: str = None, duration: int = 5000) -> bool:
        """Show Windows 10 toast notification"""
        try:
            import win10toast
            toaster = win10toast.ToastNotifier()
            
            # Convert duration from milliseconds to seconds
            duration_sec = duration // 1000
            
            toaster.show_toast(
                title,
                message,
                icon_path=icon,
                duration=duration_sec,
                threaded=True
            )
            return True
            
        except Exception as e:
            logging.error(f"Error with win10toast: {e}")
            return False
    
    def _show_plyer_notification(self, title: str, message: str, icon: str = None, duration: int = 5000) -> bool:
        """Show notification using plyer"""
        try:
            from plyer import notification
            
            # Convert duration from milliseconds to seconds
            timeout = duration // 1000
            
            notification.notify(
                title=title,
                message=message,
                app_icon=icon,
                timeout=timeout
            )
            return True
            
        except Exception as e:
            logging.error(f"Error with plyer notification: {e}")
            return False
    
    def _show_windows_msg(self, title: str, message: str) -> bool:
        """Show notification using Windows msg command"""
        try:
            # Use Windows msg command (works on Windows)
            full_message = f"{title}\\n\\n{message}"
            subprocess.run(['msg', '*', full_message], check=False, capture_output=True)
            return True
            
        except Exception as e:
            logging.error(f"Error with Windows msg: {e}")
            return False
    
    def _show_console_notification(self, title: str, message: str) -> bool:
        """Show notification in console (fallback)"""
        try:
            print(f"\n🔔 NOTIFICATION: {title}")
            print(f"📝 {message}")
            print("─" * 50)
            return True
            
        except Exception as e:
            logging.error(f"Error with console notification: {e}")
            return False
    
    def show_success_notification(self, message: str) -> bool:
        """Show success notification"""
        return self.show_notification("✅ Success", message)
    
    def show_error_notification(self, message: str) -> bool:
        """Show error notification"""
        return self.show_notification("❌ Error", message)
    
    def show_warning_notification(self, message: str) -> bool:
        """Show warning notification"""
        return self.show_notification("⚠️ Warning", message)
    
    def show_info_notification(self, message: str) -> bool:
        """Show info notification"""
        return self.show_notification("ℹ️ Information", message)
    
    def show_task_completion(self, task_name: str, execution_time: float = None) -> bool:
        """Show task completion notification"""
        if execution_time:
            message = f"Task '{task_name}' completed in {execution_time:.1f} seconds"
        else:
            message = f"Task '{task_name}' completed successfully"
        
        return self.show_notification("🎯 Task Complete", message)
    
    def show_system_alert(self, alert_type: str, details: str) -> bool:
        """Show system alert notification"""
        icons = {
            'cpu': '🔥',
            'memory': '💾',
            'disk': '💿',
            'network': '🌐',
            'battery': '🔋'
        }
        
        icon = icons.get(alert_type, '⚠️')
        title = f"{icon} System Alert: {alert_type.title()}"
        
        return self.show_notification(title, details)
    
    def show_reminder(self, reminder_text: str) -> bool:
        """Show reminder notification"""
        return self.show_notification("⏰ Reminder", reminder_text)
    
    def schedule_notification(self, title: str, message: str, delay_seconds: int) -> bool:
        """Schedule a notification for later"""
        try:
            import threading
            
            def delayed_notification():
                time.sleep(delay_seconds)
                self.show_notification(title, message)
            
            thread = threading.Thread(target=delayed_notification, daemon=True)
            thread.start()
            
            return True
            
        except Exception as e:
            logging.error(f"Error scheduling notification: {e}")
            return False
    
    def get_notification_history(self, limit: int = 20) -> List[Dict]:
        """Get recent notification history"""
        return self.notification_history[-limit:]
    
    def clear_notification_history(self) -> bool:
        """Clear notification history"""
        try:
            self.notification_history.clear()
            return True
        except Exception as e:
            logging.error(f"Error clearing notification history: {e}")
            return False
    
    def configure_notifications(self, enabled: bool = None, sound: bool = None, duration: int = None) -> bool:
        """Configure notification settings"""
        try:
            if enabled is not None:
                self.notification_settings['enabled'] = enabled
            
            if sound is not None:
                self.notification_settings['sound_enabled'] = sound
            
            if duration is not None:
                self.notification_settings['duration'] = duration
            
            return True
            
        except Exception as e:
            logging.error(f"Error configuring notifications: {e}")
            return False
    
    def test_notifications(self) -> bool:
        """Test notification system"""
        try:
            test_messages = [
                ("Test Notification", "This is a test notification from Shadow AI"),
                ("✅ Success Test", "Success notification test"),
                ("❌ Error Test", "Error notification test"),
                ("⚠️ Warning Test", "Warning notification test"),
                ("ℹ️ Info Test", "Information notification test")
            ]
            
            for title, message in test_messages:
                self.show_notification(title, message, duration=2000)
                time.sleep(1)
            
            return True
            
        except Exception as e:
            logging.error(f"Error testing notifications: {e}")
            return False

# Global instance
notification_manager = NotificationManager()

# Convenience functions
def notify_success(message: str) -> bool:
    """Quick success notification"""
    return notification_manager.show_success_notification(message)

def notify_error(message: str) -> bool:
    """Quick error notification"""
    return notification_manager.show_error_notification(message)

def notify_warning(message: str) -> bool:
    """Quick warning notification"""
    return notification_manager.show_warning_notification(message)

def notify_info(message: str) -> bool:
    """Quick info notification"""
    return notification_manager.show_info_notification(message)

def notify_task_complete(task_name: str, execution_time: float = None) -> bool:
    """Quick task completion notification"""
    return notification_manager.show_task_completion(task_name, execution_time)
