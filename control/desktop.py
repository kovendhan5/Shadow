import pyautogui
import platform
import subprocess
import logging
import time
import os
from config import DESKTOP_PATH

# Optional imports with fallbacks
try:
    from pynput import keyboard, mouse
    from pynput.keyboard import Key, Listener
    PYNPUT_AVAILABLE = True
except ImportError:
    logging.warning("pynput not available, some features may be limited")
    PYNPUT_AVAILABLE = False

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    logging.warning("win32gui not available, some Windows features may be limited")
    WIN32_AVAILABLE = False

# Configure pyautogui
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

class DesktopController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        logging.info(f"Screen resolution: {self.screen_width}x{self.screen_height}")
    
    def open_application(self, app_name: str) -> bool:
        """Open an application by name"""
        try:
            app_name = app_name.lower()
            
            if app_name == "notepad":
                return self.open_notepad()
            elif app_name == "calculator":
                return self.open_calculator()
            elif app_name == "paint":
                return self.open_paint()
            elif app_name == "cmd" or app_name == "command prompt":
                return self.open_cmd()
            elif app_name == "explorer" or app_name == "file explorer":
                return self.open_explorer()
            elif app_name == "chrome" or app_name == "google chrome":
                return self.open_chrome()
            elif app_name == "firefox":
                return self.open_firefox()
            elif app_name == "edge":
                return self.open_edge()
            else:
                # Try to open using Windows search
                return self.open_via_search(app_name)
        
        except Exception as e:
            logging.error(f"Error opening application {app_name}: {e}")
            return False
    
    def open_notepad(self) -> bool:
        """Open Notepad"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["notepad.exe"])
                logging.info("Opened Notepad")
                return True
            else:
                logging.error("Notepad is Windows-specific")
                return False
        except Exception as e:
            logging.error(f"Error opening Notepad: {e}")
            return False
    
    def open_calculator(self) -> bool:
        """Open Calculator"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["calc.exe"])
                logging.info("Opened Calculator")
                return True
            else:
                logging.error("Calculator command is Windows-specific")
                return False
        except Exception as e:
            logging.error(f"Error opening Calculator: {e}")
            return False
    
    def open_paint(self) -> bool:
        """Open Paint"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["mspaint.exe"])
                logging.info("Opened Paint")
                return True
            else:
                logging.error("Paint is Windows-specific")
                return False
        except Exception as e:
            logging.error(f"Error opening Paint: {e}")
            return False
    
    def open_cmd(self) -> bool:
        """Open Command Prompt"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["cmd.exe"])
                logging.info("Opened Command Prompt")
                return True
            else:
                logging.error("CMD is Windows-specific")
                return False
        except Exception as e:
            logging.error(f"Error opening CMD: {e}")
            return False
    
    def open_explorer(self) -> bool:
        """Open File Explorer"""
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["explorer.exe"])
                logging.info("Opened File Explorer")
                return True
            else:
                logging.error("Explorer is Windows-specific")
                return False
        except Exception as e:
            logging.error(f"Error opening Explorer: {e}")
            return False
    
    def open_chrome(self) -> bool:
        """Open Google Chrome"""
        try:
            chrome_paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    logging.info("Opened Chrome")
                    return True
            
            # Try via Windows search
            return self.open_via_search("chrome")
        
        except Exception as e:
            logging.error(f"Error opening Chrome: {e}")
            return False
    
    def open_firefox(self) -> bool:
        """Open Firefox"""
        try:
            firefox_paths = [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
            ]
            
            for path in firefox_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    logging.info("Opened Firefox")
                    return True
            
            return self.open_via_search("firefox")
        
        except Exception as e:
            logging.error(f"Error opening Firefox: {e}")
            return False
    
    def open_edge(self) -> bool:
        """Open Microsoft Edge"""
        try:
            subprocess.Popen(["msedge.exe"])
            logging.info("Opened Edge")
            return True
        except Exception as e:
            logging.error(f"Error opening Edge: {e}")
            return self.open_via_search("edge")
    
    def open_via_search(self, app_name: str) -> bool:
        """Open application via Windows search"""
        try:
            # Press Windows key
            pyautogui.press('win')
            time.sleep(1)
            
            # Type application name
            pyautogui.typewrite(app_name)
            time.sleep(1)
            
            # Press Enter
            pyautogui.press('enter')
            time.sleep(2)
            
            logging.info(f"Attempted to open {app_name} via Windows search")
            return True
        
        except Exception as e:
            logging.error(f"Error opening {app_name} via search: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.1) -> bool:
        """Type text with specified interval between characters"""
        try:
            pyautogui.typewrite(text, interval=interval)
            logging.info(f"Typed text: {text[:50]}...")
            return True
        except Exception as e:
            logging.error(f"Error typing text: {e}")
            return False
    
    def click_at(self, x: int, y: int, button: str = 'left', clicks: int = 1) -> bool:
        """Click at specific coordinates"""
        try:
            if 0 <= x <= self.screen_width and 0 <= y <= self.screen_height:
                pyautogui.click(x, y, button=button, clicks=clicks)
                logging.info(f"Clicked at ({x}, {y}) with {button} button")
                return True
            else:
                logging.error(f"Click coordinates ({x}, {y}) are out of screen bounds")
                return False
        except Exception as e:
            logging.error(f"Error clicking at ({x}, {y}): {e}")
            return False
    
    def double_click_at(self, x: int, y: int) -> bool:
        """Double-click at specific coordinates"""
        return self.click_at(x, y, clicks=2)
    
    def right_click_at(self, x: int, y: int) -> bool:
        """Right-click at specific coordinates"""
        return self.click_at(x, y, button='right')
    
    def drag_to(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """Drag from start coordinates to end coordinates"""
        try:
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=1, button='left')
            logging.info(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
        except Exception as e:
            logging.error(f"Error dragging: {e}")
            return False
    
    def scroll(self, direction: str = 'up', clicks: int = 3) -> bool:
        """Scroll up or down"""
        try:
            if direction.lower() == 'up':
                pyautogui.scroll(clicks)
            elif direction.lower() == 'down':
                pyautogui.scroll(-clicks)
            else:
                logging.error(f"Invalid scroll direction: {direction}")
                return False
            
            logging.info(f"Scrolled {direction} {clicks} clicks")
            return True
        except Exception as e:
            logging.error(f"Error scrolling: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press a single key"""
        try:
            pyautogui.press(key)
            logging.info(f"Pressed key: {key}")
            return True
        except Exception as e:
            logging.error(f"Error pressing key {key}: {e}")
            return False
    
    def press_key_combination(self, keys: list) -> bool:
        """Press a combination of keys"""
        try:
            pyautogui.hotkey(*keys)
            logging.info(f"Pressed key combination: {' + '.join(keys)}")
            return True
        except Exception as e:
            logging.error(f"Error pressing key combination {keys}: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot and save it"""
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            screenshot_path = os.path.join(DESKTOP_PATH, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            logging.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return None
    
    def find_on_screen(self, image_path: str, confidence: float = 0.8):
        """Find an image on screen and return its location"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                logging.info(f"Found image at: {center}")
                return center
            else:
                logging.warning(f"Image not found: {image_path}")
                return None
        except Exception as e:
            logging.error(f"Error finding image on screen: {e}")
            return None
    
    def click_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """Find and click an image on screen"""
        try:
            location = self.find_on_screen(image_path, confidence)
            if location:
                pyautogui.click(location)
                logging.info(f"Clicked on image: {image_path}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error clicking image: {e}")
            return False
    
    def get_active_window_title(self) -> str:
        """Get the title of the active window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            return window_title
        except Exception as e:
            logging.error(f"Error getting active window title: {e}")
            return ""
    
    def minimize_window(self) -> bool:
        """Minimize the active window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            logging.info("Minimized active window")
            return True
        except Exception as e:
            logging.error(f"Error minimizing window: {e}")
            return False
    
    def maximize_window(self) -> bool:
        """Maximize the active window"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            logging.info("Maximized active window")
            return True
        except Exception as e:
            logging.error(f"Error maximizing window: {e}")
            return False
    
    def close_window(self) -> bool:
        """Close the active window"""
        try:
            self.press_key_combination(['alt', 'f4'])
            logging.info("Closed active window")
            return True
        except Exception as e:
            logging.error(f"Error closing window: {e}")
            return False
    
    def is_notepad_open(self) -> bool:
        """Check if Notepad is currently open"""
        try:
            if WIN32_AVAILABLE:
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_title = win32gui.GetWindowText(hwnd)
                        class_name = win32gui.GetClassName(hwnd)
                        if "Notepad" in window_title or class_name == "Notepad":
                            windows.append(hwnd)
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                return len(windows) > 0
            else:
                # Fallback method using pyautogui
                import pyautogui
                windows = pyautogui.getWindowsWithTitle("Notepad")
                return len(windows) > 0
        except Exception as e:
            logging.error(f"Error checking if Notepad is open: {e}")
            return False
    
    def activate_notepad(self) -> bool:
        """Activate existing Notepad window"""
        try:
            if WIN32_AVAILABLE:
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_title = win32gui.GetWindowText(hwnd)
                        class_name = win32gui.GetClassName(hwnd)
                        if "Notepad" in window_title or class_name == "Notepad":
                            windows.append(hwnd)
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                
                if windows:
                    # Activate the first Notepad window found
                    hwnd = windows[0]
                    win32gui.SetForegroundWindow(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    return True
            else:
                # Fallback method using pyautogui
                import pyautogui
                windows = pyautogui.getWindowsWithTitle("Notepad")
                if windows:
                    windows[0].activate()
                    return True
            
            return False
        except Exception as e:
            logging.error(f"Error activating Notepad: {e}")
            return False
    
    def open_or_activate_notepad(self) -> bool:
        """Open Notepad if not open, or activate if already open"""
        try:
            if self.is_notepad_open():
                logging.info("Notepad is already open, activating it")
                return self.activate_notepad()
            else:
                logging.info("Opening new Notepad window")
                return self.open_notepad()
        except Exception as e:
            logging.error(f"Error opening or activating Notepad: {e}")
            return False
    
    def select_all(self) -> bool:
        """Select all text in the current window"""
        try:
            pyautogui.keyDown('ctrl')
            pyautogui.press('a')
            pyautogui.keyUp('ctrl')
            logging.info("Selected all text")
            return True
        except Exception as e:
            logging.error(f"Error selecting all text: {e}")
            return False

# Global desktop controller instance
desktop_controller = DesktopController()

# Exported functions for backward compatibility and convenience
def open_notepad() -> bool:
    """Open Notepad"""
    return desktop_controller.open_notepad()

def type_text(text: str) -> bool:
    """Type text"""
    return desktop_controller.type_text(text)

def click_at(x: int, y: int) -> bool:
    """Click at coordinates"""
    return desktop_controller.click_at(x, y)

def open_application(app_name: str) -> bool:
    """Open an application"""
    return desktop_controller.open_application(app_name)

def take_screenshot(filename: str = None) -> str:
    """Take a screenshot"""
    return desktop_controller.take_screenshot(filename)

def press_key(key: str) -> bool:
    """Press a key"""
    return desktop_controller.press_key(key)

def press_key_combination(keys: list) -> bool:
    """Press key combination"""
    return desktop_controller.press_key_combination(keys)
