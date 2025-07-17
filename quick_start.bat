@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo     🚀 Shadow AI - Enhanced Quick Start Launcher
echo ====================================================
echo.

:: Check for virtual environment and activate if available
if exist venv\ (
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate.bat
    if !errorlevel! equ 0 (
        echo ✅ Virtual environment activated
    ) else (
        echo ⚠️  Could not activate virtual environment
    )
) else (
    echo ⚠️  No virtual environment found (venv\).
    echo    Running in system Python environment.
    echo    For better isolation, consider running enhanced_installer.py
)

:: Check Python availability
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ❌ Python not found! Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if basic dependencies are available
echo.
echo 🔍 Checking basic dependencies...
python -c "import sys, os, json, logging; print('✅ Core Python modules OK')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ Basic Python modules missing!
    goto install_prompt
)

python -c "import pyautogui; print('✅ PyAutoGUI available')" 2>nul
if !errorlevel! neq 0 (
    echo ⚠️  PyAutoGUI not found
    set MISSING_DEPS=1
)

python -c "import config; print('✅ Config module available')" 2>nul
if !errorlevel! neq 0 (
    echo ❌ Config module not found!
    goto install_prompt
)

if defined MISSING_DEPS (
    echo.
    echo ⚠️  Some dependencies are missing. Shadow AI will use fallback functionality.
    echo    For full features, consider running: pip install -r requirements.txt
    echo.
)

:: Show menu
:menu
echo.
echo Choose how to start Shadow AI:
echo.
echo 1. Command Line Interface (always works)
echo 2. Working GUI (recommended)
echo 3. Premium GUI (advanced features)
echo 4. Run Diagnostic Tool
echo 5. Install/Update Dependencies
echo 6. Open Configuration (.env)
echo 0. Exit
echo.

set /p choice="Enter your choice (0-6): "

if "!choice!"=="1" (
    echo.
    echo 🚀 Starting Shadow AI Command Line Interface...
    python main.py
    goto end
) else if "!choice!"=="2" (
    echo.
    echo 🎨 Starting Shadow AI Working GUI...
    python gui\gui_working.py
    goto end
) else if "!choice!"=="3" (
    echo.
    echo 💎 Starting Shadow AI Premium GUI...
    python gui\gui_premium.py
    goto end
) else if "!choice!"=="4" (
    echo.
    echo 🔍 Running diagnostic tool...
    python diagnostic.py
    goto menu
) else if "!choice!"=="5" (
    echo.
    echo � Installing/updating dependencies...
    pip install -r requirements.txt --upgrade
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto menu
) else if "!choice!"=="6" (
    echo.
    echo ⚙️  Opening configuration file...
    if exist .env (
        notepad .env
    ) else (
        echo ❌ .env file not found. Creating template...
        python -c "
with open('.env', 'w') as f:
    f.write('# Shadow AI Configuration\n')
    f.write('OPENAI_API_KEY=your_openai_key_here\n')
    f.write('GEMINI_API_KEY=your_gemini_key_here\n')
    f.write('VOICE_ENABLED=True\n')
    f.write('REQUIRE_CONFIRMATION=True\n')
print('✅ .env template created')
"
        notepad .env
    )
    goto menu
) else if "!choice!"=="0" (
    echo.
    echo 👋 Goodbye!
    goto end
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    goto menu
)

:install_prompt
echo.
echo 🔧 Missing critical dependencies detected!
echo.
echo Options:
echo 1. Run enhanced installer (recommended)
echo 2. Manual install with pip
echo 3. Continue anyway (limited functionality)
echo.
set /p install_choice="Choose option (1-3): "

if "!install_choice!"=="1" (
    echo.
    echo 🚀 Running enhanced installer...
    python enhanced_installer.py
    goto end
) else if "!install_choice!"=="2" (
    echo.
    echo 📦 Installing dependencies with pip...
    pip install -r requirements.txt
    echo.
    echo ✅ Installation complete. Restarting launcher...
    goto menu
) else (
    echo.
    echo ⚠️  Continuing with limited functionality...
    goto menu
)

:end
echo.
if exist venv\ (
    echo 🔄 Deactivating virtual environment...
    deactivate
)
echo Press any key to exit...
pause >nul
