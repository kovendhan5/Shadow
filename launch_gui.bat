@echo off
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              🧠 Shadow AI - Modern GUI Launcher              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  🎨 Starting beautiful Shadow AI interface...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌ Python not found. Please install Python 3.7+ 
    pause
    exit /b 1
)

REM Launch the GUI
python demo_gui.py

REM If that fails, try the launcher
if errorlevel 1 (
    echo.
    echo  ⚠️  Demo failed, trying main launcher...
    python launch_gui.py
)

echo.
echo  👋 Thanks for using Shadow AI!
pause
