@echo off
echo ========================================
echo    PyEnv Python Configuration
echo ========================================
echo.

echo Found pyenv installation with Python versions:
echo - Python 3.11.9
echo - Python 3.13.1
echo.

echo Step 1: Adding pyenv to PATH...
set "PYENV_ROOT=C:\Users\koven\.pyenv"
set "PYENV_HOME=%PYENV_ROOT%\pyenv-win"

REM Add pyenv to current session PATH
set "PATH=%PYENV_HOME%\bin;%PYENV_HOME%\shims;%PATH%"

echo Current session PATH updated with pyenv
echo.

echo Step 2: Setting pyenv paths permanently...
REM Set environment variables permanently
setx PYENV_ROOT "%PYENV_ROOT%" >nul 2>&1
setx PYENV_HOME "%PYENV_HOME%" >nul 2>&1
setx PATH "%PYENV_HOME%\bin;%PYENV_HOME%\shims;%PATH%" >nul 2>&1

echo Environment variables set permanently
echo.

echo Step 3: Testing pyenv functionality...
echo.

REM Test pyenv
"%PYENV_HOME%\bin\pyenv.bat" versions
if %ERRORLEVEL% == 0 (
    echo SUCCESS: pyenv is working!
) else (
    echo ERROR: pyenv not responding
)

echo.
echo Step 4: Setting global Python version...
echo.

REM Check current global version
echo Current global Python version:
"%PYENV_HOME%\bin\pyenv.bat" global

echo.
echo Setting Python 3.11.9 as global version...
"%PYENV_HOME%\bin\pyenv.bat" global 3.11.9

echo.
echo Step 5: Testing Python access...
echo.

REM Refresh environment
call "%PYENV_HOME%\bin\pyenv.bat" rehash

REM Test Python
python --version
if %ERRORLEVEL% == 0 (
    echo SUCCESS: Python is accessible!
    echo.
    echo Testing pip...
    pip --version
    if %ERRORLEVEL% == 0 (
        echo SUCCESS: pip is working!
    ) else (
        echo WARNING: pip might need refresh
    )
) else (
    echo Trying direct path...
    "%PYENV_ROOT%\pyenv-win\versions\3.11.9\python.exe" --version
)

echo.
echo Step 6: Creating pyenv activation script...
echo.

echo @echo off > activate_pyenv.bat
echo REM PyEnv activation script >> activate_pyenv.bat
echo set "PYENV_ROOT=C:\Users\koven\.pyenv" >> activate_pyenv.bat
echo set "PYENV_HOME=%%PYENV_ROOT%%\pyenv-win" >> activate_pyenv.bat
echo set "PATH=%%PYENV_HOME%%\bin;%%PYENV_HOME%%\shims;%%PATH%%" >> activate_pyenv.bat
echo call "%%PYENV_HOME%%\bin\pyenv.bat" rehash >> activate_pyenv.bat
echo echo PyEnv activated - Python versions available: >> activate_pyenv.bat
echo "%%PYENV_HOME%%\bin\pyenv.bat" versions >> activate_pyenv.bat

echo Created activate_pyenv.bat - run this anytime to activate pyenv
echo.

echo ========================================
echo PyEnv Configuration Complete!
echo.
echo Available commands:
echo - pyenv versions       : List installed versions
echo - pyenv global X.X.X   : Set global Python version
echo - pyenv local X.X.X    : Set local Python version for this project
echo - activate_pyenv.bat   : Reactivate pyenv if needed
echo.
echo Recommended: Set Python 3.11.9 for compatibility
echo ========================================
echo.

pause
