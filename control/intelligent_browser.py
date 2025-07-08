# intelligent_browser.py
"""
Intelligent Web Browsing System for Shadow AI
Provides smart web navigation, content extraction, and task automation
"""

import logging
import time
import re
import json
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from brain.gpt_agent import agent

class IntelligentBrowser:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.current_url = ""
        
    def start_browser(self) -> bool:
        """Start the browser with intelligent settings"""
        try:
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            
            # Add intelligent browser options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent to appear more human-like
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            
            logging.info("Intelligent browser started successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error starting browser: {e}")
            return False
    
    def navigate_to(self, url: str) -> bool:
        """Navigate to URL with intelligent handling"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.driver.get(url)
            self.current_url = self.driver.current_url
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            logging.info(f"Navigated to: {self.current_url}")
            return True
            
        except Exception as e:
            logging.error(f"Error navigating to {url}: {e}")
            return False
    
    def intelligent_search(self, query: str, site: str = "google.com") -> bool:
        """Perform intelligent search on specified site"""
        try:
            if site.lower() == "google.com":
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            elif site.lower() == "amazon.com":
                search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
            elif site.lower() == "youtube.com":
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            else:
                # Generic search - go to site and find search box
                if not self.navigate_to(site):
                    return False
                return self.find_and_use_search_box(query)
            
            return self.navigate_to(search_url)
            
        except Exception as e:
            logging.error(f"Error in intelligent search: {e}")
            return False
    
    def find_and_use_search_box(self, query: str) -> bool:
        """Find search box on any website and use it"""
        try:
            # Common search box selectors
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='search' i]",
                "input[name*='search' i]",
                "input[id*='search' i]",
                "#search", ".search-input", ".search-box"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if search_box:
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                logging.info(f"Searched for: {query}")
                return True
            else:
                logging.warning("No search box found on page")
                return False
                
        except Exception as e:
            logging.error(f"Error finding search box: {e}")
            return False
    
    def extract_page_content(self) -> Dict[str, Any]:
        """Extract meaningful content from current page"""
        try:
            content = {
                "title": self.driver.title,
                "url": self.current_url,
                "text": "",
                "links": [],
                "images": [],
                "forms": [],
                "buttons": []
            }
            
            # Extract main text content
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            content["text"] = soup.get_text()[:2000]  # Limit text length
            
            # Extract links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links[:20]:  # Limit to first 20 links
                href = link.get_attribute("href")
                text = link.text.strip()
                if href and text:
                    content["links"].append({"text": text, "href": href})
            
            # Extract images
            images = self.driver.find_elements(By.TAG_NAME, "img")
            for img in images[:10]:  # Limit to first 10 images
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                if src:
                    content["images"].append({"src": src, "alt": alt or ""})
            
            # Extract forms
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            for form in forms:
                inputs = form.find_elements(By.TAG_NAME, "input")
                form_data = []
                for inp in inputs:
                    input_type = inp.get_attribute("type")
                    name = inp.get_attribute("name")
                    placeholder = inp.get_attribute("placeholder")
                    form_data.append({
                        "type": input_type,
                        "name": name,
                        "placeholder": placeholder
                    })
                content["forms"].append(form_data)
            
            # Extract buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons[:10]:  # Limit to first 10 buttons
                text = btn.text.strip()
                if text:
                    content["buttons"].append(text)
            
            return content
            
        except Exception as e:
            logging.error(f"Error extracting content: {e}")
            return {"error": str(e)}
    
    def intelligent_click(self, description: str) -> bool:
        """Intelligently click on an element based on description"""
        try:
            # Try different strategies to find the element
            
            # Strategy 1: Find by exact text
            try:
                element = self.driver.find_element(By.XPATH, f"//*[text()='{description}']")
                element.click()
                logging.info(f"Clicked element with text: {description}")
                return True
            except NoSuchElementException:
                pass
            
            # Strategy 2: Find by partial text
            try:
                element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{description}')]")
                element.click()
                logging.info(f"Clicked element containing text: {description}")
                return True
            except NoSuchElementException:
                pass
            
            # Strategy 3: Find by attributes
            for attr in ['aria-label', 'title', 'alt', 'value']:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[@{attr}='{description}']")
                    element.click()
                    logging.info(f"Clicked element with {attr}: {description}")
                    return True
                except NoSuchElementException:
                    continue
            
            # Strategy 4: Use AI to analyze page and suggest element
            if agent.client_available:
                content = self.extract_page_content()
                prompt = f"""
                Page content: {content}
                User wants to click: {description}
                
                Suggest the best CSS selector or XPath to find this element.
                Respond with just the selector.
                """
                
                suggestion = agent.generate_response(prompt)
                if suggestion and len(suggestion) < 200:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, suggestion)
                        element.click()
                        logging.info(f"Clicked using AI suggestion: {suggestion}")
                        return True
                    except:
                        pass
            
            logging.warning(f"Could not find element to click: {description}")
            return False
            
        except Exception as e:
            logging.error(f"Error in intelligent click: {e}")
            return False
    
    def smart_form_fill(self, form_data: Dict[str, str]) -> bool:
        """Intelligently fill out forms"""
        try:
            filled_fields = 0
            
            for field_name, value in form_data.items():
                # Try different strategies to find form fields
                field_found = False
                
                # Strategy 1: Find by name attribute
                try:
                    field = self.driver.find_element(By.NAME, field_name)
                    field.clear()
                    field.send_keys(value)
                    filled_fields += 1
                    field_found = True
                except NoSuchElementException:
                    pass
                
                # Strategy 2: Find by id
                if not field_found:
                    try:
                        field = self.driver.find_element(By.ID, field_name)
                        field.clear()
                        field.send_keys(value)
                        filled_fields += 1
                        field_found = True
                    except NoSuchElementException:
                        pass
                
                # Strategy 3: Find by placeholder text
                if not field_found:
                    try:
                        field = self.driver.find_element(By.XPATH, f"//input[@placeholder='{field_name}']")
                        field.clear()
                        field.send_keys(value)
                        filled_fields += 1
                        field_found = True
                    except NoSuchElementException:
                        pass
                
                if not field_found:
                    logging.warning(f"Could not find field: {field_name}")
            
            logging.info(f"Filled {filled_fields} form fields")
            return filled_fields > 0
            
        except Exception as e:
            logging.error(f"Error filling form: {e}")
            return False
    
    def execute_web_task(self, task_description: str) -> Dict[str, Any]:
        """Execute complex web tasks using AI"""
        try:
            # Analyze current page
            content = self.extract_page_content()
            
            # Use AI to plan the task
            prompt = f"""
            Current page: {content.get('title', '')} at {content.get('url', '')}
            Task: {task_description}
            Available elements: {content.get('buttons', [])}
            Available links: {[link['text'] for link in content.get('links', [])[:10]]}
            
            Plan the steps to complete this task. Respond with JSON:
            {{
                "steps": [
                    {{"action": "click", "target": "button text or link text"}},
                    {{"action": "type", "target": "field name", "text": "text to type"}},
                    {{"action": "navigate", "url": "url to go to"}}
                ],
                "explanation": "why these steps will complete the task"
            }}
            """
            
            if agent.client_available:
                response = agent.generate_response(prompt)
                try:
                    plan = json.loads(response)
                    return self.execute_task_plan(plan)
                except json.JSONDecodeError:
                    pass
            
            return {"success": False, "error": "Could not generate task plan"}
            
        except Exception as e:
            logging.error(f"Error executing web task: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_task_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a planned sequence of web actions"""
        try:
            results = []
            
            for step in plan.get('steps', []):
                action = step.get('action')
                target = step.get('target')
                
                if action == 'click':
                    success = self.intelligent_click(target)
                    results.append(f"Click {target}: {'Success' if success else 'Failed'}")
                    
                elif action == 'type':
                    text = step.get('text', '')
                    success = self.smart_form_fill({target: text})
                    results.append(f"Type in {target}: {'Success' if success else 'Failed'}")
                    
                elif action == 'navigate':
                    url = step.get('url', target)
                    success = self.navigate_to(url)
                    results.append(f"Navigate to {url}: {'Success' if success else 'Failed'}")
                
                # Small delay between actions
                time.sleep(1)
            
            return {
                "success": True,
                "results": results,
                "explanation": plan.get('explanation', '')
            }
            
        except Exception as e:
            logging.error(f"Error executing task plan: {e}")
            return {"success": False, "error": str(e)}
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")

# Global instance
intelligent_browser = IntelligentBrowser()
