import logging
import json
import openai
import google.generativeai as genai
import requests
from typing import Dict, Any, List
from config import (
    OPENAI_API_KEY, GEMINI_API_KEY, OLLAMA_URL, 
    DEFAULT_LLM_PROVIDER, DEFAULT_MODEL
)

class GPTAgent:
    def __init__(self, provider: str = DEFAULT_LLM_PROVIDER):
        self.provider = provider
        self.model = DEFAULT_MODEL.get(provider, "gpt-4")
        self.client_available = False
        try:
            self.setup_client()
            self.client_available = True
        except ValueError as e:
            logging.warning(f"LLM client not available: {e}")
            self.client_available = False
    
    def setup_client(self):
        """Setup the appropriate LLM client based on provider"""
        if self.provider == "openai":
            if not OPENAI_API_KEY or OPENAI_API_KEY == "test_key_not_real" or OPENAI_API_KEY == "your_openai_key_here":
                raise ValueError("OpenAI API key not found or is a placeholder. Please set OPENAI_API_KEY in .env file")
            openai.api_key = OPENAI_API_KEY
        elif self.provider == "gemini":
            if not GEMINI_API_KEY or GEMINI_API_KEY == "test_key_not_real" or GEMINI_API_KEY == "your_gemini_key_here":
                raise ValueError("Gemini API key not found or is a placeholder. Please set GEMINI_API_KEY in .env file")
            genai.configure(api_key=GEMINI_API_KEY)
        elif self.provider == "ollama":
            # Test connection to Ollama
            try:
                response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
                if response.status_code != 200:
                    raise ValueError("Cannot connect to Ollama server")
            except requests.exceptions.RequestException:
                raise ValueError("Cannot connect to Ollama server. Make sure it's running.")
    
    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using the configured LLM provider"""
        if not self.client_available:
            logging.warning("LLM client not available, using fallback response")
            return "I'm sorry, but I don't have access to AI services right now. Please configure your API keys in the .env file."
        
        try:
            if self.provider == "openai":
                return self._openai_generate(prompt, system_prompt)
            elif self.provider == "gemini":
                return self._gemini_generate(prompt, system_prompt)
            elif self.provider == "ollama":
                return self._ollama_generate(prompt, system_prompt)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while processing your request."
    
    def _openai_generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using OpenAI GPT"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    def _gemini_generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using Google Gemini"""
        model = genai.GenerativeModel(self.model)
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text.strip()
    
    def _ollama_generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using Ollama"""
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        data = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=data)
        response.raise_for_status()
        return response.json()["response"].strip()

# System prompt for Shadow AI Agent
SYSTEM_PROMPT = """You are Shadow, a personal AI agent for Windows. Your role is to understand user commands and convert them into actionable tasks.

For each user command, respond with a JSON object containing:
1. "task_type": The type of task (e.g., "document_creation", "web_automation", "desktop_control", "file_operation")
2. "action": Specific action to perform
3. "parameters": Dictionary of parameters needed for the action
4. "confirmation_required": Boolean indicating if user confirmation is needed
5. "description": Human-readable description of what will be done

Available task types and actions:
- document_creation: create_document, save_as_pdf, open_word, open_notepad
- web_automation: open_browser, navigate_to, search_on_site, fill_form, click_element
- desktop_control: open_application, type_text, click_at, take_screenshot
- file_operation: save_file, open_file, move_file, delete_file
- email_automation: compose_email, send_email, read_email
- shopping_automation: search_product, add_to_cart, proceed_to_checkout

Example response:
{
    "task_type": "document_creation",
    "action": "create_document",
    "parameters": {
        "content": "Generated document content",
        "filename": "Leave_Letter.docx",
        "format": "docx"
    },
    "confirmation_required": false,
    "description": "Create a leave letter document and save it as Leave_Letter.docx"
}

