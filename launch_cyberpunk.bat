@echo off
title Shadow AI - Cyberpunk Interface
color 0a

echo.
echo  ╔═══════════════════════════════════════════════════════════════════════════════════╗
echo  ║                      SHADOW AI - CYBERPUNK INTERFACE                             ║
echo  ╠═══════════════════════════════════════════════════════════════════════════════════╣
echo  ║  🖥️  Cyberpunk Dark Theme                                                        ║
echo  ║  ⚡  Neon Glow Effects                                                           ║
echo  ║  🌧️  Matrix Rain Animation                                                       ║
echo  ║  📊  Real-time System Monitoring                                                 ║
echo  ║  🎯  Terminal-style Interface                                                    ║
echo  ║  🔊  Voice Recognition                                                           ║
echo  ╚═══════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  [INFO] Initializing neural networks...
echo  [INFO] Loading cyberpunk interface...
echo  [INFO] Starting matrix effects...
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

REM Launch cyberpunk interface
echo  [INFO] Launching Shadow AI Cyberpunk GUI...
echo.
python gui_cyberpunk.py

echo.
echo  [INFO] Neural interface disconnected
echo  [INFO] Cyberpunk session terminated
pause
