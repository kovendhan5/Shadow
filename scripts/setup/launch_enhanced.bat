@echo off
title Shadow AI Enhanced - Desktop Assistant
echo.
echo ========================================
echo    Shadow AI Enhanced
echo ========================================
echo.
echo Choose interface:
echo [1] Modern GUI (Recommended)
echo [2] Enhanced CLI
echo [3] Auto-detect best interface
echo.
set /p choice="Enter choice (1-3): "

cd /d "K:\Devops\Shadow"

if "%choice%"=="1" goto GUI
if "%choice%"=="2" goto CLI
if "%choice%"=="3" goto AUTO
goto GUI

:GUI
echo Starting Shadow AI with GUI interface...
K:/Devops/Shadow/venv/Scripts/python.exe gui/modern_gui.py
goto END

:CLI
echo Starting Shadow AI with CLI interface...
K:/Devops/Shadow/venv/Scripts/python.exe enhanced_main.py --cli
goto END

:AUTO
echo Auto-detecting best interface...
K:/Devops/Shadow/venv/Scripts/python.exe enhanced_main.py --gui
goto END

:END
echo.
echo Shadow AI has closed.
pause
