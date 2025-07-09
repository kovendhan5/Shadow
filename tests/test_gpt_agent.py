#!/usr/bin/env python3
"""
Test script for GPT Agent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain.gpt_agent import GPTAgent, process_command
import json

def test_gpt_agent():
    """Test the GPT Agent initialization and basic functionality"""
    print("Testing GPT Agent...")
    
    # Test initialization
    try:
        agent = GPTAgent()
        print(f"✓ Agent initialized successfully")
        print(f"  Provider: {agent.provider}")
        print(f"  Model: {agent.model}")
        print(f"  Client available: {agent.client_available}")
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False
    
    # Test command processing
    test_commands = [
        "open notepad",
        "take a screenshot",
        "write an article about artificial intelligence",
        "open notepad and create a new file and name it test.txt then write hello world"
    ]
    
    print("\nTesting command processing...")
    for cmd in test_commands:
        try:
            result = process_command(cmd)
            print(f"✓ Command: '{cmd}'")
            print(f"  Result: {json.dumps(result, indent=2)}")
            print()
        except Exception as e:
            print(f"✗ Command failed: '{cmd}' - {e}")
    
    return True

def test_fallback_parsing():
    """Test the fallback command parsing"""
    print("Testing fallback command parsing...")
    
    # Import the fallback function
    from brain.gpt_agent import _fallback_command_parsing
    
    test_cases = [
        ("open notepad", "desktop_control", "open_notepad"),
        ("take a screenshot", "desktop_control", "take_screenshot"),
        ("write an article about AI", "desktop_control", "open_notepad_and_write_article"),
        ("type: hello world", "desktop_control", "type_text"),
        ("click at 100,200", "desktop_control", "click_at"),
        ("unknown command", "unknown", "unknown_command")
    ]
    
    for cmd, expected_type, expected_action in test_cases:
        try:
            result = _fallback_command_parsing(cmd)
            if result["task_type"] == expected_type and result["action"] == expected_action:
                print(f"✓ '{cmd}' -> {expected_type}/{expected_action}")
            else:
                print(f"✗ '{cmd}' -> Expected {expected_type}/{expected_action}, got {result['task_type']}/{result['action']}")
        except Exception as e:
            print(f"✗ '{cmd}' failed: {e}")

if __name__ == "__main__":
    print("=== GPT Agent Test Suite ===")
    print()
    
    success = test_gpt_agent()
    print()
    test_fallback_parsing()
    
    if success:
        print("\n✓ All tests completed successfully!")
    else:
        print("\n✗ Some tests failed!")
