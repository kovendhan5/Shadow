@echo off
echo ========================================
echo    Shadow AI Complete Installation
echo ========================================
echo.

set PYTHON_EXE=K:/Devops/Shadow/venv/Scripts/python.exe

echo Installing core packages (this may take a few minutes)...
echo.

echo [1/5] Installing environment and utility packages...
%PYTHON_EXE% -m pip install python-dotenv colorama psutil --quiet

echo [2/5] Installing input/output packages...
%PYTHON_EXE% -m pip install SpeechRecognition pyttsx3 pynput keyboard --quiet

echo [3/5] Installing automation packages...
%PYTHON_EXE% -m pip install pyautogui pywinauto --quiet

echo [4/5] Installing web packages...
%PYTHON_EXE% -m pip install requests beautifulsoup4 --quiet

echo [5/5] Installing GUI packages...
%PYTHON_EXE% -m pip install customtkinter Pillow --quiet

echo.
echo Testing Shadow AI installation...
echo.

%PYTHON_EXE% -c "
import sys
print('Python version:', sys.version)
print()

# Test core imports
try:
    import speech_recognition
    print('✓ SpeechRecognition imported successfully')
except ImportError as e:
    print('✗ SpeechRecognition failed:', e)

try:
    import pyautogui
    print('✓ PyAutoGUI imported successfully')
except ImportError as e:
    print('✗ PyAutoGUI failed:', e)

try:
    import pynput
    print('✓ PyNput imported successfully')
except ImportError as e:
    print('✗ PyNput failed:', e)

try:
    from dotenv import load_dotenv
    print('✓ python-dotenv imported successfully')
except ImportError as e:
    print('✗ python-dotenv failed:', e)

try:
    import colorama
    print('✓ Colorama imported successfully')
except ImportError as e:
    print('✗ Colorama failed:', e)

print()
print('Core dependencies test complete!')
"

echo.
echo Now testing Shadow AI main script...
echo.

%PYTHON_EXE% main.py --help

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run Shadow AI:
echo %PYTHON_EXE% main.py
echo.
echo Available modes:
echo - Voice mode: %PYTHON_EXE% main.py --voice
echo - Demo mode: %PYTHON_EXE% main.py --demo
echo - GUI mode: %PYTHON_EXE% gui/gui_modern.py
echo.
pause
