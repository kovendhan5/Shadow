# browser.py
import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import DEFAULT_BROWSER, BROWSER_TIMEOUT, HEADLESS_MODE

# Optional webdriver-manager import
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    logging.warning("webdriver-manager not available, using system drivers")
    WEBDRIVER_MANAGER_AVAILABLE = False

class BrowserController:
    def __init__(self, browser_type: str = DEFAULT_BROWSER, headless: bool = HEADLESS_MODE):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None
        self.wait = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup the WebDriver based on browser type"""
        try:
            if self.browser_type == "chrome":
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                self.driver = webdriver.Chrome(options=options)
            
            elif self.browser_type == "firefox":
                options = FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Firefox(options=options)
            
            elif self.browser_type == "edge":
                options = EdgeOptions()
                if self.headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Edge(options=options)
            
            else:
                raise ValueError(f"Unsupported browser: {self.browser_type}")
            
            self.wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            self.driver.maximize_window()
            logging.info(f"Browser ({self.browser_type}) initialized successfully")
        
        except Exception as e:
            logging.error(f"Error setting up browser: {e}")
            raise
    
    def navigate_to(self, url: str) -> bool:
        """Navigate to a specific URL"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            logging.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            logging.info(f"Successfully navigated to: {url}")
            return True
        
        except Exception as e:
            logging.error(f"Error navigating to {url}: {e}")
            return False
    
    def find_element(self, selector: str, by: str = By.CSS_SELECTOR, timeout: int = 10):
        """Find an element on the page"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, selector)))
            return element
        except TimeoutException:
            logging.error(f"Element not found: {selector}")
            return None
    
    def click_element(self, selector: str, by: str = By.CSS_SELECTOR) -> bool:
        """Click an element"""
        try:
            element = self.find_element(selector, by)
            if element:
                # Scroll to element if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                # Try to click
                element.click()
                logging.info(f"Successfully clicked element: {selector}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error clicking element {selector}: {e}")
            return False
    
    def type_in_element(self, selector: str, text: str, by: str = By.CSS_SELECTOR, clear_first: bool = True) -> bool:
        """Type text in an element"""
        try:
            element = self.find_element(selector, by)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logging.info(f"Successfully typed text in element: {selector}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error typing in element {selector}: {e}")
            return False
    
    def search_google(self, query: str) -> bool:
        """Search on Google"""
        try:
            self.navigate_to("https://www.google.com")
            
            # Find search box and enter query
            search_box = self.find_element("input[name='q']")
            if search_box:
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results
                time.sleep(2)
                logging.info(f"Google search completed for: {query}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error searching Google: {e}")
            return False
    
    def search_flipkart(self, product: str) -> bool:
        """Search for a product on Flipkart"""
        try:
            self.navigate_to("https://www.flipkart.com")
            
            # Close login popup if present
            try:
                close_btn = self.find_element("button._2KpZ6l._2doB4z", timeout=3)
                if close_btn:
                    close_btn.click()
            except:
                pass
            
            # Find search box and search
            search_box = self.find_element("input[name='q']")
            if search_box:
                search_box.clear()
                search_box.send_keys(product)
                search_box.send_keys(Keys.RETURN)
                
                # Wait for results
                time.sleep(3)
                logging.info(f"Flipkart search completed for: {product}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error searching Flipkart: {e}")
            return False
    
    def open_gmail(self) -> bool:
        """Open Gmail"""
        try:
            self.navigate_to("https://mail.google.com")
            logging.info("Gmail opened")
            return True
        except Exception as e:
            logging.error(f"Error opening Gmail: {e}")
            return False
    
    def open_naukri(self) -> bool:
        """Open Naukri.com"""
        try:
            self.navigate_to("https://www.naukri.com")
            logging.info("Naukri opened")
            return True
        except Exception as e:
            logging.error(f"Error opening Naukri: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take a screenshot of the current page"""
        try:
            if not filename:
                filename = f"screenshot_{int(time.time())}.png"
            
            screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
            self.driver.save_screenshot(screenshot_path)
            
            logging.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return None
    
    def get_page_title(self) -> str:
        """Get the current page title"""
        try:
            return self.driver.title
        except Exception as e:
            logging.error(f"Error getting page title: {e}")
            return ""
    
    def get_current_url(self) -> str:
        """Get the current URL"""
        try:
            return self.driver.current_url
        except Exception as e:
            logging.error(f"Error getting current URL: {e}")
            return ""
    
    def scroll_down(self, pixels: int = 500):
        """Scroll down by specified pixels"""
        try:
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error scrolling: {e}")
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the page"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Error scrolling to bottom: {e}")
    
    def wait_for_element(self, selector: str, by: str = By.CSS_SELECTOR, timeout: int = 10):
        """Wait for an element to be present"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, selector)))
            return element
        except TimeoutException:
            logging.error(f"Timeout waiting for element: {selector}")
            return None
    
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                logging.info("Browser closed")
        except Exception as e:
            logging.error(f"Error closing browser: {e}")
    
    def __del__(self):
        """Destructor to ensure browser is closed"""
        self.close()

# Global browser controller instance
browser_controller = None

def get_browser_controller() -> BrowserController:
    """Get or create browser controller instance"""
    global browser_controller
    if browser_controller is None:
        browser_controller = BrowserController()
    return browser_controller

def open_browser(url: str = None) -> bool:
    """Open browser and optionally navigate to URL"""
    try:
        controller = get_browser_controller()
        if url:
            return controller.navigate_to(url)
        return True
    except Exception as e:
        logging.error(f"Error opening browser: {e}")
        return False

def close_browser():
    """Close the browser"""
    global browser_controller
    if browser_controller:
        browser_controller.close()
        browser_controller = None

def search_product(site: str, product: str) -> bool:
    """Search for a product on specified site"""
    try:
        controller = get_browser_controller()
        if site.lower() == "flipkart":
            return controller.search_flipkart(product)
        elif site.lower() == "google":
            return controller.search_google(product)
        else:
            logging.error(f"Unsupported site: {site}")
            return False
    except Exception as e:
        logging.error(f"Error searching product: {e}")
        return False
