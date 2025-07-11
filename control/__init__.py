"""
Shadow AI Control Module
System control and automation
"""

from .desktop import desktop_controller
from .browser import get_browser_controller
from .documents import document_controller

__all__ = [
    'desktop_controller',
    'get_browser_controller', 
    'document_controller'
]
