@echo off
echo ========================================
echo    Python PATH Fix Utility
echo ========================================
echo.

echo Step 1: Finding Python installation...
echo.

REM Check common Python installation locations
set "PYTHON_FOUND="
set "PYTHON_PATH="

REM Check Microsoft Store Python
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
    echo Found Python in Microsoft Store location
    set "PYTHON_FOUND=1"
    set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps"
)

REM Check Python.org installations
for /d %%i in ("C:\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python in %%i
        set "PYTHON_FOUND=1"
        set "PYTHON_PATH=%%i"
    )
)

REM Check Program Files
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python in %%i
        set "PYTHON_FOUND=1"
        set "PYTHON_PATH=%%i"
    )
)

REM Check AppData Local
for /d %%i in ("C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo Found Python in %%i
        set "PYTHON_FOUND=1"
        set "PYTHON_PATH=%%i"
    )
)

if not defined PYTHON_FOUND (
    echo ERROR: Python installation not found!
    echo Please install Python from python.org or Microsoft Store
    pause
    exit /b 1
)

echo.
echo Step 2: Current PATH status...
echo PATH=%PATH%
echo.

echo Step 3: Checking if Python is in PATH...
python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Python is accessible from PATH
    python --version
) else (
    echo Python is NOT accessible from PATH
    echo Adding %PYTHON_PATH% to system PATH...
    
    REM Add to system PATH permanently
    setx PATH "%PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts" /M >nul 2>&1
    if %ERRORLEVEL% == 0 (
        echo Successfully added Python to system PATH
    ) else (
        echo Adding to user PATH instead...
        setx PATH "%PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts" >nul 2>&1
    )
    
    REM Update current session PATH
    set "PATH=%PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts"
    echo Updated current session PATH
)

echo.
echo Step 4: Testing Python access...
echo.
python --version
if %ERRORLEVEL% == 0 (
    echo SUCCESS: Python is now accessible!
    echo.
    echo Testing pip...
    pip --version
    if %ERRORLEVEL% == 0 (
        echo SUCCESS: pip is also working!
    ) else (
        echo WARNING: pip might need to be installed
    )
) else (
    echo ERROR: Python still not accessible
    echo You may need to restart your command prompt or computer
)

echo.
echo Step 5: Creating monitoring script...
echo Creating python_monitor.bat...

echo @echo off > python_monitor.bat
echo REM Check if Python is accessible >> python_monitor.bat
echo python --version ^>nul 2^>^&1 >> python_monitor.bat
echo if %%ERRORLEVEL%% neq 0 ( >> python_monitor.bat
echo     echo Python PATH lost - restoring... >> python_monitor.bat
echo     set "PATH=%%PATH%%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts" >> python_monitor.bat
echo     setx PATH "%%PATH%%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts" /M ^>nul 2^>^&1 >> python_monitor.bat
echo ^) >> python_monitor.bat

echo.
echo Monitoring script created: python_monitor.bat
echo You can run this anytime to restore Python PATH if it gets lost again.

echo.
echo ========================================
echo Fix complete! Summary:
echo - Python found at: %PYTHON_PATH%
echo - Added to system PATH
echo - Monitoring script created
echo ========================================
echo.
pause
