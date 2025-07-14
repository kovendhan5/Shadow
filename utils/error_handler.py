"""
Shadow AI Error Handling and Logging
Centralized error handling and logging configuration.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Any
from datetime import datetime
import traceback
import json

class ShadowLogger:
    """Advanced logging setup for Shadow AI."""
    
    def __init__(self, log_file: str = 'shadow.log', level: str = 'INFO'):
        self.log_file = Path(log_file)
        self.level = getattr(logging, level.upper())
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure logging with both file and console handlers."""
        # Create logs directory if it doesn't exist
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Basic configuration
        logging.basicConfig(
            level=self.level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.log_file)
            ]
        )
        
        # Set up exception hook
        sys.excepthook = self._handle_exception
        
    def _handle_exception(self, exc_type: type, exc_value: Exception, exc_traceback: Any) -> None:
        """Custom exception handler that logs full stack traces."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        logging.error("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))
        
    def log_error(self, error: Exception, context: dict = None) -> None:
        """Log an error with additional context."""
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        logging.error(json.dumps(error_info, indent=2))
        
    def setup_module_logger(self, module_name: str) -> logging.Logger:
        """Create a logger for a specific module."""
        logger = logging.getLogger(module_name)
        logger.setLevel(self.level)
        return logger
        
# Global logger instance
logger = ShadowLogger()

def get_logger(module_name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logger.setup_module_logger(module_name)
