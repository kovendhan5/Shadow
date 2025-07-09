#!/usr/bin/env python3
"""
Test the specific notepad task that's failing
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_notepad_task():
    """Test the specific task: open notepad, create file, name it new.txt, write AI article"""
    print("🔧 Testing Notepad Task...")
    print("=" * 50)
    
    try:
        from main import ShadowAI
        from config import GEMINI_API_KEY
        
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_key_here":
            print("❌ Gemini API key not configured")
            return False
        
        # Initialize Shadow AI
        shadow = ShadowAI()
        
        # Test the specific task
        command = "open a notepad and create a new file and name it new.txt then write an article about ai"
        print(f"📝 Command: {command}")
        print("\n🚀 Executing task...")
        
        result = shadow.process_command(command)
        
        print(f"\n📊 Result:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', 'No message')}")
        
        if 'task_result' in result:
            task_result = result['task_result']
            print(f"   Task Success: {task_result.success}")
            print(f"   Execution Time: {task_result.execution_time:.2f}s")
            if task_result.step_results:
                print("   Step Results:")
                for step in task_result.step_results:
                    status = "✅" if step.get('success', False) else "❌"
                    print(f"     {status} Step {step.get('step_number', '?')}: {step.get('action', 'Unknown')}")
                    if not step.get('success', False) and 'error' in step:
                        print(f"       Error: {step['error']}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Error testing task: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_notepad_task()
