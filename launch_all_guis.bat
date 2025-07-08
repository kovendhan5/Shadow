@echo off
color 0b
title Shadow AI - Ultimate GUI Collection

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════════╗
echo ║                          SHADOW AI - GUI COLLECTION                             ║
echo ║                          🎨 Choose Your Experience                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  🎯 AVAILABLE INTERFACES:
echo.
echo  1. 💎 PREMIUM GUI
echo     └─ Professional glassmorphism design with card layouts
echo     └─ Perfect for business and professional environments
echo.
echo  2. 🌈 ULTRA MODERN GUI  
echo     └─ Advanced animations with gradient backgrounds
echo     └─ Cutting-edge visual effects and smooth transitions
echo.
echo  3. 🌌 CYBERPUNK GUI
echo     └─ Dark theme with neon effects and matrix rain
echo     └─ Terminal-style interface for developers and hackers
echo.
echo  4. 🎨 MODERN GUI
echo     └─ Clean and balanced modern interface
echo     └─ Standard modern design with essential features
echo.
echo  5. 🛠️ WORKING GUI
echo     └─ Minimal, stable interface for maximum reliability
echo     └─ Best for older systems or when you need stability
echo.
echo  0. ❌ EXIT
echo.

set /p choice="🚀 Select your interface (0-5): "

cd /d "k:\Devops\Shadow"

if "%choice%"=="1" (
    echo.
    echo 💎 Launching Premium GUI...
    echo ✨ Loading glassmorphism effects...
    python gui_premium.py
) else if "%choice%"=="2" (
    echo.
    echo 🌈 Launching Ultra Modern GUI...
    echo ⚡ Initializing advanced animations...
    python gui_ultra.py
) else if "%choice%"=="3" (
    echo.
    echo 🌌 Launching Cyberpunk GUI...
    echo 🖥️ Starting neural interface...
    python gui_cyberpunk.py
) else if "%choice%"=="4" (
    echo.
    echo 🎨 Launching Modern GUI...
    echo 📱 Loading standard interface...
    python gui_modern.py
) else if "%choice%"=="5" (
    echo.
    echo 🛠️ Launching Working GUI...
    echo 🔧 Starting minimal interface...
    python gui_working.py
) else if "%choice%"=="0" (
    echo.
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please select 0-5.
    echo.
    pause
    goto :eof
)

echo.
echo 📊 GUI session completed.
echo 🔄 Run this script again to try a different interface!
echo.
pause
