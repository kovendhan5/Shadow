#!/usr/bin/env python3
"""
Shadow AI Comprehensive Diagnostic Tool
Performs extensive system checks and provides detailed troubleshooting information
"""

import sys
import os
import platform
import subprocess
import importlib
import traceback
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
import json
from datetime import datetime

class ShadowAIDiagnostic:
    """Comprehensive diagnostic tool for Shadow AI"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "python_info": {},
            "dependencies": {},
            "project_structure": {},
            "configuration": {},
            "tests": {},
            "recommendations": []
        }
        self.issues = []
        self.warnings = []
    
    def run_full_diagnostic(self):
        """Run complete diagnostic suite"""
        print("🔍 Shadow AI Comprehensive Diagnostic Tool")
        print("=" * 50)
        
        diagnostic_steps = [
            ("System Information", self.check_system_info),
            ("Python Environment", self.check_python_environment),
            ("Project Structure", self.check_project_structure),
            ("Dependencies", self.check_dependencies),
            ("Configuration", self.check_configuration),
            ("Import Tests", self.test_imports),
            ("Functionality Tests", self.test_functionality),
            ("Performance Check", self.check_performance)
        ]
        
        for step_name, step_func in diagnostic_steps:
            print(f"\n🔍 {step_name}...")
            try:
                step_func()
                print(f"✅ {step_name} completed")
            except Exception as e:
                print(f"❌ {step_name} failed: {e}")
                self.issues.append(f"{step_name}: {e}")
        
        self.generate_report()
    
    def check_system_info(self):
        """Gather system information"""
        system_info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable": sys.executable,
            "working_directory": os.getcwd(),
            "user_home": str(Path.home()),
            "path_separator": os.pathsep,
            "environment_variables": {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
                "VIRTUAL_ENV": os.environ.get("VIRTUAL_ENV", ""),
            }
        }
        
        self.results["system_info"] = system_info
        
        # Print key information
        print(f"   OS: {system_info['platform']}")
        print(f"   Python: {system_info['python_version']} ({system_info['python_implementation']})")
        print(f"   Working Dir: {system_info['working_directory']}")
        
        # Check if running in virtual environment
        if system_info["environment_variables"]["VIRTUAL_ENV"]:
            print(f"   Virtual Env: ✅ {system_info['environment_variables']['VIRTUAL_ENV']}")
        else:
            print("   Virtual Env: ❌ Not detected")
            self.warnings.append("Not running in a virtual environment")
    
    def check_python_environment(self):
        """Check Python environment details"""
        python_info = {
            "version": sys.version,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro
            },
            "executable": sys.executable,
            "path": sys.path,
            "modules": list(sys.modules.keys()),
            "pip_version": self._get_pip_version(),
            "site_packages": self._get_site_packages_location()
        }
        
        self.results["python_info"] = python_info
        
        # Check Python version compatibility
        if sys.version_info < (3, 8):
            self.issues.append(f"Python version {sys.version_info.major}.{sys.version_info.minor} is too old. Requires 3.8+")
            print("   ❌ Python version too old (requires 3.8+)")
        else:
            print(f"   ✅ Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is compatible")
        
        print(f"   Pip version: {python_info['pip_version']}")
        print(f"   Site packages: {python_info['site_packages']}")
    
    def check_project_structure(self):
        """Check project structure and key files"""
        project_root = Path(__file__).parent
        
        expected_files = [
            "main.py",
            "config.py",
            "requirements.txt",
            ".env",
            "README.md",
            "setup.py"
        ]
        
        expected_dirs = [
            "brain",
            "control", 
            "gui",
            "input",
            "utils",
            "docs",
            "examples"
        ]
        
        structure_info = {
            "project_root": str(project_root),
            "files": {},
            "directories": {},
            "missing_files": [],
            "missing_directories": []
        }
        
        # Check files
        for file_name in expected_files:
            file_path = project_root / file_name
            if file_path.exists():
                structure_info["files"][file_name] = {
                    "exists": True,
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
                print(f"   ✅ {file_name}")
            else:
                structure_info["missing_files"].append(file_name)
                print(f"   ❌ {file_name} (missing)")
                if file_name in ["main.py", "config.py", "requirements.txt"]:
                    self.issues.append(f"Critical file missing: {file_name}")
        
        # Check directories
        for dir_name in expected_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                file_count = len(list(dir_path.glob("*")))
                structure_info["directories"][dir_name] = {
                    "exists": True,
                    "file_count": file_count
                }
                print(f"   ✅ {dir_name}/ ({file_count} files)")
            else:
                structure_info["missing_directories"].append(dir_name)
                print(f"   ❌ {dir_name}/ (missing)")
                if dir_name in ["brain", "control", "input"]:
                    self.issues.append(f"Critical directory missing: {dir_name}/")
        
        self.results["project_structure"] = structure_info
    
    def check_dependencies(self):
        """Check dependency availability and versions"""
        dependencies = {
            "core": [
                ("pyautogui", "Desktop automation"),
                ("logging", "Logging system"),
                ("json", "JSON processing"),
                ("pathlib", "Path handling"),
                ("subprocess", "Process management")
            ],
            "optional": [
                ("pyttsx3", "Text-to-speech"),
                ("speech_recognition", "Voice recognition"),
                ("selenium", "Web automation"),
                ("docx", "Document creation"),
                ("PIL", "Image processing"),
                ("colorama", "Terminal colors"),
                ("requests", "HTTP requests"),
                ("google.generativeai", "AI integration"),
                ("openai", "OpenAI integration"),
                ("flask", "Web interface"),
                ("customtkinter", "Modern GUI"),
                ("pywin32", "Windows integration")
            ]
        }
        
        dependency_results = {"core": {}, "optional": {}}
        
        # Check core dependencies
        print("   Core Dependencies:")
        for module, description in dependencies["core"]:
            status = self._check_module(module)
            dependency_results["core"][module] = status
            if status["available"]:
                print(f"     ✅ {module} - {description}")
            else:
                print(f"     ❌ {module} - {description} (CRITICAL)")
                self.issues.append(f"Critical dependency missing: {module}")
        
        # Check optional dependencies
        print("   Optional Dependencies:")
        available_count = 0
        for module, description in dependencies["optional"]:
            status = self._check_module(module)
            dependency_results["optional"][module] = status
            if status["available"]:
                print(f"     ✅ {module} - {description}")
                available_count += 1
            else:
                print(f"     ⚠️  {module} - {description} (fallback available)")
        
        print(f"   Optional: {available_count}/{len(dependencies['optional'])} available")
        
        if available_count < len(dependencies["optional"]) // 2:
            self.warnings.append("Many optional dependencies missing - functionality will be limited")
        
        self.results["dependencies"] = dependency_results
    
    def check_configuration(self):
        """Check configuration files and settings"""
        config_info = {
            "env_file": {},
            "config_module": {},
            "api_keys": {},
            "paths": {}
        }
        
        # Check .env file
        env_file = Path(".env")
        if env_file.exists():
            config_info["env_file"]["exists"] = True
            config_info["env_file"]["size"] = env_file.stat().st_size
            
            # Check for API key placeholders
            try:
                with open(env_file, 'r') as f:
                    env_content = f.read()
                
                api_keys = {
                    "OPENAI_API_KEY": "your_openai_key_here" not in env_content,
                    "GEMINI_API_KEY": "your_gemini_key_here" not in env_content,
                    "OLLAMA_URL": "http://localhost:11434" in env_content
                }
                
                config_info["api_keys"] = api_keys
                
                configured_keys = sum(api_keys.values())
                print(f"   ✅ .env file exists ({configured_keys}/3 API keys configured)")
                
                if configured_keys == 0:
                    self.warnings.append("No API keys configured - AI features will be limited")
                
            except Exception as e:
                print(f"   ⚠️  .env file exists but couldn't read: {e}")
                self.warnings.append(f"Could not read .env file: {e}")
        else:
            config_info["env_file"]["exists"] = False
            print("   ❌ .env file missing")
            self.issues.append(".env configuration file missing")
        
        # Check config.py module
        try:
            import config
            config_info["config_module"]["available"] = True
            config_attributes = [attr for attr in dir(config) if not attr.startswith('_')]
            config_info["config_module"]["attributes"] = config_attributes
            print(f"   ✅ config.py module ({len(config_attributes)} settings)")
        except ImportError as e:
            config_info["config_module"]["available"] = False
            config_info["config_module"]["error"] = str(e)
            print(f"   ❌ config.py module: {e}")
            self.issues.append(f"Could not import config module: {e}")
        
        self.results["configuration"] = config_info
    
    def test_imports(self):
        """Test importing key project modules"""
        modules_to_test = [
            "config",
            "brain.gpt_agent",
            "brain.universal_processor",
            "brain.universal_executor",
            "control.desktop",
            "input.text_input",
            "utils.logging",
            "utils.confirm"
        ]
        
        import_results = {}
        success_count = 0
        
        for module in modules_to_test:
            try:
                importlib.import_module(module)
                import_results[module] = {"success": True, "error": None}
                print(f"   ✅ {module}")
                success_count += 1
            except Exception as e:
                import_results[module] = {"success": False, "error": str(e)}
                print(f"   ❌ {module}: {e}")
                if "brain" in module or module == "config":
                    self.issues.append(f"Critical module import failed: {module}")
                else:
                    self.warnings.append(f"Module import failed: {module}")
        
        print(f"   Import Success: {success_count}/{len(modules_to_test)}")
        self.results["tests"]["imports"] = import_results
    
    def test_functionality(self):
        """Test basic functionality"""
        functionality_tests = {
            "basic_logging": self._test_logging,
            "config_loading": self._test_config,
            "desktop_controller": self._test_desktop_controller,
            "tts_system": self._test_tts
        }
        
        test_results = {}
        
        for test_name, test_func in functionality_tests.items():
            try:
                result = test_func()
                test_results[test_name] = {"success": True, "result": result}
                print(f"   ✅ {test_name}")
            except Exception as e:
                test_results[test_name] = {"success": False, "error": str(e)}
                print(f"   ❌ {test_name}: {e}")
                self.warnings.append(f"Functionality test failed: {test_name}")
        
        self.results["tests"]["functionality"] = test_results
    
    def check_performance(self):
        """Basic performance checks"""
        print("   Running basic performance tests...")
        
        performance_results = {}
        
        # Import time test
        start_time = time.time()
        try:
            import sys
            import os
            import json
        except:
            pass
        import_time = time.time() - start_time
        performance_results["import_time"] = import_time
        
        # File system test
        start_time = time.time()
        test_file = Path("temp_test.txt")
        try:
            test_file.write_text("test")
            test_file.unlink()
            fs_time = time.time() - start_time
            performance_results["filesystem_time"] = fs_time
        except Exception as e:
            performance_results["filesystem_error"] = str(e)
        
        print(f"   Import time: {import_time:.3f}s")
        if "filesystem_time" in performance_results:
            print(f"   Filesystem: {performance_results['filesystem_time']:.3f}s")
        
        self.results["tests"]["performance"] = performance_results
    
    def _check_module(self, module_name: str) -> Dict[str, Any]:
        """Check if a module is available and get its info"""
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            return {
                "available": True,
                "version": version,
                "location": getattr(module, '__file__', 'built-in')
            }
        except ImportError as e:
            return {
                "available": False,
                "error": str(e)
            }
    
    def _get_pip_version(self) -> str:
        """Get pip version"""
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "unknown"
        except:
            return "not available"
    
    def _get_site_packages_location(self) -> str:
        """Get site-packages location"""
        try:
            import site
            return str(site.getsitepackages()[0])
        except:
            return "unknown"
    
    def _test_logging(self) -> str:
        """Test logging functionality"""
        import logging
        logging.info("Test log message")
        return "Logging system functional"
    
    def _test_config(self) -> str:
        """Test config loading"""
        import config
        return f"Config loaded with {len([attr for attr in dir(config) if not attr.startswith('_')])} attributes"
    
    def _test_desktop_controller(self) -> str:
        """Test desktop controller"""
        from control.desktop import desktop_controller
        return f"Desktop controller initialized (screen: {desktop_controller.screen_width}x{desktop_controller.screen_height})"
    
    def _test_tts(self) -> str:
        """Test TTS system"""
        try:
            from utils.orpheus_tts import speak
            return "TTS system available"
        except:
            return "TTS using fallback"
    
    def generate_report(self):
        """Generate comprehensive diagnostic report"""
        print("\n" + "=" * 60)
        print("           🔍 SHADOW AI DIAGNOSTIC REPORT")
        print("=" * 60)
        
        # Summary
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        
        if total_issues == 0 and total_warnings == 0:
            print("🎉 EXCELLENT! No issues detected.")
            status = "EXCELLENT"
        elif total_issues == 0:
            print(f"✅ GOOD! {total_warnings} warnings found (no critical issues).")
            status = "GOOD"
        elif total_issues <= 2:
            print(f"⚠️  FAIR! {total_issues} issues and {total_warnings} warnings found.")
            status = "FAIR"
        else:
            print(f"❌ POOR! {total_issues} issues and {total_warnings} warnings found.")
            status = "POOR"
        
        self.results["summary"] = {
            "status": status,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "timestamp": datetime.now().isoformat()
        }
        
        # Print issues
        if self.issues:
            print(f"\n❌ Critical Issues ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        
        # Print warnings
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        # Recommendations
        self._generate_recommendations()
        if self.results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(self.results["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        # Save detailed report
        self._save_detailed_report()
        
        print("\n📄 Detailed report saved to: shadow_ai_diagnostic_report.json")
        print("=" * 60)
    
    def _generate_recommendations(self):
        """Generate recommendations based on findings"""
        recommendations = []
        
        # Dependency recommendations
        if any("missing" in issue.lower() for issue in self.issues):
            recommendations.append("Run 'pip install -r requirements.txt' to install missing dependencies")
        
        # Configuration recommendations
        if any(".env" in issue for issue in self.issues):
            recommendations.append("Create .env file and configure API keys for full functionality")
        
        # Python version recommendations
        if any("python version" in issue.lower() for issue in self.issues):
            recommendations.append("Upgrade to Python 3.8 or higher")
        
        # Virtual environment recommendations
        if "Not running in a virtual environment" in self.warnings:
            recommendations.append("Use a virtual environment: python -m venv venv && venv\\Scripts\\activate")
        
        # Performance recommendations
        if self.results.get("tests", {}).get("performance", {}).get("import_time", 0) > 5:
            recommendations.append("Slow import times detected - consider SSD storage or check antivirus settings")
        
        # General recommendations
        if len(self.warnings) > 5:
            recommendations.append("Consider running enhanced_installer.py for automated setup")
        
        self.results["recommendations"] = recommendations
    
    def _save_detailed_report(self):
        """Save detailed JSON report"""
        try:
            report_file = Path("shadow_ai_diagnostic_report.json")
            with open(report_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save detailed report: {e}")

def main():
    """Main diagnostic function"""
    try:
        diagnostic = ShadowAIDiagnostic()
        diagnostic.run_full_diagnostic()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnostic cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Diagnostic failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
