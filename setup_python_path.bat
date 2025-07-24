@echo off
echo ========================================
echo    Python PATH Setup for Shadow AI
echo ========================================
echo.

echo Step 1: Checking for existing Python installations...
echo.

:: Check if Python is already working
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already working! Version:
    python --version
    echo.
    goto :setup_project
)

:: Check common Python installation paths
set "PYTHON_PATHS=C:\Python39;C:\Python310;C:\Python311;C:\Python312;C:\Program Files\Python39;C:\Program Files\Python310;C:\Program Files\Python311;C:\Program Files\Python312;%USERPROFILE%\AppData\Local\Programs\Python\Python39;%USERPROFILE%\AppData\Local\Programs\Python\Python310;%USERPROFILE%\AppData\Local\Programs\Python\Python311;%USERPROFILE%\AppData\Local\Programs\Python\Python312"

echo Searching for Python installations...
for %%p in (%PYTHON_PATHS%) do (
    if exist "%%p\python.exe" (
        echo Found Python at: %%p
        set "FOUND_PYTHON=%%p"
        goto :found_python
    )
)

echo No Python installation found in common locations.
echo.
echo Please download and install Python from: https://python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation!
echo.
pause
goto :end

:found_python
echo.
echo Found Python installation at: %FOUND_PYTHON%
echo.
echo Testing Python installation...
"%FOUND_PYTHON%\python.exe" --version
if %errorlevel% neq 0 (
    echo Python installation appears to be corrupted.
    echo Please reinstall Python from https://python.org/downloads/
    pause
    goto :end
)

echo.
echo Adding Python to PATH environment variable...
echo.

:: Add Python to system PATH (requires admin rights)
echo Current PATH: %PATH%
echo.
echo Adding: %FOUND_PYTHON%
echo Adding: %FOUND_PYTHON%\Scripts

:: Try to add to user PATH first (doesn't require admin)
powershell -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';%FOUND_PYTHON%;%FOUND_PYTHON%\Scripts', 'User')"

echo.
echo Python PATH has been updated for your user account.
echo Please restart your command prompt or VS Code for changes to take effect.
echo.

:setup_project
echo Step 2: Setting up Shadow AI project...
echo.

:: Try to use the found Python or system Python
if defined FOUND_PYTHON (
    set "PYTHON_CMD=%FOUND_PYTHON%\python.exe"
) else (
    set "PYTHON_CMD=python"
)

echo Using Python: %PYTHON_CMD%
echo.

echo Installing required packages...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install -r requirements.txt

echo.
echo Testing Shadow AI...
%PYTHON_CMD% quick_test.py

echo.
echo Setup complete! You can now run Shadow AI with:
echo %PYTHON_CMD% main.py
echo.

:end
pause
