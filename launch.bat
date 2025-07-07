@echo off
echo.
echo ================================
echo    🧠 Shadow AI Agent Launcher
echo ================================
echo.
echo Select an option:
echo.
echo 1. Start Shadow AI (Interactive Mode)
echo 2. Start Shadow AI (Voice Mode)
echo 3. Run Demo
echo 4. Run Tests
echo 5. Start Web Interface
echo 6. Start GUI
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Starting Shadow AI in Interactive Mode...
    python main.py
) else if "%choice%"=="2" (
    echo Starting Shadow AI in Voice Mode...
    python main.py --voice
) else if "%choice%"=="3" (
    echo Running Demo...
    python main.py --demo
) else if "%choice%"=="4" (
    echo Running Tests...
    python -m pytest test_shadow.py -v
) else if "%choice%"=="5" (
    echo Starting Web Interface...
    python web_interface.py
) else if "%choice%"=="6" (
    echo Starting GUI...
    python gui.py
) else if "%choice%"=="7" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    goto :start
)

pause
