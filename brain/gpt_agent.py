import logging

def process_command(command):
    logging.info(f"Processing command: {command}")
    # In the future, this will interact with an LLM
    if "open notepad" in command.lower():
        return {"action": "open_notepad"}
    elif command.lower().startswith("type:"):
        text_to_type = command.split(":", 1)[1].strip()
        return {"action": "type_text", "text": text_to_type}
    elif command.lower().startswith("click at"):
        try:
            coords = command.lower().split("click at")[1].strip().split(",")
            x = int(coords[0])
            y = int(coords[1])
            return {"action": "click_at", "x": x, "y": y}
        except (ValueError, IndexError):
            return {"action": "unknown_command"}
    else:
        return {"action": "unknown_command"}
