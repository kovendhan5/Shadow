@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo      🧠 Shadow AI Agent - Environment Setup and Launcher 🚀
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8 or newer.
    echo   Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist venv\ (
    echo 🔄 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully.
)

:: Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)

:: Check if requirements are installed
pip list | findstr pyautogui >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔄 Installing dependencies (this may take a few minutes)...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies!
        echo   Some packages might require Microsoft Visual C++ Build Tools.
        echo   Try running: pip install pyaudio pyttsx3
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully.
)

:: Check if API keys are configured
findstr "your_gemini_key_here" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Warning: API keys not fully configured in .env file.
    echo   Some features may not work without proper API keys.
    echo   Run option 9 to configure API keys.
)

:menu
cls
echo.
echo ================================
echo    🧠 Shadow AI Agent Launcher
echo ================================
echo.
echo Select an option:
echo.
echo 1. GUI Launcher (All GUIs)
echo 2. Quick Launch - Working GUI
echo 3. Quick Launch - Premium GUI  
echo 4. Quick Launch - Cyberpunk GUI
echo 5. Command Line Interface
echo 6. Voice Mode
echo 7. Run Demo
echo 8. Run Tests
echo 9. Configuration
echo 0. Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" (
    echo Starting GUI Launcher...
    python launchers\launch_gui_new.py
) else if "%choice%"=="2" (
    echo Launching Working GUI...
    python gui\gui_working.py
) else if "%choice%"=="3" (
    echo Launching Premium GUI...
    python gui\gui_premium.py
) else if "%choice%"=="4" (
    echo Launching Cyberpunk GUI...
    python gui\gui_cyberpunk.py
) else if "%choice%"=="5" (
    echo Starting command line interface...
    python main.py
) else if "%choice%"=="6" (
    echo Starting voice-enabled mode...
    python main.py --voice
) else if "%choice%"=="7" (
    echo Running demo...
    python demos\demo.py
) else if "%choice%"=="8" (
    echo Running tests...
    python test_imports.py
) else if "%choice%"=="9" (
    echo Opening configuration...
    notepad .env
    goto menu
) else if "%choice%"=="0" (
    echo Goodbye! 👋
    deactivate
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto menu
)

echo.
echo Press any key to return to the menu...
pause >nul
goto menu
