@echo off
REM Shadow AI Agent Startup Script
REM This script helps you start Shadow AI with different modes

echo.
echo ============================================
echo   🧠 Shadow AI Agent Startup Script
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\pyautogui" (
    echo 📋 Installing requirements...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo Please copy .env.template to .env and configure your API keys
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        echo Setup cancelled. Please configure .env file first.
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Starting Shadow AI Agent...
echo.
echo Available options:
echo   1. Interactive Mode (Default)
echo   2. Voice Mode
echo   3. Demo Mode
echo   4. Help
echo   5. Exit
echo.

set /p choice="Choose an option (1-5): "

if "%choice%"=="1" (
    echo Starting in Interactive Mode...
    python main.py --interactive
) else if "%choice%"=="2" (
    echo Starting in Voice Mode...
    python main.py --voice
) else if "%choice%"=="3" (
    echo Starting Demo Mode...
    python main.py --demo
) else if "%choice%"=="4" (
    echo Showing Help...
    python main.py --help
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Starting in Interactive Mode (default)...
    python main.py
)

echo.
echo 👋 Shadow AI Agent has stopped.
pause
