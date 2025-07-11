import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

class WhatsAppAutomator:
    def __init__(self, app_path=None):
        self.app_path = app_path or r"C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
        self.app = None

    def open_whatsapp(self):
        try:
            self.app = Application(backend="uia").start(self.app_path)
            time.sleep(5)
            return True
        except Exception as e:
            print(f"❌ Could not open WhatsApp: {e}")
            return False

    def send_message(self, contact, message):
        try:
            if not self.app:
                self.open_whatsapp()
            win = self.app.window(title_re=".*WhatsApp.*")
            win.wait('visible', timeout=15)
            search_box = win.child_window(title="Search or start new chat", control_type="Edit")
            search_box.set_edit_text(contact)
            time.sleep(1)
            send_keys('{ENTER}')
            time.sleep(1)
            input_box = win.child_window(auto_id="input-chatlist-search", control_type="Edit")
            input_box.set_edit_text(message)
            send_keys('{ENTER}')
            print(f"✅ Message sent to {contact}")
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
