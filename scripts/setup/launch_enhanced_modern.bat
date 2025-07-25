@echo off
title Shadow AI Enhanced Launcher
color 0A

echo.
echo ========================================
echo           SHADOW AI ENHANCED
echo         Desktop AI Assistant
echo ========================================
echo.

echo Available interfaces:
echo [1] Enhanced GUI (Recommended)
echo [2] Modern GUI  
echo [3] Enhanced CLI
echo [4] Basic CLI
echo [5] Exit
echo.

set /p choice="Select interface (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Enhanced GUI...
    python gui/enhanced_modern_gui.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Starting Modern GUI...
    python gui/modern_gui.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Starting Enhanced CLI...
    python enhanced_main.py --cli
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Starting Basic CLI...
    python main.py
    goto end
)

if "%choice%"=="5" (
    echo Goodbye!
    goto end
)

echo Invalid choice. Please select 1-5.
pause
goto start

:end
echo.
echo Shadow AI session ended.
pause
