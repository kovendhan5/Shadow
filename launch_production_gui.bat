@echo off
title Shadow AI - Production GUI Launcher

echo.
echo 🤖 Shadow AI - Production Interface Launcher
echo ===============================================
echo 🎨 Beautiful • 🚀 Fast • 💻 Powerful
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo 📁 Working Directory: %CD%
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo ✅ Python Version:
python --version
echo.

echo 🔧 Installing/Updating GUI dependencies...
echo    This may take a moment on first run...
echo.

REM Install required packages for beautiful GUI
python -m pip install --upgrade pip --quiet
python -m pip install customtkinter pillow psutil requests pyautogui --quiet

if errorlevel 1 (
    echo ⚠️  Some packages may not have installed - GUI will use fallback
) else (
    echo ✅ All dependencies installed successfully!
)

echo.
echo 🎨 Launching Beautiful Shadow AI GUI...
echo    The GUI window should open shortly...
echo.

REM Launch the beautiful GUI
python gui\beautiful_gui.py

REM Check if GUI launched successfully
if errorlevel 1 (
    echo.
    echo ❌ Error launching Beautiful GUI! Trying fallback...
    echo.
    
    REM Try the ultra modern GUI as fallback
    python gui\ultra_modern_gui.py
    
    if errorlevel 1 (
        echo ❌ All GUI options failed!
        echo 💡 You can try: python gui\gui.py
        pause
        exit /b 1
    )
)

echo.
echo 👋 Shadow AI GUI closed successfully.
echo    Thank you for using Shadow AI!
echo.
pause
