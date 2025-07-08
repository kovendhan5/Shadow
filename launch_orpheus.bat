@echo off
title Shadow AI - Orpheus Emotional Interface
color 5f

echo.
echo  ╔═══════════════════════════════════════════════════════════════════════════════════╗
echo  ║                          ORPHEUS EMOTIONAL AI                                    ║
echo  ╠═══════════════════════════════════════════════════════════════════════════════════╣
echo  ║  🎭  Emotional Intelligence                                                       ║
echo  ║  💭  Empathetic Conversations                                                     ║
echo  ║  🎨  Beautiful Visual Indicators                                                  ║
echo  ║  💜  Advanced Emotion Recognition                                                 ║
echo  ║  🗣️  Natural Language Processing                                                 ║
echo  ║  🔄  Dual Mode (Orpheus + Shadow AI)                                            ║
echo  ╚═══════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  [INFO] Initializing Orpheus emotional neural network...
echo  [INFO] Loading emotion recognition models...
echo  [INFO] Preparing empathetic conversation engine...
echo.

cd /d "k:\Devops\Shadow"

REM Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found in system PATH
    echo  [ERROR] Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check Gemini API key
if not exist ".env" (
    echo  [WARNING] .env file not found
    echo  [WARNING] Make sure your Gemini API key is configured
    echo.
)

REM Launch Orpheus emotional interface
echo  [INFO] Starting Orpheus Emotional AI Interface...
echo.
python gui_orpheus.py

echo.
echo  [INFO] Orpheus emotional session ended
echo  [INFO] Thank you for the meaningful conversation
pause
