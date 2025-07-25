@echo off
title Shadow AI - Report Generator
echo.
echo ========================================
echo    Shadow AI Report Generator
echo ========================================
echo.

cd /d "K:\Devops\Shadow"

echo Generating comprehensive project report...
echo.

K:/Devops/Shadow/venv/Scripts/python.exe report/generate_report.py

echo.
echo Report generation complete!
echo Check the report/ directory for generated files.
echo.
pause
