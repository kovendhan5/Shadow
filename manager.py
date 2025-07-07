#!/usr/bin/env python3
"""
Shadow AI Manager
A comprehensive management script for Shadow AI Agent
"""

import os
import sys
import subprocess
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

class ShadowManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.python_exe = self.get_python_executable()
        self.config_file = self.project_root / "manager_config.json"
        self.load_config()
    
    def get_python_executable(self):
        """Get the correct Python executable"""
        if os.name == 'nt':  # Windows
            if self.venv_path.exists():
                return str(self.venv_path / "Scripts" / "python.exe")
            return "python"
        else:  # Unix/Linux/Mac
            if self.venv_path.exists():
                return str(self.venv_path / "bin" / "python")
            return "python3"
    
    def load_config(self):
        """Load manager configuration"""
        default_config = {
            "last_run": None,
            "run_count": 0,
            "preferred_mode": "interactive",
            "auto_update": True,
            "log_level": "INFO"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
    
    def save_config(self):
        """Save manager configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def check_installation(self):
        """Check if Shadow AI is properly installed"""
        print("🔍 Checking Shadow AI installation...")
        
        # Check Python
        try:
            result = subprocess.run([self.python_exe, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Python: {result.stdout.strip()}")
            else:
                print("❌ Python not found")
                return False
        except:
            print("❌ Python not accessible")
            return False
        
        # Check virtual environment
        if self.venv_path.exists():
            print("✅ Virtual environment: Found")
        else:
            print("⚠️  Virtual environment: Not found")
        
        # Check main files
        required_files = [
            "main.py", "config.py", "requirements.txt",
            "brain/gpt_agent.py", "control/desktop.py",
            "input/voice_input.py", "utils/logging.py"
        ]
        
        missing_files = []
        for file in required_files:
            if (self.project_root / file).exists():
                print(f"✅ {file}: Found")
            else:
                print(f"❌ {file}: Missing")
                missing_files.append(file)
        
        # Check .env file
        if (self.project_root / ".env").exists():
            print("✅ .env file: Found")
        else:
            print("⚠️  .env file: Not found (copy from .env.template)")
        
        # Check dependencies
        try:
            result = subprocess.run([self.python_exe, "-c", "import pyautogui; print('OK')"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Dependencies: Basic packages installed")
            else:
                print("❌ Dependencies: Missing packages")
                return False
        except:
            print("❌ Dependencies: Cannot check")
            return False
        
        return len(missing_files) == 0
    
    def install_dependencies(self):
        """Install or update dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            # Create virtual environment if it doesn't exist
            if not self.venv_path.exists():
                print("Creating virtual environment...")
                subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], 
                             check=True)
            
            # Upgrade pip
            subprocess.run([self.python_exe, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True)
            
            # Install requirements
            requirements_file = self.project_root / "requirements.txt"
            if requirements_file.exists():
                subprocess.run([self.python_exe, "-m", "pip", "install", "-r", 
                              str(requirements_file)], check=True)
                print("✅ Dependencies installed successfully")
                return True
            else:
                print("❌ requirements.txt not found")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def run_shadow(self, mode="interactive", args=None):
        """Run Shadow AI in specified mode"""
        print(f"🚀 Starting Shadow AI in {mode} mode...")
        
        # Update config
        self.config["last_run"] = datetime.now().isoformat()
        self.config["run_count"] += 1
        self.config["preferred_mode"] = mode
        self.save_config()
        
        # Prepare command
        cmd = [self.python_exe, "main.py"]
        
        if mode == "voice":
            cmd.append("--voice")
        elif mode == "demo":
            cmd.append("--demo")
        elif mode == "gui":
            cmd = [self.python_exe, "gui.py"]
        elif mode == "web":
            cmd = [self.python_exe, "web_interface.py"]
        
        if args:
            cmd.extend(args)
        
        try:
            # Change to project directory
            os.chdir(self.project_root)
            
            # Run Shadow AI
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running Shadow AI: {e}")
            return False
        except KeyboardInterrupt:
            print("\n👋 Shadow AI stopped by user")
            return True
        
        return True
    
    def run_tests(self):
        """Run the test suite"""
        print("🧪 Running tests...")
        
        try:
            # Check if pytest is installed
            subprocess.run([self.python_exe, "-c", "import pytest"], 
                         check=True, capture_output=True)
            
            # Run tests
            result = subprocess.run([self.python_exe, "-m", "pytest", "test_shadow.py", "-v"], 
                                  cwd=self.project_root)
            
            if result.returncode == 0:
                print("✅ All tests passed!")
                return True
            else:
                print("❌ Some tests failed")
                return False
        
        except subprocess.CalledProcessError:
            print("❌ pytest not installed. Installing...")
            subprocess.run([self.python_exe, "-m", "pip", "install", "pytest"], 
                         check=True)
            return self.run_tests()
    
    def show_status(self):
        """Show Shadow AI status"""
        print("📊 Shadow AI Status")
        print("=" * 40)
        
        # Basic info
        print(f"Project Root: {self.project_root}")
        print(f"Python Executable: {self.python_exe}")
        print(f"Virtual Environment: {'Yes' if self.venv_path.exists() else 'No'}")
        
        # Configuration
        print(f"\nConfiguration:")
        print(f"• Last Run: {self.config.get('last_run', 'Never')}")
        print(f"• Run Count: {self.config.get('run_count', 0)}")
        print(f"• Preferred Mode: {self.config.get('preferred_mode', 'interactive')}")
        print(f"• Auto Update: {self.config.get('auto_update', True)}")
        
        # File status
        print(f"\nFiles:")
        key_files = [".env", "main.py", "gui.py", "web_interface.py"]
        for file in key_files:
            status = "✅" if (self.project_root / file).exists() else "❌"
            print(f"• {file}: {status}")
        
        # Log files
        logs_dir = self.project_root / "logs"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            print(f"\nLog Files: {len(log_files)}")
            for log_file in log_files:
                size = log_file.stat().st_size
                print(f"• {log_file.name}: {size} bytes")
        
        # Tasks
        try:
            from task_manager import task_manager
            tasks = task_manager.list_tasks()
            print(f"\nTasks: {len(tasks)}")
            for task in tasks[-5:]:  # Show last 5 tasks
                print(f"• {task['name']}: {task['status']}")
        except:
            print("\nTasks: Unable to load")
    
    def clean_logs(self):
        """Clean log files"""
        print("🧹 Cleaning log files...")
        
        logs_dir = self.project_root / "logs"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            
            for log_file in log_files:
                try:
                    log_file.unlink()
                    print(f"✅ Deleted {log_file.name}")
                except Exception as e:
                    print(f"❌ Could not delete {log_file.name}: {e}")
            
            print(f"🧹 Cleaned {len(log_files)} log files")
        else:
            print("No log files found")
    
    def backup_config(self):
        """Backup configuration and important files"""
        print("💾 Creating backup...")
        
        backup_dir = self.project_root / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Files to backup
        backup_files = [
            ".env", "manager_config.json", "logs/shadow.log"
        ]
        
        backed_up = 0
        for file in backup_files:
            src = self.project_root / file
            if src.exists():
                dst = backup_dir / file
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    import shutil
                    shutil.copy2(src, dst)
                    backed_up += 1
                except Exception as e:
                    print(f"❌ Could not backup {file}: {e}")
        
        print(f"✅ Backed up {backed_up} files to {backup_dir}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🧠 Shadow AI Manager - Help

USAGE:
    python manager.py [command] [options]

COMMANDS:
    install     Install or update dependencies
    run         Run Shadow AI (default: interactive mode)
    test        Run the test suite
    status      Show current status
    clean       Clean log files
    backup      Backup configuration
    check       Check installation
    help        Show this help message

RUN MODES:
    --mode interactive  Interactive text mode (default)
    --mode voice        Voice input mode
    --mode gui          Graphical user interface
    --mode web          Web interface
    --mode demo         Demonstration mode

EXAMPLES:
    python manager.py install
    python manager.py run --mode voice
    python manager.py test
    python manager.py status
    python manager.py clean
    python manager.py backup

For more information, see DOCS.md
        """
        print(help_text)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Shadow AI Manager")
    parser.add_argument("command", nargs="?", default="run",
                       choices=["install", "run", "test", "status", "clean", "backup", "check", "help"],
                       help="Command to execute")
    parser.add_argument("--mode", default="interactive",
                       choices=["interactive", "voice", "gui", "web", "demo"],
                       help="Run mode for Shadow AI")
    parser.add_argument("--args", nargs="*", help="Additional arguments")
    
    args = parser.parse_args()
    
    manager = ShadowManager()
    
    if args.command == "install":
        if manager.install_dependencies():
            print("✅ Installation completed successfully!")
        else:
            print("❌ Installation failed!")
            sys.exit(1)
    
    elif args.command == "run":
        if not manager.check_installation():
            print("❌ Installation check failed. Run 'python manager.py install' first.")
            sys.exit(1)
        
        manager.run_shadow(args.mode, args.args)
    
    elif args.command == "test":
        manager.run_tests()
    
    elif args.command == "status":
        manager.show_status()
    
    elif args.command == "clean":
        manager.clean_logs()
    
    elif args.command == "backup":
        manager.backup_config()
    
    elif args.command == "check":
        if manager.check_installation():
            print("✅ Shadow AI is properly installed!")
        else:
            print("❌ Installation issues found!")
            sys.exit(1)
    
    elif args.command == "help":
        manager.show_help()
    
    else:
        print(f"Unknown command: {args.command}")
        manager.show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
