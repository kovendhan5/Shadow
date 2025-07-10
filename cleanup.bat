@echo off
title Shadow AI - Cleanup Script
echo.
echo 🧹 Shadow AI Cleanup Script
echo =============================
echo.
echo This script will remove temporary and cache files
echo.
pause

echo Cleaning Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo Cleaning temporary files...
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *.bak 2>nul
del /s /q *~ 2>nul

echo Cleaning system files...
del /s /q Thumbs.db 2>nul
del /s /q desktop.ini 2>nul
del /s /q .DS_Store 2>nul

echo Cleaning debug files...
del debug_*.py 2>nul
del *_debug.py 2>nul
del *_temp.py 2>nul
del temp_*.txt 2>nul

echo.
echo ✅ Cleanup completed!
echo.
pause
