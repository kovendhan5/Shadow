# 🧠 Shadow AI Agent

> Your Personal AI Assistant for Windows - Automate tasks with natural language commands

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-GPT%20%7C%20Gemini%20%7C%20Ollama-purple.svg)](https://github.com/yourusername/shadow-ai)
[![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://windows.microsoft.com)

Shadow is a powerful AI agent that accepts voice or text commands and performs multi-step tasks on your Windows machine. Think of it as your personal AI assistant that can write documents, browse the web, automate desktop tasks, and much more!

## 🌟 Features

### 🎯 **Core Capabilities**

- **Natural Language Processing**: Understands voice and text commands
- **Multi-Modal Input**: Support for both voice and text input
- **Desktop Automation**: Control applications, click, type, and navigate
- **Browser Automation**: Navigate websites, search, fill forms
- **Document Creation**: Generate letters, resumes, and reports
- **Smart Window Management**: Works with existing windows (no new window spam!)

### 🛡️ **Safety & Security**

- **Confirmation Prompts**: User approval for sensitive actions
- **Comprehensive Logging**: All actions logged for transparency
- **Secure API Management**: Environment-based configuration
- **Input Validation**: Safe command processing

### 🖥️ **Interfaces**

- **Command Line**: Single commands or interactive mode
- **Voice Mode**: Natural speech recognition
- **GUI**: Tkinter-based desktop interface
- **Web Interface**: Browser-based control panel

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.11+
- Microphone (for voice commands)
- Internet connection (for AI features)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/shadow-ai.git
   cd shadow-ai
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**:

   ```bash
   copy .env.template .env
   # Edit .env file with your API keys
   ```

4. **Get API Keys**:

   - **Google Gemini**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **OpenAI** (optional): Visit [OpenAI API](https://platform.openai.com/api-keys)

5. **Run Shadow AI**:
   ```bash
   python main.py
   ```

## 🎯 Usage Examples

### **Basic Commands**

```bash
# Interactive mode
python main.py

# Single command
python main.py "open notepad"

# Voice mode
python main.py --voice

# Demo mode
python main.py --demo
```

### **Smart Text Generation**

```bash
# Write articles directly in Notepad
python main.py "write an article about artificial intelligence"

# Create documents
python main.py "write a leave letter for tomorrow"

# Simple typing
python main.py "type: Hello from Shadow AI!"
```

### **Desktop Automation**

```bash
# Take screenshots
python main.py "take a screenshot"

# Open applications
python main.py "open calculator"

# Control mouse and keyboard
python main.py "click at 500, 300"
```

### **Voice Commands**

Just say naturally:

- _"Open notepad and write about machine learning"_
- _"Take a screenshot of my desktop"_
- _"Search for laptops on Amazon"_
- _"Create a resume template"_

## 🏗️ Architecture

```
shadow-ai/
├── 🧠 brain/              # AI processing & LLM integration
│   └── gpt_agent.py       # GPT/Gemini/Ollama support
├── 🎮 control/            # System control modules
│   ├── desktop.py         # Desktop automation
│   ├── browser.py         # Web automation
│   └── documents.py       # Document creation
├── 🎙️ input/              # Input handling
│   ├── voice_input.py     # Speech recognition & TTS
│   └── text_input.py      # Text & GUI input
├── 🛠️ utils/              # Utilities
│   ├── logging.py         # Logging system
│   └── confirm.py         # User confirmation
├── 📄 main.py             # Main application
├── ⚙️ config.py           # Configuration
└── 🌐 web_interface.py    # Web interface
```

## 🔧 Configuration

### **Environment Variables**

Copy `.env.template` to `.env` and configure:

```env
# AI Provider (choose one)
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
OLLAMA_URL=http://localhost:11434

# Email (for automation)
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Web Interface
FLASK_SECRET_KEY=your-secret-key-here
```

### **Supported AI Models**

- **Google Gemini**: `gemini-1.5-flash` (default)
- **OpenAI GPT**: `gpt-4`, `gpt-3.5-turbo`
- **Ollama**: Local models (llama3, etc.)

## 📋 Use Cases

### **Content Creation**

- Write articles, letters, emails
- Generate professional documents
- Create templates and forms

### **Desktop Automation**

- Open applications and files
- Control mouse and keyboard
- Take screenshots and recordings

### **Web Automation**

- Navigate websites
- Search for products
- Fill forms and submit data

### **Voice Control**

- Hands-free operation
- Natural language commands
- Text-to-speech feedback

## 🔐 Security

### **Built-in Security Features**

- ✅ No hardcoded API keys
- ✅ Environment-based configuration
- ✅ Safe command processing
- ✅ Input validation and sanitization
- ✅ Secure error handling
- ✅ Confirmation for sensitive actions

### **Best Practices**

- Keep API keys secure
- Regularly rotate credentials
- Review automation logs
- Use confirmation prompts

## 🧪 Testing

```bash
# Run test suite
python -m pytest test_shadow.py -v

# Quick functionality test
python test_functionality.py

# Interactive testing
python main.py --demo
```

## 🚀 Deployment

### **Local Usage**

1. Install dependencies
2. Configure API keys
3. Run `python main.py`

### **Web Interface**

1. Install Flask dependencies
2. Run `python web_interface.py`
3. Open browser to `http://localhost:5000`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Common Issues**

- **Voice not working**: Check microphone permissions
- **Commands not recognized**: Ensure AI API keys are configured
- **Browser automation fails**: Install/update browser drivers

### **Getting Help**

- 📖 [Documentation](DOCS.md)
- 🐛 [Issues](https://github.com/yourusername/shadow-ai/issues)
- 💬 [Discussions](https://github.com/yourusername/shadow-ai/discussions)

## 🎉 Acknowledgments

- OpenAI for GPT API
- Google for Gemini API
- Selenium WebDriver team
- PyAutoGUI developers
- The open-source community

---

**Made with ❤️ for automation enthusiasts**

_Shadow AI listens to your voice or text, understands what you want, and takes action on your Windows machine — from opening apps to creating documents to automating complex workflows._

[![GitHub stars](https://img.shields.io/github/stars/yourusername/shadow-ai?style=social)](https://github.com/yourusername/shadow-ai)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/shadow-ai?style=social)](https://github.com/yourusername/shadow-ai)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/shadow-ai)](https://github.com/yourusername/shadow-ai/issues)
