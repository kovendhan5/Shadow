## # 🧠 Shadow AI Agent

> Your Personal AI Assistant for Windows - Automate tasks with natural language commands

Shadow is a powerful AI agent that accepts voice or text commands and performs multi-step tasks on your Windows machine. Think of it as your personal Copilot that can buy products, write documents, reply to emails, upload resumes, and much more!

## 🌟 Features

- **Natural Language Processing**: Understands voice and text commands
- **Multi-Modal Input**: Support for both voice and text input
- **Desktop Automation**: Control applications, click, type, and navigate
- **Browser Automation**: Search products, navigate websites, fill forms
- **Document Creation**: Generate letters, resumes, and reports
- **Safety First**: Confirmation prompts for sensitive actions
- **Comprehensive Logging**: All actions are logged for transparency

## 🚀 Quick Start

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

4. **Run Shadow AI**:
   ```bash
   python main.py
   ```

### First Run

When you first run Shadow, you'll see a welcome screen with available commands:

```
┌─────────────────────────────────────────────────────────────┐
│                    🧠 Shadow AI Agent                       │
│                Your Personal AI Assistant                   │
│                                                             │
│  Available commands:                                        │
│  • Voice: Say your command naturally                       │
│  • Text: Type your command                                  │
│  • Examples:                                                │
│    - "Open notepad and type hello world"                   │
│    - "Write a leave letter for tomorrow"                   │
│    - "Search for iPhone on Flipkart"                       │
│    - "Take a screenshot"                                    │
│                                                             │
│  Commands: help, quit, voice, text, demo                   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Usage Examples

### Basic Commands

```bash
# Interactive mode
python main.py

# Single command mode
python main.py "open notepad"

# Voice mode
python main.py --voice

# Run demonstration
python main.py --demo
```

### Voice Commands

- **"Open notepad"** - Opens Notepad application
- **"Write a leave letter for tomorrow due to health reasons"** - Creates a leave letter
- **"Search for iPhone on Flipkart"** - Opens Flipkart and searches for iPhone
- **"Take a screenshot"** - Captures screen and saves to desktop
- **"Create a resume template"** - Generates a professional resume template

### Text Commands

You can also type commands directly:

- `open calculator`
- `type: Hello World`
- `click at 500, 300`
- `search for laptop on amazon`

## 🛠️ Configuration

### Environment Variables

Create a `.env` file from the template:

```env
# AI Provider (choose one)
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
OLLAMA_URL=http://localhost:11434

# Email (for email automation)
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
```

### Settings

Modify `config.py` to customize behavior:

```python
# LLM Configuration
DEFAULT_LLM_PROVIDER = "gemini"  # "openai", "gemini", "ollama"

# Safety settings
REQUIRE_CONFIRMATION = True
CONFIRMATION_TIMEOUT = 30

# Voice settings
VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"
```

## 🏗️ Architecture

```
shadow/
├── main.py              # Main application entry point
├── config.py            # Configuration and settings
├── requirements.txt     # Python dependencies
├── .env.template        # Environment variables template
├── input/              # Input handling modules
│   ├── voice_input.py  # Voice recognition and TTS
│   └── text_input.py   # Text input and GUI
├── brain/              # AI processing
│   └── gpt_agent.py    # LLM integration and command processing
├── control/            # System control modules
│   ├── desktop.py      # Desktop automation
│   ├── browser.py      # Web browser automation
│   └── documents.py    # Document creation and manipulation
├── utils/              # Utility modules
│   ├── logging.py      # Logging configuration
│   └── confirm.py      # User confirmation system
└── logs/               # Log files
    └── shadow.log      # Application logs
```

## 🧩 Modules

### Input System

- **Voice Input**: Uses speech recognition for natural voice commands
- **Text Input**: CLI and GUI text input with confirmation dialogs
- **Multi-modal**: Seamlessly switch between voice and text

### Brain (AI Processing)

- **GPT Integration**: OpenAI GPT-4 support
- **Gemini Support**: Google Gemini AI integration
- **Local LLM**: Ollama support for local models
- **Command Understanding**: Natural language to structured actions

### Control Systems

- **Desktop Control**: PyAutoGUI for mouse/keyboard automation
- **Browser Control**: Selenium for web automation
- **Document Control**: Word, PDF, and text document creation

### Safety & Logging

- **Confirmation System**: User approval for sensitive actions
- **Comprehensive Logging**: All actions logged with timestamps
- **Error Handling**: Graceful error recovery and reporting

## 📋 Use Cases

### Document Creation

```python
# Voice: "Write a leave letter for tomorrow due to health reasons"
# Creates: Leave_Letter_20240707_143022.docx on desktop
```

### Web Automation

```python
# Voice: "Search for iPhone 15 on Flipkart"
# Actions: Opens browser → Navigates to Flipkart → Searches for iPhone 15
```

### Desktop Tasks

```python
# Voice: "Open calculator and take a screenshot"
# Actions: Opens Calculator → Takes screenshot → Saves to desktop
```

### File Operations

```python
# Voice: "Create a resume template with my name John Doe"
# Creates: Resume_Template_20240707_143022.docx
```

## 🔧 Development

### Adding New Commands

1. **Add to GPT Agent** (`brain/gpt_agent.py`):

   ```python
   # Add new action types to SYSTEM_PROMPT
   "new_task_type": "action_name, another_action"
   ```

2. **Implement in Control Module**:

   ```python
   def execute_new_action(self, action: str, parameters: Dict[str, Any]) -> bool:
       # Implementation here
       pass
   ```

3. **Add to Main Executor** (`main.py`):
   ```python
   elif task_type == 'new_task_type':
       return self.execute_new_action(action, parameters)
   ```

### Testing

Run the demo mode to test basic functionality:

```bash
python main.py --demo
```

### Debugging

Enable verbose logging by modifying `utils/logging.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security & Privacy

### Safety Features

- **Confirmation Required**: Sensitive actions require user approval
- **Action Logging**: All actions are logged for audit purposes
- **Timeout Protection**: Actions timeout to prevent hanging
- **Error Handling**: Graceful failure without system damage

### Privacy

- **Local Processing**: Most operations happen locally
- **Optional Cloud**: LLM calls can be local (Ollama) or cloud-based
- **No Data Storage**: No personal data stored unless explicitly saved
- **Transparent Logging**: All actions are logged and visible

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

1. **Voice Recognition Not Working**:

   - Check microphone permissions
   - Install pyaudio: `pip install pyaudio`
   - Run microphone test: `python -c "import speech_recognition as sr; print('Microphone working!')"`

2. **Browser Automation Fails**:

   - Install browser drivers (ChromeDriver, GeckoDriver)
   - Check browser version compatibility
   - Ensure browser is properly installed

3. **Document Creation Errors**:
   - Install Microsoft Office or LibreOffice
   - Check file permissions in Desktop folder
   - Verify python-docx installation

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/shadow-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shadow-ai/discussions)
- **Email**: your.email@example.com

## 🎉 Acknowledgments

- OpenAI for GPT API
- Google for Gemini API
- Selenium WebDriver team
- PyAutoGUI developers
- Speech Recognition library contributors

---

**Made with ❤️ by the Shadow AI Team** listens to your voice or text, understands what you want, and takes action on your Windows machine — from opening apps to automating workflows.
