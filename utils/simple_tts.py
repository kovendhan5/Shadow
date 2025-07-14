"""Simple Text-to-Speech implementation using pyttsx3."""
import pyttsx3
import logging
from typing import Optional

class SimpleTTS:
    def __init__(self):
        self._engine = None
        self._initialized = False
        self.setup()
    
    def setup(self) -> None:
        """Initialize the TTS engine."""
        if not self._initialized:
            try:
                self._engine = pyttsx3.init()
                self._engine.setProperty('rate', 150)  # Speaking rate
                self._engine.setProperty('volume', 0.9)  # Volume level
                self._initialized = True
            except Exception as e:
                logging.error(f"Failed to initialize TTS engine: {e}")
                self._initialized = False
    
    def speak(self, text: str) -> bool:
        """Speak the given text using TTS.
        
        Args:
            text: The text to speak
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._initialized:
            self.setup()
            
        if not self._initialized:
            logging.error("TTS engine not initialized")
            return False
            
        try:
            self._engine.say(text)
            self._engine.runAndWait()
            return True
        except Exception as e:
            logging.error(f"TTS error: {e}")
            return False
    
    def stop(self) -> None:
        """Stop any ongoing speech."""
        if self._initialized:
            try:
                self._engine.stop()
            except Exception as e:
                logging.error(f"Error stopping TTS: {e}")

# Global TTS instance
_tts = SimpleTTS()

def speak(text: str) -> bool:
    """Global speak function."""
    return _tts.speak(text)

def stop_speaking() -> None:
    """Stop any ongoing speech."""
    _tts.stop()
