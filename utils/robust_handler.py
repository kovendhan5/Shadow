"""
Enhanced error handling and dependency management for Shadow AI
"""
import logging
import sys
import importlib
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path

class DependencyManager:
    """Manages dependencies and provides fallbacks for missing packages"""
    
    def __init__(self):
        self.available_packages = {}
        self.fallback_handlers = {}
        self.check_core_dependencies()
    
    def check_core_dependencies(self):
        """Check availability of core dependencies"""
        core_deps = {
            'pyautogui': self._check_pyautogui,
            'pyttsx3': self._check_pyttsx3,
            'speech_recognition': self._check_speech_recognition,
            'selenium': self._check_selenium,
            'docx': self._check_docx,
            'PIL': self._check_pillow,
            'win32gui': self._check_win32,
            'colorama': self._check_colorama,
            'requests': self._check_requests,
            'google.generativeai': self._check_genai
        }
        
        for package, checker in core_deps.items():
            self.available_packages[package] = checker()
    
    def _check_pyautogui(self) -> bool:
        """Check if pyautogui is available"""
        try:
            import pyautogui
            return True
        except ImportError:
            logging.warning("pyautogui not available - desktop automation may be limited")
            return False
    
    def _check_pyttsx3(self) -> bool:
        """Check if pyttsx3 is available"""
        try:
            import pyttsx3
            return True
        except ImportError:
            logging.warning("pyttsx3 not available - TTS will use Windows SAPI fallback")
            return False
    
    def _check_speech_recognition(self) -> bool:
        """Check if speech recognition is available"""
        try:
            import speech_recognition
            return True
        except ImportError:
            logging.warning("speech_recognition not available - voice input disabled")
            return False
    
    def _check_selenium(self) -> bool:
        """Check if selenium is available"""
        try:
            import selenium
            return True
        except ImportError:
            logging.warning("selenium not available - web automation may be limited")
            return False
    
    def _check_docx(self) -> bool:
        """Check if python-docx is available"""
        try:
            import docx
            return True
        except ImportError:
            logging.warning("python-docx not available - document creation limited to text files")
            return False
    
    def _check_pillow(self) -> bool:
        """Check if Pillow is available"""
        try:
            from PIL import Image
            return True
        except ImportError:
            logging.warning("Pillow not available - image processing may be limited")
            return False
    
    def _check_win32(self) -> bool:
        """Check if win32gui is available"""
        try:
            import win32gui
            return True
        except ImportError:
            logging.warning("win32gui not available - some Windows features may be limited")
            return False
    
    def _check_colorama(self) -> bool:
        """Check if colorama is available"""
        try:
            import colorama
            return True
        except ImportError:
            logging.warning("colorama not available - terminal colors disabled")
            return False
    
    def _check_requests(self) -> bool:
        """Check if requests is available"""
        try:
            import requests
            return True
        except ImportError:
            logging.warning("requests not available - web requests may fail")
            return False
    
    def _check_genai(self) -> bool:
        """Check if google.generativeai is available"""
        try:
            import google.generativeai
            return True
        except ImportError:
            logging.warning("google.generativeai not available - AI features will use fallbacks")
            return False
    
    def is_available(self, package: str) -> bool:
        """Check if a package is available"""
        return self.available_packages.get(package, False)
    
    def install_missing_package(self, package: str) -> bool:
        """Attempt to install a missing package"""
        try:
            logging.info(f"Attempting to install {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            # Re-check availability
            if package in ['pyautogui', 'pyttsx3', 'speech_recognition', 'selenium', 'python-docx', 'Pillow', 'pywin32', 'colorama', 'requests', 'google-generativeai']:
                self.check_core_dependencies()
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {package}: {e}")
            return False
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get a detailed status report of all dependencies"""
        return {
            "available": {k: v for k, v in self.available_packages.items() if v},
            "missing": {k: v for k, v in self.available_packages.items() if not v},
            "total_packages": len(self.available_packages),
            "available_count": sum(self.available_packages.values()),
            "missing_count": len(self.available_packages) - sum(self.available_packages.values())
        }

class SafeImporter:
    """Safe import utility with fallbacks"""
    
    def __init__(self, dependency_manager: DependencyManager):
        self.dep_manager = dependency_manager
    
    def safe_import(self, module_name: str, fallback_name: str = None, required: bool = False):
        """Safely import a module with optional fallback"""
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            if required:
                raise ImportError(f"Required module '{module_name}' not available: {e}")
            
            if fallback_name:
                try:
                    logging.warning(f"Module '{module_name}' not available, trying fallback '{fallback_name}'")
                    return importlib.import_module(fallback_name)
                except ImportError:
                    logging.error(f"Both '{module_name}' and fallback '{fallback_name}' not available")
            
            logging.warning(f"Module '{module_name}' not available, returning None")
            return None

class FallbackTTS:
    """Fallback text-to-speech using Windows SAPI"""
    
    def __init__(self):
        self.available = self._check_windows_sapi()
    
    def _check_windows_sapi(self) -> bool:
        """Check if Windows SAPI is available"""
        try:
            import os
            import platform
            return platform.system() == "Windows"
        except:
            return False
    
    def speak(self, text: str):
        """Speak text using Windows SAPI"""
        if not self.available:
            print(f"[SPEECH] {text}")
            return
        
        try:
            import os
            # Use PowerShell for Windows TTS
            escaped_text = text.replace("'", "''")  # Escape single quotes
            command = f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{escaped_text}\')"'
            os.system(command)
        except Exception as e:
            logging.error(f"Windows SAPI TTS failed: {e}")
            print(f"[SPEECH] {text}")

class FallbackVoiceInput:
    """Fallback voice input using simple text input"""
    
    def __init__(self):
        self.enabled = False
        logging.warning("Voice input not available, using text input fallback")
    
    def listen(self, prompt: str = None) -> str:
        """Fallback to text input"""
        if prompt:
            return input(f"{prompt}: ")
        else:
            return input("Enter command: ")

class RobustShadowAI:
    """Enhanced Shadow AI with robust error handling and fallbacks"""
    
    def __init__(self):
        self.dep_manager = DependencyManager()
        self.safe_importer = SafeImporter(self.dep_manager)
        self.setup_fallbacks()
        self.initialize_components()
    
    def setup_fallbacks(self):
        """Setup fallback systems for missing dependencies"""
        
        # TTS fallback
        if not self.dep_manager.is_available('pyttsx3'):
            self.tts = FallbackTTS()
        
        # Voice input fallback
        if not self.dep_manager.is_available('speech_recognition'):
            self.voice_input = FallbackVoiceInput()
        
        # GUI fallback
        if not self.dep_manager.is_available('customtkinter'):
            logging.warning("CustomTkinter not available, will use tkinter fallback")
    
    def initialize_components(self):
        """Initialize components with error handling"""
        try:
            # Import core modules with error handling
            self.setup_logging()
            self.setup_voice_systems()
            self.setup_automation()
            self.setup_ai_systems()
            
        except Exception as e:
            logging.error(f"Error initializing components: {e}")
            self.setup_minimal_fallback()
    
    def setup_logging(self):
        """Setup logging with fallbacks"""
        try:
            from utils.logging import setup_logging
            setup_logging()
        except ImportError:
            # Fallback logging setup
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler()]
            )
            logging.warning("Using fallback logging setup")
    
    def setup_voice_systems(self):
        """Setup voice systems with fallbacks"""
        try:
            if self.dep_manager.is_available('pyttsx3'):
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                logging.info("TTS engine initialized successfully")
            else:
                self.tts_engine = FallbackTTS()
                logging.info("Using fallback TTS")
        except Exception as e:
            logging.error(f"TTS setup failed: {e}")
            self.tts_engine = FallbackTTS()
    
    def setup_automation(self):
        """Setup automation with fallbacks"""
        try:
            if self.dep_manager.is_available('pyautogui'):
                import pyautogui
                pyautogui.PAUSE = 0.5
                pyautogui.FAILSAFE = True
                self.automation_available = True
                logging.info("PyAutoGUI initialized successfully")
            else:
                self.automation_available = False
                logging.warning("Desktop automation not available")
        except Exception as e:
            logging.error(f"Automation setup failed: {e}")
            self.automation_available = False
    
    def setup_ai_systems(self):
        """Setup AI systems with fallbacks"""
        try:
            if self.dep_manager.is_available('google.generativeai'):
                from config import GEMINI_API_KEY
                if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_key_here":
                    import google.generativeai as genai
                    genai.configure(api_key=GEMINI_API_KEY)
                    self.ai_available = True
                    logging.info("AI system initialized successfully")
                else:
                    self.ai_available = False
                    logging.warning("AI API key not configured")
            else:
                self.ai_available = False
                logging.warning("AI system not available, using pattern-based processing")
        except Exception as e:
            logging.error(f"AI system setup failed: {e}")
            self.ai_available = False
    
    def setup_minimal_fallback(self):
        """Setup minimal fallback system"""
        logging.warning("Setting up minimal fallback system")
        self.tts_engine = FallbackTTS()
        self.automation_available = False
        self.ai_available = False
    
    def speak(self, text: str):
        """Speak text with fallback handling"""
        try:
            if hasattr(self.tts_engine, 'say'):
                # pyttsx3 engine
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Fallback TTS
                self.tts_engine.speak(text)
        except Exception as e:
            logging.error(f"TTS error: {e}")
            print(f"[SPEECH] {text}")
    
    def get_dependency_status(self) -> str:
        """Get formatted dependency status"""
        status = self.dep_manager.get_status_report()
        
        report = f"""
Shadow AI Dependency Status:
============================
Available: {status['available_count']}/{status['total_packages']} packages
Missing: {status['missing_count']} packages

✅ Available Packages:
{chr(10).join(f"  • {pkg}" for pkg in status['available'].keys())}

❌ Missing Packages:
{chr(10).join(f"  • {pkg}" for pkg in status['missing'].keys())}

Core Systems Status:
• Desktop Automation: {'✅ Available' if self.automation_available else '❌ Limited'}
• AI Processing: {'✅ Available' if self.ai_available else '❌ Fallback mode'}
• Text-to-Speech: {'✅ Available' if hasattr(self.tts_engine, 'say') else '❌ Fallback mode'}
"""
        return report
    
    def install_missing_dependencies(self) -> bool:
        """Attempt to install missing dependencies"""
        status = self.dep_manager.get_status_report()
        missing = list(status['missing'].keys())
        
        if not missing:
            logging.info("No missing dependencies to install")
            return True
        
        # Map package names to pip package names
        pip_packages = {
            'pyautogui': 'pyautogui',
            'pyttsx3': 'pyttsx3',
            'speech_recognition': 'SpeechRecognition',
            'selenium': 'selenium',
            'docx': 'python-docx',
            'PIL': 'Pillow',
            'win32gui': 'pywin32',
            'colorama': 'colorama',
            'requests': 'requests',
            'google.generativeai': 'google-generativeai'
        }
        
        success_count = 0
        for package in missing:
            pip_name = pip_packages.get(package, package)
            if self.dep_manager.install_missing_package(pip_name):
                success_count += 1
        
        logging.info(f"Successfully installed {success_count}/{len(missing)} missing packages")
        return success_count == len(missing)

# Global instance
robust_shadow = RobustShadowAI()

def get_robust_shadow() -> RobustShadowAI:
    """Get the robust Shadow AI instance"""
    return robust_shadow

def check_and_report_dependencies():
    """Check dependencies and return a report"""
    return robust_shadow.get_dependency_status()

def install_missing_dependencies():
    """Install missing dependencies"""
    return robust_shadow.install_missing_dependencies()


