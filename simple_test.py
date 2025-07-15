#!/usr/bin/env python3
"""
Simple test script to run Shadow AI in non-GUI mode
"""

import os
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def print_header():
    """Print a colorful header"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}      🧠 Shadow AI - Command Line Test Runner")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}\n")

def test_shadow_ai():
    """Run a simple test of Shadow AI's core functionality"""
    try:
        print(f"{Fore.YELLOW}Importing Shadow AI components...")
        from main import ShadowAI
        print(f"{Fore.GREEN}✅ Import successful!")
        
        print(f"{Fore.YELLOW}Initializing Shadow AI...")
        shadow = ShadowAI()
        print(f"{Fore.GREEN}✅ Initialization successful!")
        
        # Test simple command
        test_command = "Take a screenshot"
        print(f"{Fore.YELLOW}Testing command: '{test_command}'")
        result = shadow.process_ai_command(test_command)
        
        print(f"{Fore.GREEN}Command executed:")
        print(f"{Fore.WHITE}Result: {result}")
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 Test completed successfully!")
        print(f"{Fore.GREEN}Shadow AI is operational.")
        return True
    
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print_header()
    
    # Check if dependencies are installed
    try:
        import pyautogui
        import pyttsx3
    except ImportError as e:
        print(f"{Fore.RED}Missing dependency: {e}")
        print(f"{Fore.YELLOW}Please install all dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the test
    success = test_shadow_ai()
    
    print(f"\n{Fore.CYAN}{'=' * 60}")
    if success:
        print(f"{Fore.GREEN}Shadow AI is ready to use!")
        print(f"{Fore.GREEN}Try running 'launch_improved_new.bat' for the full experience.")
    else:
        print(f"{Fore.RED}Shadow AI test failed. Please check the error messages above.")
        print(f"{Fore.YELLOW}Make sure you have set up your API keys in the .env file.")
    print(f"{Fore.CYAN}{'=' * 60}")
    
    input(f"\n{Fore.YELLOW}Press Enter to exit...")
