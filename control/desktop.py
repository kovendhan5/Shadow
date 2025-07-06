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

def type_text(text):
    try:
        pyautogui.typewrite(text)
    except Exception as e:
        print(f"Error typing text: {e}")

def click_at(x, y):
    try:
        pyautogui.click(x, y)
    except Exception as e:
        print(f"Error clicking at ({x}, {y}): {e}")
