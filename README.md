# 🧠 Shadow AI - Universal Personal Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Audited](https://img.shields.io/badge/Security-Audited-green.svg)](docs/SECURITY_AUDIT_FINAL.md)

> **Transform your computer into an intelligent AI companion that understands and executes any task through natural language commands.**

Shadow AI is a powerful, secure, and feature-rich personal AI assistant for Windows that combines advanced natural language processing with desktop automation, emotional intelligence, and beautiful user interfaces.

## ✨ Quick Start

### 🚀 Super Easy Setup (Recommended)

1. **One-Command Setup:**
   ```bash
   # Run the enhanced installer (handles everything automatically)
   python enhanced_installer.py
   ```
   
   The installer will:
   - ✅ Check your Python version
   - ✅ Create a virtual environment
   - ✅ Install all dependencies
   - ✅ Set up configuration files
   - ✅ Test the installation
   - ✅ Create convenient launchers

2. **Launch Shadow AI:**
   - **Windows:** Double-click `quick_start.bat`
   - **Any OS:** `python launch_shadow.py`
   - **Direct:** Use the created launchers

### 🛠️ Manual Setup (Alternative)

If you prefer manual setup:

1. **Environment Setup:**
   ```bash
   # Install Python 3.8+ if not already installed
   # https://www.python.org/downloads/

   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure API Keys:**
   - Edit the `.env` file (or create from template)
   - Add your API key: `GEMINI_API_KEY=your_actual_api_key_here`
   - Get free keys from: https://ai.google.dev/

3. **Launch Options:**
   - `quick_start.bat` - Enhanced launcher with dependency checks
   - `launch_improved_new.bat` - Full launcher with environment setup
   - `python main.py` - Direct command line launch
   - `python diagnostic.py` - Run system diagnostics

### 🔍 Troubleshooting

**Quick Fix:** Run the diagnostic tool first:
```bash
python diagnostic.py
```

**Common Issues:**
1. **Missing Dependencies:** Run `python enhanced_installer.py`
2. **Python Too Old:** Install Python 3.8+ from python.org
3. **Import Errors:** Activate virtual environment: `venv\Scripts\activate`
4. **API Issues:** Configure keys in `.env` file
5. **Permission Errors:** Run as administrator (Windows) or with sudo (Linux)

**Get Help:**
- Check `shadow_ai_diagnostic_report.json` after running diagnostics
- Review logs in the `logs/` directory
- See detailed docs in `docs/` folder

## 🌟 Key Features

### 🎨 **4 Fully Functional GUIs** ✅

- **Working** - Simple, reliable tkinter interface ✅
- **Premium** - Elegant glassmorphism design with advanced features ✅
- **Cyberpunk** - Futuristic neon-themed interface with animations ✅
- **Modern** - Clean CustomTkinter interface ✅
- **Ultra, Enhanced, Orpheus** - Coming soon (placeholders available)

### 🧠 **AI Capabilities**

- **Natural Language Processing** - Speak or type commands naturally
- **Universal Task Execution** - Handles ANY computer task
- **Emotional Intelligence** - Understands and responds to emotions
- **Context Awareness** - Remembers conversation history

### 🚀 **Automation Features**

- **Desktop Control** - Applications, windows, keyboard/mouse
- **Document Creation** - Letters, reports, presentations
- **Web Automation** - Browsing, searching, form filling
- **File Management** - Create, organize, manipulate files

## 💬 Example Commands

```
"Open notepad and write an article about AI"
"Take a screenshot and save it to Desktop"
"Search for the best laptops under $1000"
"I'm feeling stressed, can you help?" (Orpheus mode)
"Create a leave letter for tomorrow"
```

## 📁 Project Structure

```
Shadow AI/
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── launch.bat          # Main launcher
├── start.bat           # Command line launcher
├── brain/              # AI processing modules
├── control/            # System control modules
├── gui/                # User interface options
├── input/              # Voice & text input handling
├── utils/              # Utility functions
├── demos/              # Demo and example scripts
├── tests/              # Test suite
├── launchers/          # GUI launchers
├── docs/               # Documentation
└── examples/           # Usage examples
```

## 🛡️ Security & Privacy

✅ **Fully Audited** - Comprehensive security review completed  
✅ **No Data Collection** - All processing happens locally  
✅ **Secure API Handling** - Proper encryption and key management  
✅ **Privacy First** - Your data never leaves your computer

## 📚 Documentation

- **[Complete Documentation](docs/DOCS.md)** - Detailed setup and usage guide
- **[GUI Collection](docs/GUI_COLLECTION_README.md)** - All GUI options explained
- **[Orpheus Guide](docs/ORPHEUS_COMPLETE_GUIDE.md)** - Emotional AI documentation
- **[Security Audit](docs/SECURITY_AUDIT_FINAL.md)** - Security review results

## 🧪 Testing

```bash
# Run basic tests
python tests/test_gpt_agent.py

# Test specific features
python tests/test_notepad_task.py
python tests/test_orpheus.py

# Demo the system
python demos/demo.py
python examples/basic_usage.py
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the [docs/](docs/) folder
- **Examples**: See [examples/](examples/) and [demos/](demos/)

---

**Ready to transform your computer experience?** Clone the repo and launch your first GUI in under 5 minutes! 🚀
