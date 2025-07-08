#!/usr/bin/env python3
"""
Test the fixed universal executor functionality
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_executor_fixes():
    """Test that the executor fixes work"""
    try:
        print("🔧 Testing universal executor fixes...")
        
        # Import the modules
        from brain.universal_processor import process_universal_command
        from brain.universal_executor import execute_universal_task
        
        print("✅ Universal modules imported successfully")
        
        # Test command that was previously failing
        test_command = "open notepad and write an article about ai"
        print(f"📝 Testing command: {test_command}")
        
        # Process the command
        task = process_universal_command(test_command)
        
        if task:
            print(f"✅ Task processed successfully:")
            print(f"   - Description: {task.description}")
            print(f"   - Complexity: {task.complexity.value}")
            print(f"   - Steps: {len(task.steps)}")
            
            # Check for type_content action
            has_type_content = any(step.action == "type_content" for step in task.steps)
            if has_type_content:
                print("✅ type_content action found in steps")
            else:
                print("⚠️ type_content action not found in steps")
            
            print("\n🔍 Task steps:")
            for i, step in enumerate(task.steps, 1):
                print(f"   {i}. {step.action} - {step.expected_result}")
            
            # Test execution (without actually executing for safety)
            print("\n🚀 Testing task execution...")
            
            # We'll just test the executor setup, not actual execution
            from brain.universal_executor import universal_executor
            
            # Check if type_content handler exists
            if "type_content" in universal_executor.action_handlers:
                print("✅ type_content handler is registered")
            else:
                print("❌ type_content handler is missing")
            
            print(f"📊 Total action handlers: {len(universal_executor.action_handlers)}")
            print("✅ Available action handlers:")
            for action in sorted(universal_executor.action_handlers.keys()):
                print(f"   - {action}")
                
        else:
            print("❌ Task processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_executor_fixes()
