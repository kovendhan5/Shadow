@echo off 
REM Check if Python is accessible 
python --version >nul 2>&1 
if %ERRORLEVEL% neq 0 ( 
    echo Python PATH lost - restoring... 
    set "PATH=%PATH%;C:\Users\koven\AppData\Local\Microsoft\WindowsApps;C:\Users\koven\AppData\Local\Microsoft\WindowsApps\Scripts" 
    setx PATH "%PATH%;C:\Users\koven\AppData\Local\Microsoft\WindowsApps;C:\Users\koven\AppData\Local\Microsoft\WindowsApps\Scripts" /M >nul 2>&1 
) 
