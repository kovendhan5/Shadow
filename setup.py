#!/usr/bin/env python3
"""
Shadow AI Agent Setup Script
This script helps set up the Shadow AI environment and dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🧠 Shadow AI Agent Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print("\n📦 Setting up virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def get_pip_command():
    """Get the correct pip command for the current platform"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")

def install_dependencies():
    """Install required dependencies"""
    print("\n📋 Installing dependencies...")
    
    pip_cmd = get_pip_command()
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment_file():
    """Setup .env file"""
    print("\n🔧 Setting up environment file...")
    
    env_path = Path(".env")
    template_path = Path(".env.template")
    
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    if not template_path.exists():
        print("❌ .env.template not found")
        return False
    
    try:
        # Copy template to .env
        with open(template_path, 'r') as template:
            content = template.read()
        
        with open(env_path, 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file with your API keys before running Shadow AI")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_optional_dependencies():
    """Check for optional system dependencies"""
    print("\n🔍 Checking optional dependencies...")
    
    # Check for browser drivers
    drivers = []
    
    # Chrome
    if platform.system() == "Windows":
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
        if any(os.path.exists(path) for path in chrome_paths):
            drivers.append("Chrome")
    
    # Firefox
    if platform.system() == "Windows":
        firefox_paths = [
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        ]
        if any(os.path.exists(path) for path in firefox_paths):
            drivers.append("Firefox")
    
    if drivers:
        print(f"✅ Found browsers: {', '.join(drivers)}")
    else:
        print("⚠️  No browsers found. Install Chrome or Firefox for web automation.")
    
    # Check for Microsoft Office
    if platform.system() == "Windows":
        office_paths = [
            "C:\\Program Files\\Microsoft Office",
            "C:\\Program Files (x86)\\Microsoft Office"
        ]
        if any(os.path.exists(path) for path in office_paths):
            print("✅ Microsoft Office detected")
        else:
            print("⚠️  Microsoft Office not found. Document automation may be limited.")

def run_test():
    """Run a quick test to verify installation"""
    print("\n🧪 Running quick test...")
    
    try:
        # Test imports
        python_cmd = sys.executable
        if platform.system() == "Windows":
            python_cmd = os.path.join("venv", "Scripts", "python.exe")
        else:
            python_cmd = os.path.join("venv", "bin", "python")
        
        test_code = """
import pyautogui
import logging
print("✅ Core imports successful")
"""
        
        result = subprocess.run([python_cmd, "-c", test_code], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Installation test passed")
            return True
        else:
            print(f"❌ Installation test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys (OpenAI, Gemini, etc.)")
    print("2. Run Shadow AI:")
    print("   • Windows: double-click start.bat")
    print("   • Command line: python main.py")
    print("   • Voice mode: python main.py --voice")
    print("   • Demo mode: python main.py --demo")
    print()
    print("For help: python main.py --help")
    print()
    print("Enjoy using Shadow AI! 🚀")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Check optional dependencies
    check_optional_dependencies()
    
    # Run test
    if not run_test():
        print("⚠️  Installation completed but tests failed. You may need to install additional dependencies.")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
