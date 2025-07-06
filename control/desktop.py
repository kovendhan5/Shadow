import pyautogui
import platform
import subprocess

def open_notepad():
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["notepad.exe"])
        else:
            # Add support for other OS if needed
            print("Unsupported OS")
    except Exception as e:
        print(f"Error opening notepad: {e}")
