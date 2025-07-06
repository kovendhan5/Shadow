# main.py

import logging
from utils.logging import setup_logging
from input.text_input import get_text_input
from brain.gpt_agent import process_command
from control.desktop import open_notepad

def main():
    setup_logging()
    logging.info("Shadow is running...")
    
    while True:
        command = get_text_input()
        if command.lower() == "exit":
            logging.info("Exiting Shadow.")
            break
        
        action = process_command(command)
        
        if action == "open_notepad":
            open_notepad()
        else:
            logging.warning(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
