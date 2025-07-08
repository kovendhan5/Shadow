# advanced_vision.py
"""
Advanced Computer Vision System for Shadow AI
Provides intelligent screen understanding and element detection
"""

import logging
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
import base64
import io
from typing import Dict, List, Tuple, Optional, Any
import json
import requests
from brain.gpt_agent import agent

class AdvancedVision:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        # Configure tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
    def take_screenshot(self) -> Image.Image:
        """Take a screenshot and return as PIL Image"""
        screenshot = pyautogui.screenshot()
        return screenshot
    
    def extract_text_from_screen(self, region: Tuple[int, int, int, int] = None) -> str:
        """Extract text from screen using OCR"""
        try:
            screenshot = self.take_screenshot()
            
            if region:
                # Crop to specific region (x, y, width, height)
                screenshot = screenshot.crop(region)
            
            # Enhance image for better OCR
            screenshot = self.enhance_for_ocr(screenshot)
            
            # Extract text
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
        
        except Exception as e:
            logging.error(f"Error extracting text: {e}")
            return ""
    
    def enhance_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image for better OCR accuracy"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image
    
    def find_text_on_screen(self, target_text: str) -> Optional[Tuple[int, int]]:
        """Find text on screen and return its center coordinates"""
        try:
            screenshot = self.take_screenshot()
            
            # Get text with bounding boxes
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
            
            for i, text in enumerate(data['text']):
                if target_text.lower() in text.lower() and int(data['conf'][i]) > 30:
                    # Calculate center of text
                    x = data['left'][i] + data['width'][i] // 2
                    y = data['top'][i] + data['height'][i] // 2
                    return (x, y)
            
            return None
        
        except Exception as e:
            logging.error(f"Error finding text: {e}")
            return None
    
    def describe_screen(self) -> str:
        """Use AI to describe what's currently on screen"""
        try:
            screenshot = self.take_screenshot()
            
            # Convert to base64 for AI analysis
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Use AI to analyze the screen
            prompt = """Analyze this screenshot and describe:
            1. What applications/windows are open
            2. What UI elements are visible (buttons, menus, forms)
            3. What text content is visible
            4. What actions the user might want to perform
            
            Be specific about clickable elements and their locations."""
            
            # Note: This would work with GPT-4 Vision or similar
            # For now, we'll use OCR text as fallback
            screen_text = self.extract_text_from_screen()
            return f"Screen contains text: {screen_text[:500]}..."
        
        except Exception as e:
            logging.error(f"Error describing screen: {e}")
            return "Unable to analyze screen"
    
    def find_clickable_elements(self) -> List[Dict[str, Any]]:
        """Find potential clickable elements on screen"""
        elements = []
        
        try:
            screenshot = self.take_screenshot()
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Find potential buttons/clickable areas
            # This is a simplified approach - in practice you'd use more sophisticated detection
            
            # Look for rectangular regions that might be buttons
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 100 < area < 10000:  # Reasonable button size
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x = x + w // 2
                    center_y = y + h // 2
                    
                    elements.append({
                        'type': 'potential_button',
                        'center': (center_x, center_y),
                        'bounds': (x, y, w, h),
                        'area': area
                    })
            
            return elements[:20]  # Limit to top 20 elements
        
        except Exception as e:
            logging.error(f"Error finding elements: {e}")
            return []
    
    def smart_click(self, description: str) -> bool:
        """Intelligently click on an element based on description"""
        try:
            # First try to find by text
            if text_pos := self.find_text_on_screen(description):
                pyautogui.click(text_pos[0], text_pos[1])
                logging.info(f"Clicked on text: {description} at {text_pos}")
                return True
            
            # If text not found, analyze screen and try to find similar elements
            screen_description = self.describe_screen()
            
            # Use AI to help identify where to click
            prompt = f"""
            Looking at this screen: {screen_description}
            User wants to click on: {description}
            
            Based on the screen content, suggest the most likely location or element name to click.
            Respond with just the element name or text that should be clicked.
            """
            
            ai_suggestion = agent.generate_response(prompt) if agent.client_available else ""
            
            if ai_suggestion and len(ai_suggestion) < 50:
                if suggestion_pos := self.find_text_on_screen(ai_suggestion):
                    pyautogui.click(suggestion_pos[0], suggestion_pos[1])
                    logging.info(f"Clicked on AI suggestion: {ai_suggestion} at {suggestion_pos}")
                    return True
            
            logging.warning(f"Could not find element to click: {description}")
            return False
        
        except Exception as e:
            logging.error(f"Error in smart click: {e}")
            return False
    
    def analyze_screen_for_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze screen to understand how to complete a task"""
        try:
            screenshot = self.take_screenshot()
            screen_text = self.extract_text_from_screen()
            clickable_elements = self.find_clickable_elements()
            
            # Use AI to analyze what actions are needed
            prompt = f"""
            Task: {task_description}
            Screen text: {screen_text[:1000]}
            Number of clickable elements: {len(clickable_elements)}
            
            Analyze this screen and suggest the next action to complete the task.
            Respond with JSON:
            {{
                "action": "click|type|scroll|wait",
                "target": "element description or text to click",
                "text_to_type": "text if typing",
                "explanation": "why this action is needed"
            }}
            """
            
            if agent.client_available:
                response = agent.generate_response(prompt)
                try:
                    analysis = json.loads(response)
                    return analysis
                except json.JSONDecodeError:
                    pass
            
            # Fallback analysis
            return {
                "action": "analyze",
                "target": "screen",
                "explanation": f"Found {len(clickable_elements)} potential clickable elements"
            }
        
        except Exception as e:
            logging.error(f"Error analyzing screen: {e}")
            return {"action": "error", "explanation": str(e)}

# Global instance
advanced_vision = AdvancedVision()
