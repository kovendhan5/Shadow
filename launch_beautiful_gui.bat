@echo off
title Shadow AI - Beautiful GUI Launcher

echo.
echo 🤖 Shadow AI - Beautiful Interface
echo ===============================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo 📁 Current Directory: %CD%
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies quietly
echo 🔧 Checking dependencies...
python -m pip install --quiet customtkinter pillow psutil >nul 2>&1

echo 🎨 Launching Beautiful GUI...
echo.

REM Launch the beautiful GUI
python gui\beautiful_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error launching GUI!
    pause
)

echo.
echo 👋 GUI closed.
pause
