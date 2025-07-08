@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    Shadow AI - GUI Launcher                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Choose your GUI experience:
echo.
echo 1. Premium GUI     - Professional glassmorphism design
echo 2. Ultra GUI       - Advanced animations and effects  
echo 3. Cyberpunk GUI   - Dark theme with neon effects
echo 4. Working GUI     - Minimal, stable interface
echo 5. Modern GUI      - Standard modern interface
echo.
set /p choice="Enter your choice (1-5): "

cd /d "k:\Devops\Shadow"

if "%choice%"=="1" (
    echo.
    echo 🚀 Launching Premium GUI...
    python gui_premium.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Launching Ultra GUI...
    python gui_ultra.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Launching Cyberpunk GUI...
    python gui_cyberpunk.py
) else if "%choice%"=="4" (
    echo.
    echo 🚀 Launching Working GUI...
    python gui_working.py
) else if "%choice%"=="5" (
    echo.
    echo 🚀 Launching Modern GUI...
    python gui_modern.py
) else (
    echo Invalid choice. Please run again and select 1-5.
    pause
    exit /b 1
)

echo.
echo GUI session ended.
pause
