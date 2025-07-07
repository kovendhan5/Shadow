# 📖 Shadow AI Agent - Complete Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Modules](#modules)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Development](#development)
10. [Contributing](#contributing)

## Introduction

Shadow AI Agent is a comprehensive personal automation assistant for Windows that accepts natural language commands and performs complex multi-step tasks. It combines the power of AI language models with system automation to create a truly intelligent desktop assistant.

### Key Features

- **Natural Language Understanding**: Processes commands in plain English
- **Multi-Modal Input**: Supports both voice and text input
- **Desktop Automation**: Controls applications, windows, and user interface
- **Browser Automation**: Automates web browsing and online tasks
- **Document Creation**: Generates professional documents and reports
- **Task Management**: Handles complex multi-step workflows
- **Safety Features**: Confirmation prompts and comprehensive logging

## Installation

### Prerequisites

- Windows 10 or later
- Python 3.8 or higher
- Internet connection for AI model access

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shadow-ai.git
cd shadow-ai

# Run the setup script
python setup.py

# Or install manually
pip install -r requirements.txt
```

### Manual Installation Steps

1. **Install Python Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment Variables**:

   ```bash
   copy .env.template .env
   # Edit .env with your API keys
   ```

3. **Install Browser Drivers** (for web automation):

   - Chrome: Download ChromeDriver
   - Firefox: Download GeckoDriver
   - Edge: Usually pre-installed

4. **Configure Microphone** (for voice input):
   - Grant microphone permissions
   - Test with `python -c "import speech_recognition; print('OK')"`

## Configuration

### Environment Variables (.env)

```env
# AI Provider Configuration
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
OLLAMA_URL=http://localhost:11434

# Email Configuration
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password

# Additional APIs
FLIPKART_API_KEY=your_flipkart_key
NAUKRI_API_KEY=your_naukri_key
```

### Configuration Options (config.py)

```python
# LLM Provider
DEFAULT_LLM_PROVIDER = "gemini"  # "openai", "gemini", "ollama"

# Voice Settings
VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"
VOICE_TIMEOUT = 5

# Safety Settings
REQUIRE_CONFIRMATION = True
CONFIRMATION_TIMEOUT = 30

# Browser Settings
DEFAULT_BROWSER = "chrome"
HEADLESS_MODE = False

# Document Settings
DEFAULT_DOC_FORMAT = "docx"
SAVE_LOCATION = "~/Desktop"
```

## Usage

### Command Line Interface

```bash
# Interactive mode
python main.py

# Voice mode
python main.py --voice

# Single command
python main.py "open notepad"

# Demo mode
python main.py --demo
```

### Graphical Interface

```bash
# Launch GUI
python gui.py
```

### Web Interface

```bash
# Launch web interface
python web_interface.py
```

### Startup Script (Windows)

```bash
# Use the startup script
start.bat
```

## Modules

### Brain Module (`brain/`)

**Purpose**: AI processing and command understanding

**Files**:

- `gpt_agent.py`: Main AI agent with LLM integration

**Key Functions**:

- `process_command(command)`: Parse natural language commands
- `GPTAgent.generate_response()`: Generate AI responses
- AI provider support (OpenAI, Gemini, Ollama)

### Control Module (`control/`)

**Purpose**: System automation and control

**Files**:

- `desktop.py`: Desktop automation using PyAutoGUI
- `browser.py`: Web browser automation using Selenium
- `documents.py`: Document creation and manipulation

**Key Functions**:

- Desktop: `open_application()`, `type_text()`, `click_at()`
- Browser: `navigate_to()`, `search_product()`, `click_element()`
- Documents: `create_document()`, `generate_leave_letter()`

### Input Module (`input/`)

**Purpose**: Handle user input (voice and text)

**Files**:

- `voice_input.py`: Voice recognition and text-to-speech
- `text_input.py`: Text input with GUI support

**Key Functions**:

- Voice: `get_voice_input()`, `speak_response()`
- Text: `get_text_input()`, `confirm_action()`

### Utils Module (`utils/`)

**Purpose**: Utility functions and helpers

**Files**:

- `logging.py`: Logging configuration
- `confirm.py`: User confirmation system

**Key Functions**:

- `setup_logging()`: Configure logging
- `confirm_action()`: Get user confirmation

## API Reference

### ShadowAI Class

```python
class ShadowAI:
    def __init__(self)
    def run_interactive(self)
    def run_single_command(self, command: str) -> bool
    def process_ai_command(self, command: str)
    def execute_action(self, action_data: Dict[str, Any]) -> bool
```

### DesktopController Class

```python
class DesktopController:
    def open_application(self, app_name: str) -> bool
    def type_text(self, text: str) -> bool
    def click_at(self, x: int, y: int) -> bool
    def take_screenshot(self, filename: str = None) -> str
    def press_key(self, key: str) -> bool
```

### BrowserController Class

```python
class BrowserController:
    def navigate_to(self, url: str) -> bool
    def search_product(self, site: str, product: str) -> bool
    def click_element(self, selector: str) -> bool
    def type_in_element(self, selector: str, text: str) -> bool
```

### DocumentController Class

```python
class DocumentController:
    def create_document(self, content: str, title: str, format: str) -> str
    def generate_leave_letter(self, reason: str, date: str) -> str
    def open_word(self, filepath: str = None) -> bool
```

### TaskManager Class

```python
class TaskManager:
    def create_task(self, name: str, description: str) -> Task
    def execute_task(self, task_id: str) -> bool
    def get_task_progress(self, task_id: str) -> Dict[str, Any]
    def cancel_task(self, task_id: str) -> bool
```

## Examples

### Basic Commands

```python
# Desktop automation
shadow.run_single_command("open notepad")
shadow.run_single_command("type: Hello World")
shadow.run_single_command("take a screenshot")

# Document creation
shadow.run_single_command("write a leave letter for tomorrow")
shadow.run_single_command("create a resume template")

# Web automation
shadow.run_single_command("search for iPhone on Flipkart")
shadow.run_single_command("open gmail")
```

### Voice Commands

```python
# Enable voice mode
shadow.voice_mode = True

# Get voice input
command = get_voice_input("What would you like me to do?")

# Speak response
speak_response("Task completed successfully!")
```

### Complex Workflows

```python
# Create a task
task = task_manager.create_task("Job Application", "Apply for software developer position")

# Add steps
task_manager.add_step(task.id, "Create resume", "create_resume", {})
task_manager.add_step(task.id, "Search jobs", "search_jobs", {"site": "naukri"})
task_manager.add_step(task.id, "Upload resume", "upload_resume", {}, confirmation_required=True)

# Execute task
task_manager.execute_task(task.id)
```

## Troubleshooting

### Common Issues

**1. Voice Recognition Not Working**

```bash
# Check microphone permissions
# Install pyaudio
pip install pyaudio

# Test microphone
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('Microphone OK')"
```

**2. Browser Automation Fails**

```bash
# Install browser drivers
# For Chrome: Download ChromeDriver
# For Firefox: Download GeckoDriver
# Add to PATH or place in project directory
```

**3. Document Creation Errors**

```bash
# Install Microsoft Office or LibreOffice
# Check file permissions
# Install required packages
pip install python-docx reportlab
```

**4. AI Model Not Responding**

```bash
# Check API keys in .env file
# Verify internet connection
# Test with simple command
python main.py "open notepad"
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose output
python main.py --debug
```

### Log Files

- Main log: `logs/shadow.log`
- Error log: `logs/error.log`
- Task log: `logs/tasks.log`

## Development

### Project Structure

```
shadow/
├── main.py              # Main application
├── config.py            # Configuration
├── task_manager.py      # Task management
├── gui.py              # GUI interface
├── web_interface.py    # Web interface
├── brain/              # AI processing
├── control/            # System control
├── input/              # Input handling
├── utils/              # Utilities
├── examples/           # Example scripts
├── tests/              # Test files
└── docs/              # Documentation
```

### Adding New Features

**1. Add New Command Type**

```python
# In brain/gpt_agent.py
SYSTEM_PROMPT += """
- new_task_type: action1, action2, action3
"""

# In main.py
def execute_new_action(self, action: str, parameters: Dict[str, Any]) -> bool:
    # Implementation here
    pass
```

**2. Add New Control Module**

```python
# Create control/new_module.py
class NewController:
    def __init__(self):
        pass

    def new_action(self, params):
        # Implementation
        pass

# Import in main.py
from control.new_module import NewController
```

**3. Add New Input Method**

```python
# Create input/new_input.py
def get_new_input():
    # Implementation
    pass

# Integrate in main.py
```

### Testing

```bash
# Run all tests
python -m pytest test_shadow.py -v

# Run specific test
python -m pytest test_shadow.py::TestDesktopController -v

# Run with coverage
pip install pytest-cov
python -m pytest test_shadow.py --cov=. --cov-report=html
```

### Code Style

```bash
# Install formatting tools
pip install black flake8

# Format code
black *.py

# Check style
flake8 *.py
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Run tests to ensure everything works

### Making Changes

1. Create a feature branch
2. Make your changes
3. Add tests for new features
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

### Code Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write tests for new features
- Update documentation

### Pull Request Process

1. Ensure tests pass
2. Update README if needed
3. Add entry to CHANGELOG
4. Request review from maintainers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/shadow-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/shadow-ai/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/yourusername/shadow-ai/wiki)
- **Email**: support@shadow-ai.com

## Changelog

### v1.0.0 (2024-07-07)

- Initial release
- Basic voice and text input
- Desktop automation
- Browser automation
- Document creation
- Task management
- GUI and web interfaces
