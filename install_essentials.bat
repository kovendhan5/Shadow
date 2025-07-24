@echo off
echo Installing essential Shadow AI packages...
echo.

set PYTHON_EXE=K:/Devops/Shadow/venv/Scripts/python.exe

echo Installing python-dotenv...
%PYTHON_EXE% -m pip install python-dotenv --quiet

echo Installing pyautogui...
%PYTHON_EXE% -m pip install pyautogui --quiet

echo Installing colorama...
%PYTHON_EXE% -m pip install colorama --quiet

echo Installing requests...
%PYTHON_EXE% -m pip install requests --quiet

echo.
echo Testing Shadow AI...
echo.
%PYTHON_EXE% main.py --help

echo.
echo Essential packages installed! Shadow AI should now work.
pause
