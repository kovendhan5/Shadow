# Shadow AI Project Setup Guide

This document provides a comprehensive guide to setting up and running the Shadow AI project.

## 📋 Setup Steps

1. **Environment Setup**
   - Create a Python virtual environment: `python -m venv venv`
   - Activate the environment: 
     - Windows: `venv\Scripts\activate`
     - Linux/Mac: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

2. **API Key Configuration**
   - The `.env` file already exists but needs to be configured
   - Replace placeholder API keys with your actual keys
   - At minimum, you'll need a Google Gemini API key (free at https://ai.google.dev/)

3. **Launch Options**
   - `quick_start.bat` - Simple launcher for beginners
   - `launch_improved_new.bat` - Advanced launcher with environment setup
   - `launch.bat` - Original launcher with all options
   - Direct command line: `python main.py`

## 🔍 Troubleshooting Common Issues

1. **Missing Dependencies**
   - Run `python quick_check.py` to check basic functionality
   - For voice input issues: `pip install pyaudio` (may require `pipwin install pyaudio` on Windows)
   - For GUI issues: `pip install customtkinter pillow`

2. **API Key Problems**
   - Make sure your API keys are correctly formatted in `.env`
   - Check for extra spaces or quotes around the API key
   - If you don't have a key, the system will use fallback functionality

3. **Python Version**
   - Shadow AI requires Python 3.8 or newer
   - Check your version with `python --version`

4. **Windows-Specific Issues**
   - For text-to-speech issues, try reinstalling: `pip uninstall pyttsx3 && pip install pyttsx3`
   - For automation issues, make sure you're not running in a restricted environment

## 🚀 Testing the Installation

1. **Basic Functionality Test**
   - Run `python quick_check.py` to check if core components work

2. **Command Line Test**
   - Run `python simple_test.py` to test Shadow AI's core functionality
   
3. **Import Test**
   - Run `python test_imports.py` to check if all modules import correctly

## 📋 Project Structure Overview

- `main.py` - Main entry point for Shadow AI
- `config.py` - Configuration settings (API keys, paths, etc.)
- `brain/` - AI processing modules (GPT agent, universal processor, etc.)
- `control/` - System control modules (desktop, browser, documents)
- `gui/` - Various GUI implementations (working, premium, cyberpunk, etc.)
- `input/` - User input handling (text input, voice input)
- `utils/` - Utility functions (logging, TTS, etc.)

## 🎯 Next Steps

After successful setup:
1. Try running different GUIs to find your preferred interface
2. Test voice commands if your system supports microphone input
3. Explore the examples in `demos/` directory
4. Review documentation in `docs/` for advanced features

---

For any issues not covered here, check the detailed documentation in the `docs/` directory or open an issue on the repository.
