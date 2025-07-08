import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from brain.gpt_agent import GPTAgent, process_command
    print("✓ Successfully imported GPTAgent and process_command")
    
    # Test agent initialization
    agent = GPTAgent()
    print(f"✓ Agent initialized")
    print(f"  Provider: {agent.provider}")
    print(f"  Model: {agent.model}")
    print(f"  Client available: {agent.client_available}")
    
    # Test a simple command
    result = process_command("open notepad")
    print(f"✓ Command processed successfully")
    print(f"  Task type: {result.get('task_type')}")
    print(f"  Action: {result.get('action')}")
    print(f"  Description: {result.get('description')}")
    
    print("\n🎉 GPT Agent is working correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
