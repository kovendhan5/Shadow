@echo off
title Orpheus Emotional AI - Master Launcher
color 5f

:main_menu
cls
echo.
echo  ╔═══════════════════════════════════════════════════════════════════════════════════╗
echo  ║                          🎭 ORPHEUS EMOTIONAL AI 🎭                               ║
echo  ╠═══════════════════════════════════════════════════════════════════════════════════╣
echo  ║                                                                                   ║
echo  ║  🎨  Beautiful Emotional GUI Interface                                            ║
echo  ║  💭  Advanced Empathetic Conversations                                            ║
echo  ║  🧠  Gemini-Powered Emotional Intelligence                                        ║
echo  ║  📊  Real-time Emotion Recognition & Visualization                               ║
echo  ║  🔄  Dual Mode: Orpheus + Shadow AI Integration                                  ║
echo  ║                                                                                   ║
echo  ╚═══════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  Select Orpheus Mode:
echo.
echo  [1] 🎭 Orpheus GUI       - Beautiful emotional interface with visual indicators
echo  [2] 🎬 Orpheus Demo      - Interactive demonstration of emotional AI
echo  [3] 🗣️  Quick Chat        - Simple command-line emotional conversation  
echo  [4] 🔧 Test Orpheus      - Verify Orpheus AI functionality
echo  [5] 📚 About Orpheus     - Learn about the emotional AI system
echo  [6] 🚀 All Shadow GUIs   - Launch all available interfaces
echo  [0] ❌ Exit
echo.
set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" goto launch_gui
if "%choice%"=="2" goto launch_demo
if "%choice%"=="3" goto quick_chat
if "%choice%"=="4" goto test_orpheus
if "%choice%"=="5" goto about_orpheus
if "%choice%"=="6" goto all_guis
if "%choice%"=="0" goto exit
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto main_menu

:launch_gui
cls
echo.
echo  🎭 Starting Orpheus Emotional GUI...
echo  ═══════════════════════════════════════
echo  [INFO] Loading emotional intelligence engine...
echo  [INFO] Initializing Gemini API connection...
echo  [INFO] Preparing visual emotion indicators...
echo  [INFO] Starting beautiful GUI interface...
echo.
python gui_orpheus.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error launching Orpheus GUI
    echo Check your Python installation and Gemini API key configuration
    pause
)
goto main_menu

:launch_demo
cls
echo.
echo  🎬 Starting Orpheus Interactive Demo...
echo  ═══════════════════════════════════════════
echo  [INFO] Preparing emotional conversation scenarios...
echo  [INFO] Loading empathy models...
echo  [INFO] Starting demonstration...
echo.
python demo_orpheus.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error running Orpheus demo
    echo Check your configuration and try again
    pause
)
goto main_menu

:quick_chat
cls
echo.
echo  🗣️  Quick Orpheus Chat Session
echo  ════════════════════════════════
echo  [INFO] Starting emotional conversation...
echo  [INFO] Type your messages to chat with Orpheus
echo  [INFO] Orpheus will respond with emotional intelligence
echo.
python -c "
import sys, os
sys.path.append(os.path.dirname(os.path.abspath('.')))
from brain.orpheus_ai import chat_with_orpheus, get_orpheus_greeting, get_orpheus_emotional_state
print('🎭 ' + get_orpheus_greeting())
print('📊 Current state:', get_orpheus_emotional_state())
print('\nType your message (or \"quit\" to exit):')
while True:
    try:
        msg = input('\n👤 You: ')
        if msg.lower() == 'quit': break
        response = chat_with_orpheus(msg)
        print('🎭 Orpheus:', response)
        print('📊 State:', get_orpheus_emotional_state())
    except KeyboardInterrupt:
        print('\n👋 Goodbye!')
        break
    except Exception as e:
        print('Error:', e)
        break
"
goto main_menu

:test_orpheus
cls
echo.
echo  🔧 Testing Orpheus AI Components...
echo  ═══════════════════════════════════════
echo  [INFO] Running system diagnostics...
echo.

echo [1/4] Testing Python environment...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found or not working
    pause
    goto main_menu
)

echo [2/4] Testing Orpheus AI import...
python -c "from brain.orpheus_ai import EmotionalAI; print('✅ Orpheus AI imports successfully')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Orpheus AI import failed
    echo Check your installation and dependencies
    pause
    goto main_menu
)

echo [3/4] Testing Gemini API configuration...
python -c "from config import GEMINI_API_KEY; print('✅ API key configured' if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_key_here' else '❌ API key not configured')"

echo [4/4] Testing Orpheus functionality...
python -c "
try:
    from brain.orpheus_ai import EmotionalAI
    ai = EmotionalAI()
    print('✅ Orpheus AI initialized successfully')
    print('📊 Current emotional state:', ai.get_emotional_state_description())
except Exception as e:
    print('❌ Orpheus test failed:', e)
"

echo.
echo Testing complete!
pause
goto main_menu

:about_orpheus
cls
echo.
echo  📚 About Orpheus Emotional AI
echo  ═══════════════════════════════════════════════════════════════════════════════════
echo.
echo  🎭 WHAT IS ORPHEUS?
echo  Orpheus is an advanced emotional AI system that understands and responds to human
echo  emotions with empathy and intelligence. Named after the legendary musician who
echo  could move hearts with his art, Orpheus AI creates meaningful emotional connections.
echo.
echo  🧠 KEY FEATURES:
echo  • Emotion Recognition: Analyzes user sentiment and emotional state
echo  • Adaptive Responses: Adjusts communication style based on detected emotions  
echo  • Visual Indicators: Beautiful animated emotion displays in the GUI
echo  • Conversation Memory: Maintains context and emotional continuity
echo  • Dual Intelligence: Can switch between Orpheus (emotional) and Shadow (functional) AI
echo  • Gemini Integration: Powered by Google's advanced Gemini AI model
echo.
echo  💝 EMOTIONAL TYPES SUPPORTED:
echo  Happy, Sad, Excited, Calm, Curious, Empathetic, Confident, Playful,
echo  Thoughtful, Encouraging, Surprised, Concerned, and many more...
echo.
echo  🎨 TECHNICAL DETAILS:
echo  • Built with Python and Tkinter for beautiful cross-platform GUIs
echo  • Uses Google Gemini API for natural language processing
echo  • Real-time emotion detection and response generation
echo  • Conversation export and analytics features
echo  • Thread-safe asynchronous processing
echo.
echo  🚀 GETTING STARTED:
echo  1. Configure your Gemini API key in the .env file
echo  2. Choose 'Orpheus GUI' for the full visual experience
echo  3. Start chatting and watch Orpheus respond emotionally!
echo.
pause
goto main_menu

:all_guis
cls
echo.
echo  🚀 Launching All Shadow AI Interfaces...
echo  ═══════════════════════════════════════════
echo  [INFO] This will open all available GUI interfaces
echo  [INFO] You can choose which ones to use
echo.
call launch_all_guis.bat
goto main_menu

:exit
cls
echo.
echo  ╔═══════════════════════════════════════════════════════════════════════════════════╗
echo  ║                          Thank you for using Orpheus! 🎭                         ║
echo  ║                                                                                   ║
echo  ║  💝 Orpheus hopes your conversations were meaningful and emotionally enriching    ║
echo  ║  🌟 Remember: Emotional intelligence makes all interactions more human            ║
echo  ║  🎭 Until next time, may your conversations be filled with empathy and joy!      ║
echo  ║                                                                                   ║
echo  ╚═══════════════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 3 >nul
exit
