@echo off
title Shadow AI - Modern GUI Interface
echo.
echo ========================================
echo     Shadow AI - Modern GUI
echo ========================================
echo.

cd /d "K:\Devops\Shadow"

echo Starting Shadow AI with modern GUI interface...
echo.

K:/Devops/Shadow/venv/Scripts/python.exe gui/modern_gui.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo GUI failed to start. Trying enhanced CLI...
    K:/Devops/Shadow/venv/Scripts/python.exe enhanced_main.py --cli
)

echo.
echo Shadow AI has closed.
pause
