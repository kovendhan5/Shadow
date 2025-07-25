# 🤖 Shadow AI - Advanced Desktop Automation & AI Assistant

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Security](https://img.shields.io/badge/Security-Audited-green.svg)](docs/SECURITY_AUDIT_FINAL.md)

Shadow AI is a cutting-edge desktop automation system that combines artificial intelligence with practical computer control capabilities. It features enhanced modules for file management, system monitoring, web search, and much more - all controlled through natural language commands.

## 🚀 Enhanced Features (NEW!)

### 📁 **Advanced File Management**
- **Smart Organization**: Automatically organize files by type, date, or size
- **Intelligent Cleanup**: Find and remove duplicate files, temporary files
- **Backup System**: Create automated backups with compression
- **Large File Detection**: Quickly find files consuming disk space
- **Batch Operations**: Copy, move, rename multiple files efficiently

### 🌐 **Multi-Engine Web Search**
- **10+ Search Engines**: Google, Bing, Yahoo, DuckDuckGo, YouTube, and more
- **Specialized Searches**: News, tutorials, product prices, academic papers
- **Quick Access**: Instant search from voice or text commands
- **Smart Suggestions**: Context-aware search recommendations

### 💻 **System Diagnostics & Monitoring**
- **Real-time Monitoring**: CPU, memory, disk, and network usage
- **Health Checks**: Automated system health assessments
- **Process Management**: View and manage running applications
- **Performance Reports**: Detailed system performance analysis
- **Alerts**: Notifications for system issues

### 🔔 **Cross-Platform Notifications**
- **Smart Alerts**: Desktop notifications with rich content
- **Multiple Backends**: Windows Toast, macOS Notification Center, Linux notifications
- **Scheduled Notifications**: Set reminders and alerts
- **Status Updates**: Real-time feedback on task completion

### 📋 **Advanced Clipboard Management**
- **History Tracking**: Remember everything you copy
- **Smart Search**: Find clipboard items by content
- **Persistent Storage**: Clipboard history survives restarts
- **Format Support**: Text, images, files, and more

### 🔥 **Customizable Hotkey System**
- **Global Shortcuts**: System-wide keyboard shortcuts
- **Action Binding**: Bind any Shadow AI command to hotkeys
- **Usage Statistics**: Track hotkey usage and optimize workflow
- **Easy Configuration**: Simple setup and management

## 🎯 Core Features

- **🗣️ Voice & Text Commands**: Natural language interaction
- **🖱️ Desktop Automation**: Mouse, keyboard, and screen control
- **🌐 Browser Automation**: Web navigation and interaction
- **📄 Document Processing**: Create, edit, and manage documents
- **🧠 AI-Powered Context**: Intelligent command understanding
- **🔄 Cross-Platform**: Windows, macOS, and Linux support
- **🎮 Demo Mode**: Interactive demonstrations
- **📊 Comprehensive Logging**: Detailed activity tracking

## ⚡ Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/kovendhan5/Shadow.git
cd Shadow

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch Shadow AI
```bash
# Interactive mode with enhanced features
python main.py

# Voice interaction mode
python main.py --voice

# Single command execution
python main.py --command "organize Downloads folder by type"

# Demo mode
python main.py --demo
```

### 3. Test Enhanced Features
```bash
# Run comprehensive feature test
python test_enhanced_features.py

# Interactive demo of new features
python demo_enhanced.py
```

## 🎮 Usage Examples

### Enhanced File Management
```bash
"organize Downloads folder by type"
"find large files over 100MB"
"create backup of Documents folder"
"clean temporary files older than 7 days"
"copy all PDF files from Desktop to Documents"
```

### Smart Web Search
```bash
"search Google for Python tutorials"
"search YouTube for machine learning"
"search news about artificial intelligence"
"search StackOverflow for async programming"
"find product prices for laptop"
```

### System Monitoring
```bash
"show system information"
"check system health"
"generate system report"
"show running processes"
"monitor CPU usage"
```

### Clipboard & Productivity
```bash
"copy this text to clipboard"
"show clipboard history"
"paste from clipboard"
"search clipboard for python"
```

### Hotkeys & Automation
```bash
"show hotkey help"
"list all hotkeys"
"show hotkey statistics"
```

### Classic Desktop Automation
```bash
"open Notepad and type hello world"
"take a screenshot"
"click on the start button"
"search for weather on Google"
"open calculator"
```

## 🛠️ Configuration

### Basic Configuration (`config.py`)
```python
# Voice settings
VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"

# Enhanced features
ENABLE_FILE_MANAGER = True
ENABLE_WEB_SEARCH = True
ENABLE_SYSTEM_MONITOR = True
ENABLE_NOTIFICATIONS = True
ENABLE_CLIPBOARD = True
ENABLE_HOTKEYS = True

# API Keys (optional)
OPENAI_API_KEY = "your-key-here"
```

### Advanced Settings
- **File Management**: Custom organization rules, backup locations
- **Web Search**: Default search engines, custom search URLs
- **System Monitoring**: Alert thresholds, monitoring intervals
- **Notifications**: Display duration, sound settings
- **Hotkeys**: Custom key combinations, action mappings

## 📦 Module Structure

```
Shadow/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── control/               # Core control modules
│   ├── file_manager.py    # 📁 Enhanced file operations
│   ├── web_search.py      # 🌐 Multi-engine web search
│   ├── system_info.py     # 💻 System diagnostics
│   ├── notifications.py   # 🔔 Cross-platform notifications
│   ├── clipboard_manager.py # 📋 Advanced clipboard
│   ├── hotkey_manager.py  # 🔥 Hotkey system
│   ├── desktop.py         # 🖱️ Desktop automation
│   ├── browser.py          # 🌐 Browser control
│   └── documents.py       # 📄 Document processing
├── brain/                 # AI and processing
│   ├── gpt_agent.py       # 🧠 GPT integration
│   ├── orpheus_ai.py      # 🎭 Advanced AI
│   └── universal_processor.py # 🔄 Command processing
├── gui/                   # Graphical interfaces
├── demos/                 # Example scripts
├── tests/                 # Test suites
└── docs/                  # Documentation
```

## 🧪 Testing

### Run All Tests
```bash
# Quick functionality test
python quick_test.py

# Enhanced features test
python test_enhanced_features.py

# GUI tests
python test_gui_simple.py

# System integration test
python system_test_comprehensive.py
```

### Test Coverage
- ✅ Enhanced feature imports
- ✅ Main application integration
- ✅ Individual module functionality
- ✅ Command processing
- ✅ Error handling
- ✅ Cross-platform compatibility

## 🔧 Requirements

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for AI features

### Python Dependencies
```
psutil>=5.8.0          # System monitoring
requests>=2.25.0       # Web requests
pyperclip>=1.8.0       # Clipboard operations
keyboard>=0.13.0       # Hotkey detection
pynput>=1.7.0          # Input simulation
win10toast>=0.9        # Windows notifications
plyer>=2.0             # Cross-platform notifications
pillow>=8.0.0          # Image processing
pyautogui>=0.9.52      # GUI automation
speech_recognition>=3.8.1  # Voice recognition
pyttsx3>=2.90          # Text-to-speech
```

### Optional Dependencies
```
openai>=0.27.0         # GPT integration
selenium>=4.0.0        # Advanced browser automation
opencv-python>=4.5.0   # Computer vision
pytesseract>=0.3.8     # OCR capabilities
```

## 🚀 Launcher Scripts

Choose your preferred way to launch Shadow AI:

### Windows
```batch
# Quick launch with GUI
launch_improved.bat

# Modern launcher
launch_modern.py

# Ultra-modern with all features
launch_ultra_modern.py

# Start immediately
start_now.bat
```

### Cross-Platform
```bash
# Python launchers work on all platforms
python launch_modern.py
python simple_launcher.py
```

## 📈 Performance

### Benchmarks
- **Startup Time**: < 3 seconds
- **Command Processing**: < 500ms average
- **Memory Usage**: 50-100MB typical
- **CPU Usage**: < 5% idle, < 20% active

### Optimization Features
- **Lazy Loading**: Modules loaded on demand
- **Caching**: Frequently used data cached
- **Background Processing**: Non-blocking operations
- **Resource Cleanup**: Automatic memory management

## 🛡️ Security

### Security Features
- **Local Processing**: Core features work offline
- **Data Privacy**: No sensitive data transmitted
- **Safe Execution**: Sandboxed command execution
- **Access Control**: Permission-based operations

### Best Practices
- Keep API keys secure in environment variables
- Review commands before execution in sensitive environments
- Use voice mode in private spaces only
- Regular security updates

## 🎨 GUI Collection

Shadow AI includes multiple GUI interfaces:

- **Modern GUI** (`gui_modern.py`): Clean, professional interface
- **Cyberpunk GUI** (`gui_cyberpunk.py`): Futuristic, neon-themed
- **Premium GUI** (`gui_premium.py`): Feature-rich, polished
- **Ultra GUI** (`gui_ultra.py`): Maximum functionality
- **Minimal GUI** (`gui_minimal.py`): Lightweight, essential features

Launch any GUI:
```bash
python gui/gui_modern.py
python launchers/launch_cyberpunk.bat
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Fork the repository
git clone https://github.com/yourusername/Shadow.git
cd Shadow

# Create development environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .
```

### Contribution Areas
- 🆕 New automation modules
- 🔧 Platform-specific optimizations
- 🎨 GUI improvements
- 📖 Documentation enhancements
- 🧪 Test coverage expansion
- 🌐 Internationalization

## 📝 Changelog

### Version 2.0 (July 2025) - Enhanced Features Release
- ✨ **NEW**: Advanced File Management System
- ✨ **NEW**: Multi-Engine Web Search
- ✨ **NEW**: System Diagnostics & Monitoring
- ✨ **NEW**: Cross-Platform Notifications
- ✨ **NEW**: Advanced Clipboard Management
- ✨ **NEW**: Customizable Hotkey System
- 🔧 Enhanced main application integration
- 📚 Comprehensive documentation update
- 🧪 Expanded test coverage

### Version 1.5
- 🎨 Multiple GUI interfaces
- 🧠 Improved AI processing
- 🔄 Universal command processor
- 📱 Web interface

### Version 1.0
- 🗣️ Voice command support
- 🖱️ Basic desktop automation
- 🌐 Browser control
- 📄 Document processing

## 🆘 Support

### Getting Help
- 📖 Check the [Documentation](docs/)
- 🐛 Report issues on [GitHub Issues](https://github.com/kovendhan5/Shadow/issues)
- 💬 Join discussions in [GitHub Discussions](https://github.com/kovendhan5/Shadow/discussions)

### Common Issues
- **Import Errors**: Ensure all dependencies are installed
- **Permission Issues**: Run as administrator on Windows
- **Voice Recognition**: Check microphone permissions
- **Feature Not Working**: Run `test_enhanced_features.py` to diagnose

### Troubleshooting
```bash
# Verify installation
python test_enhanced_features.py

# Check system compatibility
python system_test_comprehensive.py

# Test specific features
python demo_enhanced.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Thanks to the open-source community for excellent libraries
- Inspired by the vision of accessible AI automation
- Built with ❤️ for productivity enthusiasts

---

<div align="center">

**🤖 Shadow AI - Where Automation Meets Intelligence 🚀**

*Made with ❤️ by [kovendhan5](https://github.com/kovendhan5)*

[⭐ Star on GitHub](https://github.com/kovendhan5/Shadow) • [🐛 Report Bug](https://github.com/kovendhan5/Shadow/issues) • [💡 Request Feature](https://github.com/kovendhan5/Shadow/issues)

</div>
