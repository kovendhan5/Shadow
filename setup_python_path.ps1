# PowerShell script to find and add Python to PATH
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Python PATH Setup for Shadow AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to test if Python works
function Test-Python($pythonPath) {
    try {
        $version = & "$pythonPath" --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found: $version" -ForegroundColor Green
            return $true
        }
    } catch {
        return $false
    }
    return $false
}

# Check if Python is already in PATH
Write-Host "Checking if Python is already available..." -ForegroundColor Yellow
if (Test-Python "python") {
    Write-Host "Python is already working!" -ForegroundColor Green
    python --version
} else {
    Write-Host "Python not found in PATH. Searching for installations..." -ForegroundColor Yellow
    
    # Common Python installation paths
    $pythonPaths = @(
        "C:\Python39\python.exe",
        "C:\Python310\python.exe",
        "C:\Python311\python.exe", 
        "C:\Python312\python.exe",
        "C:\Program Files\Python39\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python312\python.exe",
        "$env:USERPROFILE\AppData\Local\Programs\Python\Python39\python.exe",
        "$env:USERPROFILE\AppData\Local\Programs\Python\Python310\python.exe",
        "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\python.exe",
        "$env:USERPROFILE\AppData\Local\Programs\Python\Python312\python.exe"
    )
    
    $foundPython = $null
    foreach ($path in $pythonPaths) {
        if (Test-Path $path) {
            Write-Host "Found Python installation: $path" -ForegroundColor Green
            if (Test-Python $path) {
                $foundPython = Split-Path $path -Parent
                break
            }
        }
    }
    
    if ($foundPython) {
        Write-Host "Adding Python to PATH..." -ForegroundColor Yellow
        
        # Get current user PATH
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Add Python and Scripts directory if not already present
        $pythonDir = $foundPython
        $scriptsDir = Join-Path $foundPython "Scripts"
        
        $newPath = $currentPath
        if ($currentPath -notlike "*$pythonDir*") {
            $newPath = "$currentPath;$pythonDir"
        }
        if ($currentPath -notlike "*$scriptsDir*") {
            $newPath = "$newPath;$scriptsDir"
        }
        
        # Set the new PATH
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        
        Write-Host "✓ Python added to PATH!" -ForegroundColor Green
        Write-Host "Added: $pythonDir" -ForegroundColor Gray
        Write-Host "Added: $scriptsDir" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Please restart your command prompt/VS Code for changes to take effect." -ForegroundColor Yellow
        
    } else {
        Write-Host "❌ No working Python installation found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install Python from: https://python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Current PATH includes:" -ForegroundColor Cyan
$env:PATH -split ";" | Where-Object { $_ -like "*python*" -or $_ -like "*Python*" } | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
