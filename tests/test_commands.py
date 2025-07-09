#!/usr/bin/env python3
"""
Test different Shadow AI commands to ensure proper behavior
"""

import subprocess
import time

def test_command(cmd, description):
    """Test a Shadow AI command"""
    print(f"\n🧪 Testing: {description}")
    print(f"Command: {cmd}")
    print("─" * 50)
    
    try:
        result = subprocess.run(
            f'python main.py "{cmd}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Command executed successfully")
            if result.stdout:
                print(f"Output: {result.stdout[:200]}...")
        else:
            print(f"❌ Command failed with return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
                
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out (30 seconds)")
    except Exception as e:
        print(f"❌ Error running command: {e}")

def main():
    """Run all tests"""
    print("🧠 Shadow AI Command Testing")
    print("=" * 60)
    
    # Test commands
    commands = [
        ("open notepad", "Open Notepad application"),
        ("type: Hello from Shadow AI!", "Type simple text"),
        ("take a screenshot", "Take a screenshot"),
        ("write an article about machine learning", "Open Notepad and write article"),
    ]
    
    for cmd, desc in commands:
        test_command(cmd, desc)
        time.sleep(2)  # Wait between tests
    
    print("\n🎉 Testing completed!")
    print("\nTo test manually:")
    print("1. python main.py \"open notepad\"")
    print("2. python main.py \"write an article about AI\"")
    print("3. Watch Notepad open and article appear!")

if __name__ == "__main__":
    main()
