"""
Shadow AI Control Module
System control and automation with enhanced features
"""

from .desktop import desktop_controller
from .browser import get_browser_controller
from .documents import document_controller

# Enhanced features - with graceful fallback if not available
try:
    from .file_manager import EnhancedFileManager
    FILE_MANAGER_AVAILABLE = True
except ImportError:
    FILE_MANAGER_AVAILABLE = False

try:
    from .web_search import QuickWebSearch
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False

try:
    from .system_info import SystemDiagnostics
    SYSTEM_INFO_AVAILABLE = True
except ImportError:
    SYSTEM_INFO_AVAILABLE = False

try:
    from .notifications import NotificationManager
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

try:
    from .clipboard_manager import ClipboardManager
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    from .hotkey_manager import HotkeyManager
    HOTKEYS_AVAILABLE = True
except ImportError:
    HOTKEYS_AVAILABLE = False

__all__ = [
    'desktop_controller',
    'get_browser_controller', 
    'document_controller',
    'EnhancedFileManager',
    'QuickWebSearch',
    'SystemDiagnostics',
    'NotificationManager',
    'ClipboardManager',
    'HotkeyManager',
    'FILE_MANAGER_AVAILABLE',
    'WEB_SEARCH_AVAILABLE',
    'SYSTEM_INFO_AVAILABLE',
    'NOTIFICATIONS_AVAILABLE',
    'CLIPBOARD_AVAILABLE',
    'HOTKEYS_AVAILABLE'
]
