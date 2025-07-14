"""
Shadow AI Configuration Management
Centralized configuration management with validation and type checking.
"""

from typing import Any, Dict, Optional
import json
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

class Config:
    """Configuration manager for Shadow AI."""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._load_env()
        self._load_config()
        
    def _load_env(self) -> None:
        """Load environment variables."""
        load_dotenv()
        
        # Required API keys
        self._config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        self._config['google_api_key'] = os.getenv('GOOGLE_API_KEY')
        
    def _load_config(self) -> None:
        """Load configuration from config.json."""
        config_path = Path('config.json')
        
        if not config_path.exists():
            self._create_default_config()
            
        try:
            with open(config_path, 'r') as f:
                self._config.update(json.load(f))
        except Exception as e:
            logging.error(f"Failed to load config.json: {e}")
            self._create_default_config()
            
    def _create_default_config(self) -> None:
        """Create default configuration file."""
        default_config = {
            'gui': {
                'theme': 'dark',
                'window_size': [800, 600],
                'opacity': 0.95
            },
            'tts': {
                'enabled': True,
                'rate': 150,
                'volume': 0.9
            },
            'automation': {
                'whatsapp': {
                    'enabled': True,
                    'delay': 0.5
                },
                'browser': {
                    'enabled': True,
                    'default_wait': 10
                }
            },
            'logging': {
                'level': 'INFO',
                'file': 'shadow.log'
            },
            'plugins': {
                'enabled': True,
                'load_on_startup': []
            }
        }
        
        try:
            with open('config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            self._config.update(default_config)
        except Exception as e:
            logging.error(f"Failed to create default config: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
        self._save_config()
        
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            # Don't save API keys to config.json
            config_to_save = {k: v for k, v in self._config.items() 
                            if k not in ['openai_api_key', 'google_api_key']}
            
            with open('config.json', 'w') as f:
                json.dump(config_to_save, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save config: {e}")
            
    def validate(self) -> bool:
        """Validate configuration."""
        required_keys = ['openai_api_key', 'google_api_key']
        
        for key in required_keys:
            if not self._config.get(key):
                logging.error(f"Missing required configuration: {key}")
                return False
                
        return True
        
# Global configuration instance
config = Config()