Always prioritize user safety and ask for confirmation for sensitive operations like purchases or file deletions."""

# Initialize the agent
agent = GPTAgent()

def process_command(command: str) -> Dict[str, Any]:
    """Process a natural language command and return structured action data"""
    logging.info(f"Processing command: {command}")
    
    try:
        # Use LLM to understand and plan the task if available
        if agent.client_available:
            response = agent.generate_response(command, SYSTEM_PROMPT)
            
            # Try to parse JSON response
            try:
                action_data = json.loads(response)
                logging.info(f"Generated action: {action_data}")
                return action_data
            except json.JSONDecodeError:
                # Fallback to simple command parsing
                logging.warning("LLM response was not valid JSON, falling back to simple parsing")
                return _fallback_command_parsing(command)
        else:
            # Use fallback parsing when LLM is not available
            logging.info("LLM not available, using fallback command parsing")
            return _fallback_command_parsing(command)
    
    except Exception as e:
        logging.error(f"Error in command processing: {e}")
        return _fallback_command_parsing(command)

def _fallback_command_parsing(command: str) -> Dict[str, Any]:
    """Fallback command parsing for simple commands"""
    command_lower = command.lower()
    
    if "open notepad" in command_lower and "write" in command_lower:
        # Extract the content to write
        if "write an article about" in command_lower:
            topic = command_lower.split("write an article about")[1].strip()
            return {
                "task_type": "document_creation",
                "action": "create_article",
                "parameters": {
                    "topic": topic,
                    "format": "text",
                    "open_in_notepad": True
                },
                "confirmation_required": False,
                "description": f"Open Notepad and write an article about {topic}"
            }
        elif "write" in command_lower:
            # Extract text after "write"
            write_parts = command_lower.split("write")
            if len(write_parts) > 1:
                content = write_parts[1].strip()
                return {
                    "task_type": "desktop_control",
                    "action": "open_notepad_and_type",
                    "parameters": {"text": content},
                    "confirmation_required": False,
                    "description": f"Open Notepad and write: {content[:50]}..."
                }
    elif "open notepad" in command_lower:
        return {
            "task_type": "desktop_control",
            "action": "open_notepad",
            "parameters": {},
            "confirmation_required": False,
            "description": "Open Notepad application"
        }
    elif "write a leave letter" in command_lower:
        return {
            "task_type": "document_creation",
            "action": "create_leave_letter",
            "parameters": {"reason": "personal reasons"},
            "confirmation_required": False,
            "description": "Create a leave letter document"
        }
    elif "write an article about" in command_lower:
        topic = command_lower.split("write an article about")[1].strip()
        return {
            "task_type": "desktop_control",
            "action": "open_notepad_and_write_article",
            "parameters": {"topic": topic},
            "confirmation_required": False,
            "description": f"Open Notepad and write an article about {topic}"
        }
    elif "take a screenshot" in command_lower:
        return {
            "task_type": "desktop_control",
            "action": "take_screenshot",
            "parameters": {},
            "confirmation_required": False,
            "description": "Take a screenshot"
        }
    elif command_lower.startswith("type:"):
        text_to_type = command.split(":", 1)[1].strip()
        return {
            "task_type": "desktop_control",
            "action": "type_text",
            "parameters": {"text": text_to_type},
            "confirmation_required": False,
            "description": f"Type text: {text_to_type[:50]}..."
        }
    elif command_lower.startswith("click at"):
        try:
            coords = command_lower.split("click at")[1].strip().split(",")
            x = int(coords[0])
            y = int(coords[1])
            return {
                "task_type": "desktop_control",
                "action": "click_at",
                "parameters": {"x": x, "y": y},
                "confirmation_required": False,
                "description": f"Click at coordinates ({x}, {y})"
            }
        except (ValueError, IndexError):
            return {
                "task_type": "unknown",
                "action": "unknown_command",
                "parameters": {},
                "confirmation_required": False,
                "description": "Unknown command"
            }
    elif "add to document" in command_lower or "append to document" in command_lower:
        # Extract text to append
        if "add to document" in command_lower:
            content = command_lower.split("add to document")[1].strip()
        else:
            content = command_lower.split("append to document")[1].strip()
        
        return {
            "task_type": "desktop_control",
            "action": "append_text",
            "parameters": {"text": f"\n\n{content}"},
            "confirmation_required": False,
            "description": f"Add text to current document: {content[:50]}..."
        }
    else:
        return {
            "task_type": "unknown",
            "action": "unknown_command",
            "parameters": {},
            "confirmation_required": False,
            "description": "Unknown command"
        }
