"""
Shadow AI Input Module
Voice and text input handling
"""

from .text_input import get_text_input, show_message
from .voice_input import get_voice_input, speak_response

__all__ = [
    'get_text_input',
    'show_message',
    'get_voice_input', 
    'speak_response'
]
