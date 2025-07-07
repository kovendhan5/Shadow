# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# LLM Configuration
DEFAULT_LLM_PROVIDER = "gemini"  # Options: "openai", "gemini", "ollama"
DEFAULT_MODEL = {
    "openai": "gpt-4",
    "gemini": "gemini-1.5-flash",
    "ollama": "llama3"
}

# Voice settings
VOICE_ENABLED = True
VOICE_LANGUAGE = "en-US"
VOICE_TIMEOUT = 5
VOICE_PHRASE_TIME_LIMIT = 10

# Safety settings
REQUIRE_CONFIRMATION = True
CONFIRMATION_TIMEOUT = 30
LOG_ALL_ACTIONS = True

# Paths
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
DOCUMENTS_PATH = os.path.join(os.path.expanduser("~"), "Documents")
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")
LOGS_PATH = os.path.join(os.path.dirname(__file__), "logs")

# Browser settings
DEFAULT_BROWSER = "chrome"  # Options: "chrome", "firefox", "edge"
BROWSER_TIMEOUT = 30
HEADLESS_MODE = False

# Document settings
DEFAULT_DOC_FORMAT = "docx"  # Options: "docx", "pdf", "txt"
SAVE_LOCATION = DESKTOP_PATH
