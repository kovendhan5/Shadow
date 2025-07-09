#!/usr/bin/env python3
"""
Shadow AI Demo Script
Demonstrates key functionality
"""

import subprocess
import time
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_command(cmd):
    """Run a Shadow AI command"""
    print(f"🤖 Running: {cmd}")
    result = subprocess.run([sys.executable, "main.py", cmd], 
                          capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode == 0:
        print("✅ Success!")
    else:
        print(f"❌ Error: {result.stderr}")
    time.sleep(2)
    return result.returncode == 0

def main():
    """Run demo"""
    print("🧠 Shadow AI Demo")
    print("=" * 50)
    
    # Test 1: Open Notepad
    print("\n1. Opening Notepad...")
    run_command("open notepad")
    
    # Test 2: Type some text
    print("\n2. Typing text...")
    run_command("type: Hello! This is Shadow AI.")
    
    # Test 3: Add more content
    print("\n3. Adding more content...")
    run_command("add to document Here's some additional text added by Shadow AI!")
    
    # Test 4: Take screenshot
    print("\n4. Taking screenshot...")
    run_command("take a screenshot")
    
    # Test 5: Write an article
    print("\n5. Writing an article about AI...")
    run_command("write an article about machine learning")
    
    print("\n🎉 Demo completed!")
    print("\nManual Commands you can try:")
    print("- python main.py 'open notepad'")
    print("- python main.py 'type: your text here'")
    print("- python main.py 'write an article about [topic]'")
    print("- python main.py 'take a screenshot'")
    print("- python main.py 'open notepad write an article about AI'")

if __name__ == "__main__":
    main()
