# Manual Python PATH Setup Guide

## If you already have Python installed:

### Step 1: Find your Python installation
Common locations to check:
- `C:\Python39\`, `C:\Python310\`, `C:\Python311\`, `C:\Python312\`
- `C:\Program Files\Python39\`, etc.
- `%USERPROFILE%\AppData\Local\Programs\Python\Python39\`, etc.
- Custom installation directory you chose

### Step 2: Add Python to PATH manually

1. **Open System Properties:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - OR Right-click "This PC" → Properties → Advanced system settings

2. **Environment Variables:**
   - Click "Environment Variables..." button
   - In "User variables" section, find and select "PATH"
   - Click "Edit..."

3. **Add Python Paths:**
   - Click "New" and add your Python installation directory (e.g., `C:\Python311\`)
   - Click "New" again and add the Scripts directory (e.g., `C:\Python311\Scripts\`)

4. **Apply Changes:**
   - Click "OK" on all dialogs
   - Restart your command prompt/VS Code

### Step 3: Verify Installation
Open a new command prompt and run:
```cmd
python --version
pip --version
```

## If you need to install Python:

1. **Download Python:**
   - Go to https://python.org/downloads/
   - Download the latest Python 3.11.x version (recommended)

2. **Installation Options:**
   - ✅ Check "Add Python to PATH" 
   - ✅ Check "Install for all users" (if admin)
   - Choose "Customize installation"
   - ✅ Select all optional features

3. **After Installation:**
   - Restart command prompt
   - Verify with `python --version`

## Alternative: Use our installer script
Run: `install_python_proper.bat` (as administrator)

## Quick Test
After Python is working, test Shadow AI:
```cmd
cd "k:\Devops\Shadow"
python -m pip install -r requirements.txt
python quick_test.py
python main.py
```
