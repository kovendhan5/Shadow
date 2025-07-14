"""
Shadow AI - Modern Launcher
This script handles dependency checks, environment setup, and proper initialization.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('shadow.log')
    ]
)

def check_python_version() -> bool:
    """Check if Python version meets requirements."""
    required_version = (3, 11)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        logging.error(f"Python {required_version[0]}.{required_version[1]} or higher is required")
        return False
    return True

def check_virtual_env() -> bool:
    """Check if running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def setup_virtual_env() -> bool:
    """Set up a virtual environment if not already in one."""
    if check_virtual_env():
        return True
        
    try:
        venv_path = Path('venv')
        if not venv_path.exists():
            logging.info("Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            
        # Activate virtual environment
        if os.name == 'nt':  # Windows
            activate_script = venv_path / 'Scripts' / 'activate.bat'
            subprocess.run([str(activate_script)], shell=True, check=True)
        else:  # Unix
            activate_script = venv_path / 'bin' / 'activate'
            subprocess.run(['source', str(activate_script)], shell=True, check=True)
            
        return True
    except Exception as e:
        logging.error(f"Failed to setup virtual environment: {e}")
        return False

def install_dependencies() -> bool:
    """Install or update project dependencies."""
    try:
        logging.info("Installing/updating dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'], check=True)
        return True
    except Exception as e:
        logging.error(f"Failed to install dependencies: {e}")
        return False

def check_config() -> bool:
    """Check and validate configuration."""
    try:
        from dotenv import load_dotenv
        
        if not Path('.env').exists():
            logging.warning(".env file not found. Creating template...")
            with open('.env', 'w') as f:
                f.write("# Shadow AI Configuration\n")
                f.write("OPENAI_API_KEY=your_key_here\n")
                f.write("GOOGLE_API_KEY=your_key_here\n")
            logging.info("Please update .env with your API keys")
            return False
            
        load_dotenv()
        required_vars = ['OPENAI_API_KEY', 'GOOGLE_API_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            logging.error(f"Missing required environment variables: {', '.join(missing)}")
            return False
            
        return True
    except Exception as e:
        logging.error(f"Configuration error: {e}")
        return False

def main() -> int:
    """Main launcher function."""
    logging.info("Starting Shadow AI launcher...")
    
    # Essential checks
    if not check_python_version():
        return 1
        
    if not setup_virtual_env():
        return 1
        
    if not install_dependencies():
        return 1
        
    if not check_config():
        return 1
    
    try:
        logging.info("Starting Shadow AI...")
        import main
        return main.main()
    except Exception as e:
        logging.error(f"Failed to start Shadow AI: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
