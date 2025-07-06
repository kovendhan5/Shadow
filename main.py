# main.py

import logging
import sys
from utils.logging import setup_logging
from brain.gpt_agent import process_command
from control.desktop import open_notepad, type_text, click_at

def main():
    setup_logging()
    logging.info("Shadow is running...")

    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        logging.info(f"Received command: {command}")
        result = process_command(command)
        action = result.get("action")

        if action == "open_notepad":
            open_notepad()
        elif action == "type_text":
            text_to_type = result.get("text")
            if text_to_type.startswith("file:"):
                filepath = text_to_type.split(":", 1)[1].strip()
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    type_text(content)
                except FileNotFoundError:
                    logging.error(f"File not found: {filepath}")
            else:
                type_text(text_to_type)
        elif action == "click_at":
            click_at(result.get("x"), result.get("y"))
        else:
            logging.warning(f"Unknown command: {command}")
    else:
        logging.info("No command provided.")

if __name__ == "__main__":
    main()

