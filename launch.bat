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
    echo Launching GUI selector...
    python gui\gui_modern.py
) else if "%choice%"=="2" (
    echo Starting command line interface...
    python main.py --cli
) else if "%choice%"=="3" (
    echo Starting voice-enabled mode...
    python main.py --voice
) else if "%choice%"=="4" (
    echo Launching Working GUI...
    python gui\gui_working.py
) else if "%choice%"=="5" (
    echo Launching Orpheus Emotional AI...
    python gui\gui_orpheus.py
) else if "%choice%"=="6" (
    echo Launching Enhanced GUI...
    python gui\gui_enhanced.py
) else if "%choice%"=="7" (
    echo Opening configuration...
    notepad .env
) else if "%choice%"=="8" (
    echo Opening documentation...
    explorer docs
) else if "%choice%"=="9" (
    echo Running tests...
    python tests\test_gpt_agent.py
) else if "%choice%"=="0" (
    echo Goodbye! 👋
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)

pause
