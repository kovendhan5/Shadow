import logging

def process_command(command):
    logging.info(f"Processing command: {command}")
    # In the future, this will interact with an LLM
    if "open notepad" in command.lower():
        return "open_notepad"
    else:
        return "unknown_command"
