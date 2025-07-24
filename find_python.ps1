# PowerShell script to find and add Python to PATH
Write-Host "Python PATH Setup for Shadow AI" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if Python is already working
try {
    $version = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python is already working: $version" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "Python not found in PATH" -ForegroundColor Yellow
}

# Search for Python installations
$pythonPaths = @(
    "C:\Python39",
    "C:\Python310", 
    "C:\Python311",
    "C:\Python312",
    "C:\Program Files\Python39",
    "C:\Program Files\Python310",
    "C:\Program Files\Python311", 
    "C:\Program Files\Python312",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python39",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python310",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python311",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python312"
)

$foundPython = $null
foreach ($path in $pythonPaths) {
    $pythonExe = Join-Path $path "python.exe"
    if (Test-Path $pythonExe) {
        Write-Host "Found Python at: $path" -ForegroundColor Green
        try {
            $testVersion = & $pythonExe --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $foundPython = $path
                Write-Host "Python version: $testVersion" -ForegroundColor Green
                break
            }
        } catch {
            continue
        }
    }
}

if ($foundPython) {
    Write-Host "Adding Python to PATH..." -ForegroundColor Yellow
    
    # Get current user PATH
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    
    # Add Python directories
    $scriptsPath = Join-Path $foundPython "Scripts"
    $newPaths = @($foundPython, $scriptsPath)
    
    $pathUpdated = $false
    foreach ($newPath in $newPaths) {
        if ($currentPath -notlike "*$newPath*") {
            if ($currentPath) {
                $currentPath = "$currentPath;$newPath"
            } else {
                $currentPath = $newPath
            }
            $pathUpdated = $true
            Write-Host "Added to PATH: $newPath" -ForegroundColor Gray
        } else {
            Write-Host "Already in PATH: $newPath" -ForegroundColor Gray
        }
    }
    
    if ($pathUpdated) {
        [Environment]::SetEnvironmentVariable("PATH", $currentPath, "User")
        Write-Host "PATH updated successfully!" -ForegroundColor Green
        Write-Host "Please restart your command prompt for changes to take effect." -ForegroundColor Yellow
    } else {
        Write-Host "Python paths already in PATH" -ForegroundColor Green
    }
} else {
    Write-Host "No Python installation found!" -ForegroundColor Red
    Write-Host "Please install Python from: https://python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
