@echo off
echo.
echo ===============================================
echo    🎉 Shadow AI - Project Improvement Complete!
echo ===============================================
echo.
echo ✅ IMPROVEMENTS COMPLETED:
echo    • 4 Fully Functional GUI Interfaces
echo    • Enhanced Launcher System  
echo    • All Core Modules Operational
echo    • Security Vulnerabilities Fixed
echo    • Dependencies Installed & Verified
echo.
echo 🚀 READY TO USE:
echo    1. Working GUI     - Simple & Reliable
echo    2. Premium GUI     - Advanced Features
echo    3. Cyberpunk GUI   - Futuristic Theme
echo    4. Modern GUI      - Clean Design
echo.
echo 📋 TO GET STARTED:
echo    1. Configure your API key in .env file
echo    2. Run this launcher (launch.bat)
echo    3. Choose your preferred interface
echo.
echo 🔗 Quick Launch Options:
echo    • python gui\gui_working.py (Quick Start)
echo    • python launchers\launch_gui_new.py (All GUIs)
echo.
echo Press any key to continue to main launcher...
pause >nul
cls
goto :launcher

:launcher
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
    python quick_test.py
) else if "%choice%"=="9" (
    echo Opening configuration...
    notepad .env
) else if "%choice%"=="0" (
    echo Goodbye! 👋
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :launcher
)

pause
