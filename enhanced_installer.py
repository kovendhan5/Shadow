#!/usr/bin/env python3
"""
Shadow AI Enhanced Installer and Dependency Manager
Automatically sets up the environment and installs all required dependencies
"""

import os
import sys
import subprocess
import platform
import time
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

class ShadowAIInstaller:
    """Enhanced installer for Shadow AI with comprehensive dependency management"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.python_executable = None
        self.pip_executable = None
        self.errors = []
        self.warnings = []
        
    def print_header(self):
        """Print installation header"""
        print("\n" + "=" * 60)
        print("     🧠 Shadow AI - Enhanced Installer & Setup")
        print("=" * 60)
        print("🚀 Preparing to install Shadow AI and all dependencies...")
        print("📍 Project Location:", self.project_root)
        print("🐍 Python Version:", platform.python_version())
        print("💻 Operating System:", platform.system(), platform.release())
        print("=" * 60 + "\n")
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        print("🔍 Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8 or higher is required!")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            print("   Please install Python 3.8+ from https://python.org/downloads/")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    
    def setup_virtual_environment(self) -> bool:
        """Create and setup virtual environment"""
        print("\n🏗️  Setting up virtual environment...")
        
        try:
            if self.venv_path.exists():
                print("📁 Virtual environment already exists")
                response = input("   Do you want to recreate it? (y/N): ").lower()
                if response in ['y', 'yes']:
                    print("🗑️  Removing existing virtual environment...")
                    import shutil
                    shutil.rmtree(self.venv_path)
                else:
                    print("✅ Using existing virtual environment")
                    self._set_python_paths()
                    return True
            
            # Create virtual environment
            print("📦 Creating new virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], 
                          check=True, capture_output=True)
            
            self._set_python_paths()
            
            # Upgrade pip in virtual environment
            print("⬆️  Upgrading pip...")
            subprocess.run([self.pip_executable, 'install', '--upgrade', 'pip'], 
                          check=True, capture_output=True)
            
            print("✅ Virtual environment created successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to create virtual environment: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error creating virtual environment: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
    
    def _set_python_paths(self):
        """Set Python and pip executable paths for virtual environment"""
        if platform.system() == "Windows":
            self.python_executable = str(self.venv_path / "Scripts" / "python.exe")
            self.pip_executable = str(self.venv_path / "Scripts" / "pip.exe")
        else:
            self.python_executable = str(self.venv_path / "bin" / "python")
            self.pip_executable = str(self.venv_path / "bin" / "pip")
    
    def install_base_dependencies(self) -> bool:
        """Install base dependencies first"""
        print("\n📋 Installing base dependencies...")
        
        base_packages = [
            'wheel',
            'setuptools',
            'pip-tools',
            'colorama',  # For colored terminal output
        ]
        
        success = True
        for package in base_packages:
            try:
                print(f"📦 Installing {package}...")
                subprocess.run([self.pip_executable, 'install', package], 
                              check=True, capture_output=True)
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                error_msg = f"Failed to install {package}: {e}"
                print(f"❌ {error_msg}")
                self.warnings.append(error_msg)
                success = False
        
        return success
    
    def install_requirements(self) -> bool:
        """Install dependencies from requirements.txt"""
        print("\n📋 Installing project dependencies from requirements.txt...")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            error_msg = "requirements.txt not found!"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
        
        try:
            # Install requirements with timeout and better error handling
            print("⏳ This may take a few minutes...")
            result = subprocess.run([
                self.pip_executable, 'install', '-r', str(requirements_file), 
                '--timeout', '300', '--retries', '3'
            ], capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                print("✅ All dependencies installed successfully!")
                return True
            else:
                print("⚠️  Some dependencies failed to install:")
                print(result.stderr)
                self.warnings.append(f"Dependency installation warnings: {result.stderr}")
                
                # Try installing problematic packages individually
                return self._install_problematic_packages_individually()
                
        except subprocess.TimeoutExpired:
            error_msg = "Installation timed out after 10 minutes"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
        except Exception as e:
            error_msg = f"Failed to install requirements: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
    
    def _install_problematic_packages_individually(self) -> bool:
        """Install known problematic packages with special handling"""
        print("\n🔧 Installing problematic packages individually...")
        
        # Packages that often need special handling
        special_packages = {
            'pyaudio': self._install_pyaudio,
            'pywin32': self._install_pywin32,
            'pyttsx3': self._install_pyttsx3,
        }
        
        success = True
        for package, installer in special_packages.items():
            try:
                print(f"🔧 Installing {package} with special handling...")
                if installer():
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"⚠️  {package} installation had issues")
                    success = False
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")
                self.warnings.append(f"Failed to install {package}: {e}")
                success = False
        
        return success
    
    def _install_pyaudio(self) -> bool:
        """Install PyAudio with Windows-specific handling"""
        try:
            if platform.system() == "Windows":
                # Try pipwin first for Windows
                try:
                    subprocess.run([self.pip_executable, 'install', 'pipwin'], check=True, capture_output=True)
                    subprocess.run([self.pip_executable, 'install', 'pyaudio'], check=True, capture_output=True)
                    return True
                except:
                    # Fallback to regular pip
                    subprocess.run([self.pip_executable, 'install', 'pyaudio'], check=True, capture_output=True)
                    return True
            else:
                subprocess.run([self.pip_executable, 'install', 'pyaudio'], check=True, capture_output=True)
                return True
        except:
            return False
    
    def _install_pywin32(self) -> bool:
        """Install pywin32"""
        try:
            subprocess.run([self.pip_executable, 'install', 'pywin32'], check=True, capture_output=True)
            return True
        except:
            return False
    
    def _install_pyttsx3(self) -> bool:
        """Install pyttsx3"""
        try:
            subprocess.run([self.pip_executable, 'install', 'pyttsx3'], check=True, capture_output=True)
            return True
        except:
            return False
    
    def verify_installation(self) -> bool:
        """Verify that critical packages are installed and working"""
        print("\n🧪 Verifying installation...")
        
        critical_imports = [
            ('pyautogui', 'Desktop automation'),
            ('config', 'Configuration module'),
            ('pathlib', 'Path handling'),
            ('json', 'JSON processing'),
            ('logging', 'Logging system'),
        ]
        
        optional_imports = [
            ('pyttsx3', 'Text-to-speech'),
            ('speech_recognition', 'Voice recognition'),
            ('selenium', 'Web automation'),
            ('PIL', 'Image processing'),
            ('colorama', 'Terminal colors'),
            ('requests', 'HTTP requests'),
        ]
        
        # Test critical imports
        success = True
        for module, description in critical_imports:
            if self._test_import(module, description, critical=True):
                print(f"✅ {description} - OK")
            else:
                print(f"❌ {description} - FAILED")
                success = False
        
        # Test optional imports
        optional_count = 0
        for module, description in optional_imports:
            if self._test_import(module, description, critical=False):
                print(f"✅ {description} - OK")
                optional_count += 1
            else:
                print(f"⚠️  {description} - Not available (will use fallback)")
        
        print(f"\n📊 Installation Summary:")
        print(f"   Critical components: {'All working' if success else 'Some failed'}")
        print(f"   Optional components: {optional_count}/{len(optional_imports)} available")
        
        return success
    
    def _test_import(self, module_name: str, description: str, critical: bool = False) -> bool:
        """Test importing a module"""
        try:
            result = subprocess.run([
                self.python_executable, '-c', f'import {module_name}'
            ], capture_output=True, timeout=10)
            return result.returncode == 0
        except Exception:
            if critical:
                self.errors.append(f"Critical module {module_name} failed to import")
            return False
    
    def setup_configuration(self) -> bool:
        """Setup initial configuration"""
        print("\n⚙️  Setting up configuration...")
        
        env_file = self.project_root / ".env"
        if env_file.exists():
            print("✅ Configuration file (.env) already exists")
            return True
        
        # Create basic .env file if it doesn't exist
        env_content = """# Shadow AI Configuration
