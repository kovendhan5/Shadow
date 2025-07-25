@echo off
title Shadow AI - Practical Features Launcher

echo.
echo 🚀 Shadow AI - Practical Features
echo ===============================================
echo 📝 Real Notepad Integration • 🚀 App Launcher • ⌨️ Text Automation
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo 📁 Working Directory: %CD%
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python from python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

echo 🔧 Installing dependencies for practical features...
python -m pip install --quiet pyautogui customtkinter pillow >nul 2>&1

echo 🚀 Launching Practical Features GUI...
echo.
echo 💡 Features available:
echo    📝 Open Notepad and write articles automatically
echo    🚀 Launch applications (Calculator, Paint, Browser, etc.)
echo    ⌨️ Type text to any active window
echo    📄 Generate articles on any topic
echo.

REM Launch the practical GUI
python gui\practical_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error launching Practical GUI!
    echo 💡 Trying fallback...
    python gui\beautiful_gui.py
)

echo.
echo 👋 Practical Features GUI closed.
pause
