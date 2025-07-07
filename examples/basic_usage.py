# examples/basic_usage.py
"""
Basic usage examples for Shadow AI Agent
This script demonstrates basic commands and functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ShadowAI
import time

def basic_desktop_automation():
    """Demonstrate basic desktop automation"""
    print("🖥️  Basic Desktop Automation Examples")
    print("=" * 50)
    
    shadow = ShadowAI()
    
    # Example 1: Open Notepad
    print("\n1. Opening Notepad...")
    shadow.run_single_command("open notepad")
    time.sleep(2)
    
    # Example 2: Type text
    print("\n2. Typing text...")
    shadow.run_single_command("type: Hello from Shadow AI!")
    time.sleep(1)
    
    # Example 3: Take screenshot
    print("\n3. Taking screenshot...")
    shadow.run_single_command("take a screenshot")
    time.sleep(1)
    
    print("\n✅ Basic desktop automation examples completed!")

def document_creation_examples():
    """Demonstrate document creation"""
    print("\n📄 Document Creation Examples")
    print("=" * 50)
    
    shadow = ShadowAI()
    
    # Example 1: Create a leave letter
    print("\n1. Creating a leave letter...")
    shadow.run_single_command("write a leave letter for tomorrow due to health reasons")
    time.sleep(2)
    
    # Example 2: Create a resume template
    print("\n2. Creating a resume template...")
    shadow.run_single_command("create a resume template")
    time.sleep(2)
    
    print("\n✅ Document creation examples completed!")

def web_automation_examples():
    """Demonstrate web automation"""
    print("\n🌐 Web Automation Examples")
    print("=" * 50)
    
    shadow = ShadowAI()
    
    # Example 1: Search on Google
    print("\n1. Searching on Google...")
    shadow.run_single_command("search for artificial intelligence on google")
    time.sleep(3)
    
    # Example 2: Search on Flipkart
    print("\n2. Searching on Flipkart...")
    shadow.run_single_command("search for smartphone on flipkart")
    time.sleep(3)
    
    print("\n✅ Web automation examples completed!")

def application_control_examples():
    """Demonstrate application control"""
    print("\n📱 Application Control Examples")
    print("=" * 50)
    
    shadow = ShadowAI()
    
    # Example 1: Open Calculator
    print("\n1. Opening Calculator...")
    shadow.run_single_command("open calculator")
    time.sleep(2)
    
    # Example 2: Open File Explorer
    print("\n2. Opening File Explorer...")
    shadow.run_single_command("open explorer")
    time.sleep(2)
    
    # Example 3: Open Paint
    print("\n3. Opening Paint...")
    shadow.run_single_command("open paint")
    time.sleep(2)
    
    print("\n✅ Application control examples completed!")

def main():
    """Main function to run all examples"""
    print("🧠 Shadow AI Agent - Usage Examples")
    print("=" * 60)
    print("\nThis script demonstrates various Shadow AI capabilities.")
    print("Each example will run automatically with delays between actions.")
    print("\nPress Ctrl+C to stop at any time.")
    
    try:
        # Run examples
        basic_desktop_automation()
        document_creation_examples()
        web_automation_examples()
        application_control_examples()
        
        print("\n🎉 All examples completed successfully!")
        print("\nYou can now use Shadow AI with natural language commands like:")
        print("• 'Open notepad and type my shopping list'")
        print("• 'Write a professional email to my boss'")
        print("• 'Search for the best laptops under $1000'")
        print("• 'Create a presentation about AI trends'")
        
    except KeyboardInterrupt:
        print("\n\n👋 Examples stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Please check your Shadow AI installation and try again.")

if __name__ == "__main__":
    main()
