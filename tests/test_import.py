#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

import sys
import os

def test_imports():
    print("Testing imports...")
    
    try:
        import pyautogui
        print("✅ pyautogui imported successfully")
    except ImportError as e:
        print(f"❌ pyautogui import failed: {e}")
    
    try:
        import pynput
        print("✅ pynput imported successfully")
    except ImportError as e:
        print(f"❌ pynput import failed: {e}")
    
    try:
        import keyboard
        print("✅ keyboard imported successfully")
    except ImportError as e:
        print(f"❌ keyboard import failed: {e}")
    
    try:
        import speech_recognition
        print("✅ speech_recognition imported successfully")
    except ImportError as e:
        print(f"❌ speech_recognition import failed: {e}")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
    
    try:
        import google.generativeai
        print("✅ google.generativeai imported successfully")
    except ImportError as e:
        print(f"❌ google.generativeai import failed: {e}")
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
    
    try:
        import selenium
        print("✅ selenium imported successfully")
    except ImportError as e:
        print(f"❌ selenium import failed: {e}")
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
    except ImportError as e:
        print(f"❌ pytesseract import failed: {e}")
    
    try:
        import cv2
        print("✅ cv2 imported successfully")
    except ImportError as e:
        print(f"❌ cv2 import failed: {e}")
    
    try:
        import numpy
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
    
    try:
        import PIL
        print("✅ PIL imported successfully")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
    
    print("\nNow testing Shadow AI modules...")
    
    try:
        from utils.logging import setup_logging
        print("✅ utils.logging imported successfully")
    except ImportError as e:
        print(f"❌ utils.logging import failed: {e}")
    
    try:
        from utils.confirm import confirm_action
        print("✅ utils.confirm imported successfully")
    except ImportError as e:
        print(f"❌ utils.confirm import failed: {e}")
    
    try:
        from brain.gpt_agent import process_command
        print("✅ brain.gpt_agent imported successfully")
    except ImportError as e:
        print(f"❌ brain.gpt_agent import failed: {e}")
    
    try:
        from brain.universal_processor import process_universal_command
        print("✅ brain.universal_processor imported successfully")
    except ImportError as e:
        print(f"❌ brain.universal_processor import failed: {e}")
    
    try:
        from brain.universal_executor import execute_universal_task
        print("✅ brain.universal_executor imported successfully")
    except ImportError as e:
        print(f"❌ brain.universal_executor import failed: {e}")
    
    try:
        from control.advanced_vision import AdvancedVision
        print("✅ control.advanced_vision imported successfully")
    except ImportError as e:
        print(f"❌ control.advanced_vision import failed: {e}")
    
    try:
        from control.intelligent_browser import IntelligentBrowser
        print("✅ control.intelligent_browser imported successfully")
    except ImportError as e:
        print(f"❌ control.intelligent_browser import failed: {e}")
    
    print("\nAll import tests completed!")

if __name__ == "__main__":
    test_imports()