# Replace placeholder values with your actual API keys

# AI API Keys (get free keys from the respective providers)
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
OLLAMA_URL=http://localhost:11434

# Voice Settings
VOICE_ENABLED=True

# Safety Settings
REQUIRE_CONFIRMATION=True

# Email Settings (optional)
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Web Interface
FLASK_SECRET_KEY=your-secret-key-here
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ Configuration file created")
            print("📝 Edit .env file to add your API keys for full functionality")
            return True
        except Exception as e:
            error_msg = f"Failed to create configuration file: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            return False
    
    def create_launcher_scripts(self) -> bool:
        """Create convenient launcher scripts"""
        print("\n🚀 Creating launcher scripts...")
        
        try:
            # Windows batch file
            if platform.system() == "Windows":
                batch_content = f'''@echo off
echo Starting Shadow AI...
cd /d "{self.project_root}"
"{self.python_executable}" main.py %*
pause
'''
                batch_file = self.project_root / "shadow_ai.bat"
                with open(batch_file, 'w') as f:
                    f.write(batch_content)
                print("✅ Windows launcher created: shadow_ai.bat")
            
            # Python launcher script
            launcher_content = f'''#!/usr/bin/env python3
"""
Shadow AI Launcher
Auto-activates virtual environment and starts Shadow AI
"""
import os
import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent
venv_python = r"{self.python_executable}"

if __name__ == "__main__":
    os.chdir(project_root)
    subprocess.run([venv_python, "main.py"] + sys.argv[1:])
'''
            launcher_file = self.project_root / "launch_shadow.py"
            with open(launcher_file, 'w') as f:
                f.write(launcher_content)
            print("✅ Python launcher created: launch_shadow.py")
            
            return True
        except Exception as e:
            error_msg = f"Failed to create launcher scripts: {e}"
            print(f"❌ {error_msg}")
            self.warnings.append(error_msg)
            return False
    
    def test_basic_functionality(self) -> bool:
        """Test basic Shadow AI functionality"""
        print("\n🧪 Testing basic functionality...")
        
        test_script = '''
try:
    import sys
    sys.path.insert(0, ".")
    
    # Test basic imports
    from utils.robust_handler import get_robust_shadow
    
    # Test initialization
    shadow = get_robust_shadow()
    
    # Test dependency status
    status = shadow.get_dependency_status()
    print("Dependency check completed")
    
    # Test basic TTS
    shadow.speak("Shadow AI installation test successful")
    
    print("BASIC_TEST_PASSED")
except Exception as e:
    print(f"BASIC_TEST_FAILED: {e}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                self.python_executable, '-c', test_script
            ], capture_output=True, text=True, timeout=30, cwd=self.project_root)
            
            if "BASIC_TEST_PASSED" in result.stdout:
                print("✅ Basic functionality test passed")
                return True
            else:
                print("❌ Basic functionality test failed")
                print("Output:", result.stdout)
                print("Errors:", result.stderr)
                return False
                
        except Exception as e:
            error_msg = f"Failed to run basic functionality test: {e}"
            print(f"❌ {error_msg}")
            self.warnings.append(error_msg)
            return False
    
    def run_full_installation(self) -> bool:
        """Run the complete installation process"""
        self.print_header()
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Virtual Environment Setup", self.setup_virtual_environment),
            ("Base Dependencies", self.install_base_dependencies),
            ("Project Dependencies", self.install_requirements),
            ("Installation Verification", self.verify_installation),
            ("Configuration Setup", self.setup_configuration),
            ("Launcher Scripts", self.create_launcher_scripts),
            ("Functionality Test", self.test_basic_functionality),
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            try:
                if step_func():
                    success_count += 1
                    print(f"✅ {step_name} completed successfully")
                else:
                    print(f"❌ {step_name} failed")
            except Exception as e:
                print(f"❌ {step_name} failed with exception: {e}")
                self.errors.append(f"{step_name}: {e}")
        
        # Print final report
        self.print_final_report(success_count, len(steps))
        
        return success_count == len(steps)
    
    def print_final_report(self, success_count: int, total_steps: int):
        """Print final installation report"""
        print("\n" + "=" * 60)
        print("           🎉 SHADOW AI INSTALLATION COMPLETE")
        print("=" * 60)
        
        if success_count == total_steps:
            print("🎉 SUCCESS! Shadow AI has been installed successfully!")
            print("\n🚀 Next Steps:")
            print("   1. Edit .env file to add your API keys for full functionality")
            print("   2. Run Shadow AI using one of these methods:")
            print(f"      • Double-click: shadow_ai.bat (Windows)")
            print(f"      • Command line: python launch_shadow.py")
            print(f"      • Direct: {self.python_executable} main.py")
            print("\n💡 Tips:")
            print("   • Get free API keys from:")
            print("     - Google Gemini: https://ai.google.dev/")
            print("     - OpenAI: https://platform.openai.com/")
            print("   • Check docs/ folder for detailed documentation")
            print("   • Run with --help for command line options")
        else:
            print(f"⚠️  Installation completed with issues ({success_count}/{total_steps} steps successful)")
            print("\n❌ Errors encountered:")
            for error in self.errors:
                print(f"   • {error}")
            
            if self.warnings:
                print("\n⚠️  Warnings:")
                for warning in self.warnings:
                    print(f"   • {warning}")
            
            print("\n🔧 Troubleshooting:")
            print("   • Check your internet connection")
            print("   • Make sure you have admin privileges")
            print("   • Try running: pip install --upgrade pip")
            print("   • Check Python version (3.8+ required)")
        
        print("=" * 60)

def main():
    """Main installation function"""
    installer = ShadowAIInstaller()
    
    try:
        success = installer.run_full_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Installation failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
