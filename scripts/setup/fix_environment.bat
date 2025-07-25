@echo off
echo ========================================
echo    Environment Variables Diagnostic & Fix Tool
echo ========================================
echo.

echo Step 1: Detecting current environment state...
echo.

:: Check current PATH
echo Current PATH environment variable:
echo %PATH%
echo.

:: Check for Python installations
echo Searching for Python installations...

:: Common Python installation paths
set "PYTHON_LOCATIONS=C:\Python*;C:\Program Files\Python*;%USERPROFILE%\AppData\Local\Programs\Python\*;%LOCALAPPDATA%\Programs\Python\*"

:: Check registry for Python installations
echo Checking Windows Registry for Python...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python" 2>nul && echo Found Python in HKLM\SOFTWARE\Python
reg query "HKEY_CURRENT_USER\SOFTWARE\Python" 2>nul && echo Found Python in HKCU\SOFTWARE\Python

:: Check common directories
for %%d in (C:\Python39 C:\Python310 C:\Python311 C:\Python312) do (
    if exist "%%d\python.exe" (
        echo Found Python at: %%d
        set "FOUND_PYTHON=%%d"
    )
)

for %%d in ("C:\Program Files\Python39" "C:\Program Files\Python310" "C:\Program Files\Python311" "C:\Program Files\Python312") do (
    if exist "%%d\python.exe" (
        echo Found Python at: %%d
        set "FOUND_PYTHON=%%d"
    )
)

:: Check AppData locations
for %%d in ("%USERPROFILE%\AppData\Local\Programs\Python\Python39" "%USERPROFILE%\AppData\Local\Programs\Python\Python310" "%USERPROFILE%\AppData\Local\Programs\Python\Python311" "%USERPROFILE%\AppData\Local\Programs\Python\Python312") do (
    if exist "%%d\python.exe" (
        echo Found Python at: %%d
        set "FOUND_PYTHON=%%d"
    )
)

echo.
echo Step 2: Checking what's causing environment variable loss...
echo.

:: Check for potential causes
echo Checking potential causes:

:: Check if any antivirus is interfering
echo - Checking for antivirus interference...
tasklist /FI "IMAGENAME eq *antivirus*" 2>nul | find /I "antivirus" >nul && echo "  WARNING: Antivirus may be interfering"

:: Check for system restore or cleanup tools
echo - Checking for system cleanup tools...
schtasks /query /tn "*cleanup*" 2>nul | find "cleanup" >nul && echo "  WARNING: System cleanup tasks found"

:: Check for registry cleaners
echo - Checking for recent registry modifications...
echo   (This requires checking system logs)

echo.
echo Step 3: Creating permanent environment variable fix...
echo.

:: Create a PowerShell script for permanent PATH fixing
echo Creating PowerShell environment fix script...

powershell -Command "
# PowerShell script to permanently fix environment variables
Write-Host 'Creating permanent environment variable solution...' -ForegroundColor Green

# Function to add to PATH if not already present
function Add-ToPath {
    param([string]$PathToAdd, [string]$Scope = 'User')
    
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', $Scope)
    if ($currentPath -notlike '*' + $PathToAdd + '*') {
        $newPath = $currentPath + ';' + $PathToAdd
        [Environment]::SetEnvironmentVariable('PATH', $newPath, $Scope)
        Write-Host \"Added to PATH ($Scope): $PathToAdd\" -ForegroundColor Yellow
        return $true
    } else {
        Write-Host \"Already in PATH ($Scope): $PathToAdd\" -ForegroundColor Gray
        return $false
    }
}

# Search for Python installations
$pythonPaths = @()
$searchPaths = @(
    'C:\Python*',
    'C:\Program Files\Python*',
    '$env:USERPROFILE\AppData\Local\Programs\Python\Python*'
)

foreach ($searchPath in $searchPaths) {
    $found = Get-ChildItem -Path (Split-Path $searchPath -Parent) -Directory -Name (Split-Path $searchPath -Leaf) -ErrorAction SilentlyContinue
    foreach ($dir in $found) {
        $fullPath = Join-Path (Split-Path $searchPath -Parent) $dir
        if (Test-Path (Join-Path $fullPath 'python.exe')) {
            $pythonPaths += $fullPath
            $pythonPaths += Join-Path $fullPath 'Scripts'
        }
    }
}

# Add found Python paths to both User and System PATH
$pathsAdded = $false
foreach ($path in $pythonPaths) {
    if (Add-ToPath $path 'User') { $pathsAdded = $true }
    # Try to add to System PATH (requires admin)
    try {
        if (Add-ToPath $path 'Machine') { $pathsAdded = $true }
    } catch {
        Write-Host \"Cannot add to System PATH (requires admin): $path\" -ForegroundColor Red
    }
}

# Add other common tool paths
$commonPaths = @(
    'C:\Program Files\Git\cmd',
    'C:\Program Files\Git\bin',
    'C:\Program Files\nodejs',
    'C:\Windows\System32',
    'C:\Windows',
    'C:\Windows\System32\Wbem',
    'C:\Windows\System32\WindowsPowerShell\v1.0'
)

foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Add-ToPath $path 'User'
    }
}

if ($pathsAdded) {
    Write-Host 'Environment variables updated successfully!' -ForegroundColor Green
    Write-Host 'Please restart your command prompt for changes to take effect.' -ForegroundColor Yellow
} else {
    Write-Host 'No new paths were added.' -ForegroundColor Gray
}
"

echo.
echo Step 4: Creating environment variable monitor/restore script...
echo.

