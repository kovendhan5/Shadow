@echo off
title Shadow AI - Premium GUI
echo ========================================
echo     Shadow AI - Premium Interface
echo ========================================
echo.
echo Starting premium GUI...
echo.

cd /d "k:\Devops\Shadow"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Start the premium GUI
python gui_premium.py

REM If we get here, the GUI has closed
echo.
echo GUI closed.
pause
