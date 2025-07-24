@echo off
echo ========================================
echo    Shadow AI - Complete Setup & Report Generation
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
echo.

:: Install required packages for PDF processing and project functionality
pip install --upgrade pip
pip install PyPDF2 pdfplumber reportlab
pip install pyautogui selenium webdriver-manager
pip install speechrecognition pyttsx3
pip install tkinter customtkinter
pip install openai google-generativeai
pip install requests beautifulsoup4
pip install opencv-python pillow
pip install numpy pandas
pip install python-dotenv

echo.
echo Step 2: Checking core project components...
echo.

:: Test main application
echo Testing main application...
python -c "import main; print('Main module: OK')" 2>nul || echo "Main module: ERROR"

:: Test brain modules
echo Testing AI brain modules...
python -c "import brain.gpt_agent; print('GPT Agent: OK')" 2>nul || echo "GPT Agent: ERROR"
python -c "import brain.universal_processor; print('Universal Processor: OK')" 2>nul || echo "Universal Processor: ERROR"

:: Test control modules
echo Testing control modules...
python -c "import control.desktop; print('Desktop Control: OK')" 2>nul || echo "Desktop Control: ERROR"
python -c "import control.browser; print('Browser Control: OK')" 2>nul || echo "Browser Control: ERROR"

:: Test input modules
echo Testing input modules...
python -c "import input.voice_input; print('Voice Input: OK')" 2>nul || echo "Voice Input: ERROR"
python -c "import input.text_input; print('Text Input: OK')" 2>nul || echo "Text Input: ERROR"

echo.
echo Step 3: Generating comprehensive project report...
echo.

:: Generate the project report
python create_report.py

echo.
echo Step 4: Testing Shadow AI functionality...
echo.

:: Run quick tests
python quick_test.py

echo.
echo Step 5: Creating demonstration scripts...
echo.

:: Create a demo script
echo Creating demo script...
python -c "
import os
demo_content = '''
# Shadow AI Demonstration Script

print(\"=== Shadow AI Demo ===\")
print(\"1. Voice Recognition Test\")
print(\"2. Desktop Automation Test\") 
print(\"3. AI Integration Test\")
print(\"4. GUI Interface Test\")

try:
    from brain.gpt_agent import GPTAgent
    agent = GPTAgent()
    print(\"AI Agent initialized successfully!\")
except:
    print(\"AI Agent initialization failed - check API keys\")

try:
    from control.desktop import DesktopControl
    desktop = DesktopControl()
    print(\"Desktop control initialized successfully!\")
except:
    print(\"Desktop control initialization failed\")

try:
    from input.voice_input import VoiceInput
    voice = VoiceInput()
    print(\"Voice input initialized successfully!\")
except:
    print(\"Voice input initialization failed\")

print(\"Demo completed!\")
'''

with open('demo_complete.py', 'w') as f:
    f.write(demo_content)
print('Demo script created: demo_complete.py')
"

echo.
echo Step 6: Running the demo...
echo.

python demo_complete.py

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Files created:
echo - Shadow_AI_Project_Report.pdf (Comprehensive project report)
echo - sample_report_text.txt (Extracted sample format)
echo - demo_complete.py (Demonstration script)
echo.
echo To run Shadow AI:
echo   python main.py
echo.
echo To run GUI interface:
echo   python gui/gui_modern.py
echo.
echo To run voice interface:
echo   python input/voice_input.py
echo.
pause