:: Create a monitoring script
echo Creating environment monitor script...

powershell -Command "
# Create a monitoring script that runs at startup
$monitorScript = @'
# Environment Variable Monitor and Restore Script
# This script checks and restores missing environment variables

function Restore-EnvironmentVariables {
    $expectedPaths = @()
    
    # Find Python installations
    $pythonSearchPaths = @(
        'C:\Python*',
        'C:\Program Files\Python*',
        '$env:USERPROFILE\AppData\Local\Programs\Python\Python*'
    )
    
    foreach ($searchPath in $pythonSearchPaths) {
        try {
            $found = Get-ChildItem -Path (Split-Path $searchPath -Parent) -Directory -Name (Split-Path $searchPath -Leaf) -ErrorAction SilentlyContinue
            foreach ($dir in $found) {
                $fullPath = Join-Path (Split-Path $searchPath -Parent) $dir
                if (Test-Path (Join-Path $fullPath 'python.exe')) {
                    $expectedPaths += $fullPath
                    $expectedPaths += Join-Path $fullPath 'Scripts'
                }
            }
        } catch {}
    }
    
    # Add other essential paths
    $expectedPaths += @(
        'C:\Windows\System32',
        'C:\Windows',
        'C:\Windows\System32\Wbem',
        'C:\Windows\System32\WindowsPowerShell\v1.0',
        'C:\Program Files\Git\cmd',
        'C:\Program Files\Git\bin',
        'C:\Program Files\nodejs'
    )
    
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    $pathsRestored = 0
    
    foreach ($path in $expectedPaths) {
        if ((Test-Path $path) -and ($currentPath -notlike '*' + $path + '*')) {
            $currentPath = $currentPath + ';' + $path
            $pathsRestored++
            Write-Host \"Restored missing path: $path\" -ForegroundColor Yellow
        }
    }
    
    if ($pathsRestored -gt 0) {
        [Environment]::SetEnvironmentVariable('PATH', $currentPath, 'User')
        Write-Host \"Restored $pathsRestored missing environment paths\" -ForegroundColor Green
    }
}

# Run the restore function
Restore-EnvironmentVariables

# Log the check
$logFile = '$env:USERPROFILE\Desktop\env_check.log'
$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
Add-Content -Path $logFile -Value \"$timestamp - Environment variables checked and restored\"
'@

# Save the monitor script
$scriptPath = '$env:USERPROFILE\Desktop\env_monitor.ps1'
$monitorScript | Out-File -FilePath $scriptPath -Encoding UTF8

Write-Host \"Monitor script created at: $scriptPath\" -ForegroundColor Green

# Create a batch file to run the monitor script
$batchContent = @'
@echo off
powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File \"%USERPROFILE%\Desktop\env_monitor.ps1\"
'@

$batchPath = '$env:USERPROFILE\Desktop\env_monitor.bat'
$batchContent | Out-File -FilePath $batchPath -Encoding ASCII

Write-Host \"Batch launcher created at: $batchPath\" -ForegroundColor Green
"

echo.
echo Step 5: Setting up automatic restoration...
echo.

:: Create startup task
echo Setting up automatic startup task...

schtasks /Create /TN "EnvironmentVariableRestore" /TR "%USERPROFILE%\Desktop\env_monitor.bat" /SC ONLOGON /F 2>nul
if %errorlevel% == 0 (
    echo ✓ Startup task created successfully
) else (
    echo ⚠ Could not create startup task (may require admin rights)
)

echo.
echo Step 6: Creating manual fix script...
echo.

:: Create a manual fix script for immediate use
echo Creating immediate fix script...

echo @echo off > fix_env_now.bat
echo echo Fixing environment variables immediately... >> fix_env_now.bat
echo. >> fix_env_now.bat

if defined FOUND_PYTHON (
    echo echo Adding Python to PATH: %FOUND_PYTHON% >> fix_env_now.bat
    echo setx PATH "%%PATH%%;%FOUND_PYTHON%;%FOUND_PYTHON%\Scripts" >> fix_env_now.bat
    echo set PATH=%%PATH%%;%FOUND_PYTHON%;%FOUND_PYTHON%\Scripts >> fix_env_now.bat
)

echo echo Environment variables updated for current session >> fix_env_now.bat
echo echo Please restart your command prompt for permanent changes >> fix_env_now.bat
echo pause >> fix_env_now.bat

echo ✓ Manual fix script created: fix_env_now.bat

echo.
echo Step 7: Testing Python availability...
echo.

:: Try the manual fix first
call fix_env_now.bat

echo.
echo ========================================
echo    Fix Complete!
echo ========================================
echo.
echo Files created:
echo - fix_env_now.bat (Manual fix for immediate use)
echo - env_monitor.ps1 (Automatic monitoring script)
echo - env_monitor.bat (Startup launcher)
echo.
echo What was done:
echo 1. Detected Python installations
echo 2. Added Python to PATH (User and System if possible)
echo 3. Created monitoring script for automatic restoration
echo 4. Set up startup task to run monitor on login
echo 5. Created manual fix script for immediate use
echo.
echo To prevent future issues:
echo 1. Run fix_env_now.bat whenever variables are lost
echo 2. The monitor script will run automatically at startup
echo 3. Check env_check.log on your desktop for monitoring logs
echo.
echo Possible causes of environment variable loss:
echo - Antivirus software interference
echo - System cleanup tools
echo - Registry cleaners
echo - Windows updates
echo - Third-party software conflicts
echo.
pause
