@echo off
echo ========================================
echo    Python Installation for Shadow AI
echo ========================================
echo.

echo This script will help you install Python properly with PATH configuration.
echo.

echo Step 1: Download Python installer...
echo.

:: Create downloads directory if it doesn't exist
if not exist "downloads" mkdir downloads

:: Download Python 3.11 installer (stable version)
echo Downloading Python 3.11.9 installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'downloads\python-installer.exe'"

if not exist "downloads\python-installer.exe" (
    echo Failed to download Python installer!
    echo Please manually download from: https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    goto :end
)

echo.
echo Step 2: Installing Python...
echo.
echo IMPORTANT: During installation, make sure to:
echo 1. Check "Add Python to PATH"
echo 2. Check "Install for all users" (if you have admin rights)
echo 3. Choose "Customize installation" and select all optional features
echo.
pause

:: Run Python installer with automatic PATH setup
echo Running Python installer...
start /wait "downloads\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo.
echo Step 3: Verifying installation...
echo.

:: Refresh environment variables
call :refresh_env

:: Test Python installation
python --version
if %errorlevel% == 0 (
    echo Python installed successfully!
    goto :setup_project
) else (
    echo Python installation may have failed or PATH not updated.
    echo Please restart your command prompt and try again.
    echo Or manually add Python to your PATH.
    pause
    goto :end
)

:setup_project
echo.
echo Step 4: Setting up Shadow AI...
echo.

echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel__ == 0 (
    echo.
    echo Success! Shadow AI is ready to use.
    echo You can now run: python main.py
    echo.
) else (
    echo There was an issue installing some packages.
    echo Please check the error messages above.
    echo.
)

:end
echo.
echo Setup complete!
pause
goto :eof

:refresh_env
:: Refresh environment variables without restarting CMD
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "user_path=%%b"
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "system_path=%%b"
set "PATH=%system_path%;%user_path%"
goto :eof
