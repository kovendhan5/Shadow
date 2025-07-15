@echo off
echo.
echo ====================================================
echo     🚀 Shadow AI - Quick Start Launcher
echo ====================================================
echo.

:: Activate virtual environment if it exists
if exist venv\ (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Note: No virtual environment found (venv).
    echo Running in system Python environment.
)

:: Check if there are missing dependencies
echo Running quick dependency check...
python -c "try: import pyautogui, pyttsx3; print('✅ Basic dependencies found'); except ImportError as e: print(f'❌ Missing dependency: {e}');"

echo.
echo Choose how to start Shadow AI:
echo.
echo 1. Command Line Interface (simple)
echo 2. Working GUI (recommended)
echo 3. Premium GUI (advanced)
echo 0. Exit
echo.

set /p choice="Enter your choice (0-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Shadow AI Command Line Interface...
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Shadow AI Working GUI...
    python gui\gui_working.py
) else if "%choice%"=="3" (
    echo.
    echo Starting Shadow AI Premium GUI...
    python gui\gui_premium.py
) else if "%choice%"=="0" (
    echo.
    echo Goodbye! 👋
    exit /b 0
) else (
    echo.
    echo Invalid choice. Exiting.
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
