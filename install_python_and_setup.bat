@echo off
echo.
echo ========================================
echo    Shadow AI - Complete Setup
echo ========================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script needs to run as Administrator to install Python.
    echo Please right-click on this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Checking for Python installation...

:: Check if Python is already installed
py --version >nul 2>&1
if %errorLevel% equ 0 (
    echo Python is already installed!
    py --version
    goto :install_dependencies
)

python --version >nul 2>&1
if %errorLevel% equ 0 (
    echo Python is already installed!
    python --version
    goto :install_dependencies
)

echo Python not found. Installing Python...

:: Download and install Python
echo Downloading Python 3.11...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}"

if not exist python-installer.exe (
    echo Failed to download Python installer!
    echo Please download Python manually from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python 3.11...
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Wait for installation to complete
timeout /t 10 /nobreak

:: Clean up installer
del python-installer.exe

:: Refresh PATH
call refreshenv

:install_dependencies
echo.
echo ========================================
echo    Installing Python Dependencies
echo ========================================
echo.

:: Upgrade pip first
py -m pip install --upgrade pip

:: Install dependencies one by one with error handling
echo Installing core dependencies...

echo Installing pyautogui...
py -m pip install pyautogui==0.9.54

echo Installing pynput...
py -m pip install pynput==1.7.6

echo Installing keyboard...
py -m pip install keyboard==0.13.5

echo Installing speech recognition...
py -m pip install SpeechRecognition==3.10.0

echo Installing pyttsx3...
py -m pip install pyttsx3==2.90

echo Installing openai...
py -m pip install openai==1.3.0

echo Installing google-generativeai...
py -m pip install google-generativeai==0.3.0

echo Installing requests...
py -m pip install requests==2.31.0

echo Installing selenium...
py -m pip install selenium==4.15.0

echo Installing webdriver-manager...
py -m pip install webdriver-manager==4.0.1

echo Installing python-docx...
py -m pip install python-docx==1.1.0

echo Installing PyPDF2...
py -m pip install PyPDF2==3.0.1

echo Installing reportlab...
py -m pip install reportlab==4.0.7

echo Installing Pillow...
py -m pip install Pillow==10.1.0

echo Installing beautifulsoup4...
py -m pip install beautifulsoup4==4.12.2

echo Installing lxml...
py -m pip install lxml==4.9.3

echo Installing python-dotenv...
py -m pip install python-dotenv==1.0.0

echo Installing schedule...
py -m pip install schedule==1.2.0

echo Installing psutil...
py -m pip install psutil==5.9.6

echo Installing colorama...
py -m pip install colorama==0.4.6

echo Installing flask...
py -m pip install flask==3.0.0

echo Installing flask-socketio...
py -m pip install flask-socketio==5.3.6

echo Installing pytest...
py -m pip install pytest==7.4.3

echo Installing pytest-mock...
py -m pip install pytest-mock==3.12.0

:: Windows-specific packages (might fail on some systems)
echo Installing Windows-specific packages...
py -m pip install pywin32==306
py -m pip install comtypes==1.2.0
py -m pip install pywinauto==0.6.8

:: Optional packages that might fail
echo Installing optional packages...
py -m pip install pyaudio 2>nul
py -m pip install customtkinter 2>nul
py -m pip install openai-whisper 2>nul

echo.
echo ========================================
echo    Creating Environment File
echo ========================================
echo.

:: Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file for API keys...
    echo # Shadow AI Configuration > .env
    echo # Add your API keys here >> .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
    echo OLLAMA_URL=http://localhost:11434 >> .env
    echo.
    echo .env file created! Please edit it with your API keys.
)

echo.
echo ========================================
echo    Testing Installation
echo ========================================
echo.

echo Testing Python installation...
py -c "import sys; print('Python version:', sys.version[:6])"

echo Testing key modules...
py -c "import pyautogui; print('✓ pyautogui')" 2>nul || echo "✗ pyautogui failed"
py -c "import pyttsx3; print('✓ pyttsx3')" 2>nul || echo "✗ pyttsx3 failed"
py -c "import speech_recognition; print('✓ speech_recognition')" 2>nul || echo "✗ speech_recognition failed"
py -c "import selenium; print('✓ selenium')" 2>nul || echo "✗ selenium failed"
py -c "import requests; print('✓ requests')" 2>nul || echo "✗ requests failed"

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Shadow AI is now ready to use!
echo.
echo To start Shadow AI:
echo   1. Edit .env file with your API keys (optional)
echo   2. Run: quick_start.bat
echo   3. Or run: py main.py
echo.
echo For help, run: py main.py help
echo.
pause
