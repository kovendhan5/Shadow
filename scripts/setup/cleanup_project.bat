@echo off
echo ========================================
echo     Shadow AI Project Cleanup
echo ========================================
echo.

cd /d "K:\Devops\Shadow"

echo Removing unwanted files and directories...

REM Remove test directories and files
if exist "tests\" (
    echo Removing tests directory...
    rmdir /s /q tests
)

if exist "demos\" (
    echo Removing demos directory...
    rmdir /s /q demos
)

if exist "examples\" (
    echo Removing examples directory...
    rmdir /s /q examples
)

if exist "launchers\" (
    echo Removing launchers directory...
    rmdir /s /q launchers
)

if exist "knowledge_base\" (
    echo Removing knowledge_base directory...
    rmdir /s /q knowledge_base
)

if exist "plugins\" (
    echo Removing plugins directory...
    rmdir /s /q plugins
)

if exist "downloads\" (
    echo Removing downloads directory...
    rmdir /s /q downloads
)

REM Remove markdown documentation files (keep main README)
echo Removing excess documentation...
del /q *.md 2>nul
if exist "README.md" (
    echo Keeping README.md...
) else (
    echo README.md not found.
)

REM Remove __pycache__ directories
echo Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Remove .pyc files
del /s /q *.pyc 2>nul

REM Remove log files
if exist "logs\" (
    del /q logs\*.log 2>nul
)

REM Clean up old launcher scripts
echo Removing redundant launchers...
del /q launch.bat 2>nul
del /q launch_modern.py 2>nul
del /q launch_ultra_modern.py 2>nul

echo.
echo ========================================
echo Cleanup completed!
echo.
echo Remaining core files:
echo • enhanced_main.py (CLI interface)
echo • gui/modern_gui.py (GUI interface)
echo • launch_enhanced.bat (main launcher)
echo • launch_gui.bat (GUI launcher)
echo • config.py (configuration)
echo • requirements.txt (dependencies)
echo.
echo Core directories:
echo • brain/ (AI processing)
echo • control/ (desktop automation)
echo • input/ (voice and text input)
echo • utils/ (utilities)
echo • report/ (report generation)
echo ========================================
echo.
pause
