@echo off
title Shadow AI - Ultra Modern GUI Launcher

echo.
echo 🤖 Shadow AI Ultra Modern Interface
echo 🎨 Beautiful • 🚀 Fast • 💻 Powerful
echo ===============================================
echo.

REM Navigate to the project directory
cd /d "%~dp0"

echo 📁 Current Directory: %CD%
echo 🐍 Python Path: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8 or higher.
    echo 💡 Download from: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

echo.
echo 🔧 Installing/checking dependencies...
python -m pip install --upgrade pip
python -m pip install customtkinter pillow psutil requests pyautogui

echo.
echo 🎨 Launching Ultra Modern GUI...
echo.

REM Launch the ultra modern GUI
python gui\ultra_modern_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error launching GUI!
    echo 💡 Trying alternative launcher...
    python launch_ultra_modern_gui.py
)

echo.
echo 👋 Shadow AI GUI closed.
pause
