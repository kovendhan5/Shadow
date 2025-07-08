#!/usr/bin/env python3
"""
Shadow AI Quick Demo - Shows proper behavior
"""

import time
import os

def main():
    """Main demo function"""
    print("🧠 Shadow AI - Proper Command Behavior")
    print("=" * 50)
    
    print("\n🎯 FIXED ISSUE: Now opens Notepad BEFORE typing!")
    print("\nBefore: Typed wherever cursor was")
    print("After:  Opens Notepad → Waits → Types content")
    
    print("\n📋 Test Commands:")
    print('1. python main.py "open notepad"')
    print('   → Opens Notepad application')
    
    print('\n2. python main.py "write an article about AI"')
    print('   → Opens Notepad → Waits 2 seconds → Types article')
    
    print('\n3. python main.py "type: Hello Shadow AI!"')
    print('   → Types in currently active window')
    
    print("\n✅ Key Improvement:")
    print("- Commands with 'write article' now ALWAYS open Notepad first")
    print("- No more random typing in other windows")
    print("- Proper waiting time for Notepad to load")
    
    print("\n🚀 Try it now:")
    print('python main.py "write an article about machine learning"')

if __name__ == "__main__":
    main()
