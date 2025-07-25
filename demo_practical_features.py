#!/usr/bin/env python3
"""
Shadow AI - Feature Demo Script
Demonstrates all the working practical features
"""

import sys
import os
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Demo all Shadow AI practical features"""
    print("🚀 Shadow AI - Feature Demonstration")
    print("=" * 50)
    print()
    
    try:
        from main import ShadowAI
        shadow_ai = ShadowAI()
        shadow_ai.init_enhanced_features()
        print("✅ Shadow AI initialized successfully!")
    except Exception as e:
        print(f"⚠️ Shadow AI initialization failed: {e}")
        print("📝 Will demonstrate basic features without full AI integration")
        shadow_ai = None
    
    print()
    print("🎯 Available Practical Features:")
    print()
    
    features = [
        ("1", "📝 Open Notepad", demo_open_notepad),
        ("2", "📄 Write Article in Notepad", demo_write_article),
        ("3", "🚀 Launch Applications", demo_launch_apps),
        ("4", "⌨️ Type Text Automation", demo_type_text),
        ("5", "📁 File Operations", demo_file_operations),
        ("6", "🌐 Web Search", demo_web_search),
        ("7", "💻 System Information", demo_system_info),
        ("8", "🔔 Test All Features", demo_all_features),
        ("0", "❌ Exit", None)
    ]
    
    for num, desc, _ in features:
        print(f"  {num}. {desc}")
    
    print()
    
    while True:
        try:
            choice = input("Select feature to demo (0-8): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            # Find and execute the selected demo
            for num, desc, func in features:
                if choice == num and func:
                    print(f"\n🎬 Demonstrating: {desc}")
                    print("-" * 40)
                    func(shadow_ai)
                    print("-" * 40)
                    print("✅ Demo completed!")
                    print()
                    break
            else:
                print("❌ Invalid selection. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_open_notepad(shadow_ai):
    """Demo opening Notepad"""
    print("📝 Opening Notepad...")
    
    if shadow_ai:
        try:
            result = shadow_ai.execute_desktop_action('open_notepad', {})
            if result:
                print("✅ Notepad opened using Shadow AI!")
            else:
                fallback_open_notepad()
        except Exception as e:
            print(f"⚠️ Shadow AI method failed: {e}")
            fallback_open_notepad()
    else:
        fallback_open_notepad()

def fallback_open_notepad():
    """Fallback method to open Notepad"""
    try:
        import subprocess
        subprocess.Popen(['notepad.exe'])
        print("✅ Notepad opened using fallback method!")
    except Exception as e:
        print(f"❌ Failed to open Notepad: {e}")

def demo_write_article(shadow_ai):
    """Demo writing an article to Notepad"""
    topic = input("📝 Enter article topic (or press Enter for 'AI'): ").strip()
    if not topic:
        topic = "Artificial Intelligence"
    
    print(f"📄 Writing article about '{topic}' to Notepad...")
    
    if shadow_ai:
        try:
            result = shadow_ai.execute_desktop_action('open_notepad_and_write_article', {'topic': topic})
            if result:
                print("✅ Article written to Notepad using Shadow AI!")
                return
        except Exception as e:
            print(f"⚠️ Shadow AI method failed: {e}")
    
    # Fallback method
    print("📝 Using fallback method...")
    try:
        import subprocess
        import pyautogui
        
        # Open Notepad
        subprocess.Popen(['notepad.exe'])
        time.sleep(2)
        
        # Generate simple article
        article = f"""# Article: {topic.title()}

## Introduction
This article discusses {topic.lower()} and its importance in today's world.

## Key Points
1. {topic.title()} is a rapidly evolving field
2. It has applications across many industries  
3. Understanding {topic.lower()} is becoming essential

## Conclusion
{topic.title()} will continue to shape our future.

---
Generated by Shadow AI Demo
"""
        
        # Type the article
        pyautogui.typewrite(article, interval=0.01)
        print("✅ Article written using fallback method!")
        
    except Exception as e:
        print(f"❌ Failed to write article: {e}")

def demo_launch_apps(shadow_ai):
    """Demo launching applications"""
    apps = [
        ("Calculator", "calc.exe"),
        ("Paint", "mspaint.exe"),
        ("File Explorer", "explorer.exe"),
        ("Notepad", "notepad.exe")
    ]
    
    print("🚀 Available applications to launch:")
    for i, (name, _) in enumerate(apps, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select app (1-4): ")) - 1
        if 0 <= choice < len(apps):
            name, command = apps[choice]
            print(f"🚀 Launching {name}...")
            
            try:
                import subprocess
                subprocess.Popen([command])
                print(f"✅ {name} launched successfully!")
            except Exception as e:
                print(f"❌ Failed to launch {name}: {e}")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Please enter a valid number")

def demo_type_text(shadow_ai):
    """Demo typing text automation"""
    text = input("⌨️ Enter text to type (will type after 3 seconds): ").strip()
    if not text:
        text = "Hello from Shadow AI! This text was typed automatically."
    
    print("⏰ You have 3 seconds to click in any text field...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("⌨️ Typing text now...")
    
    try:
        import pyautogui
        pyautogui.typewrite(text, interval=0.05)
        print("✅ Text typed successfully!")
    except Exception as e:
        print(f"❌ Failed to type text: {e}")

def demo_file_operations(shadow_ai):
    """Demo file operations"""
    print("📁 File Operations Demo:")
    print("  1. Show current directory contents")
    print("  2. Create a test file")
    print("  3. Show file organization features")
    
    try:
        choice = input("Select operation (1-3): ").strip()
        
        if choice == "1":
            print("📂 Current directory contents:")
            try:
                import os
                files = os.listdir('.')
                for i, file in enumerate(files[:10], 1):  # Show first 10 files
                    print(f"  {i:2d}. {file}")
                if len(files) > 10:
                    print(f"     ... and {len(files) - 10} more files")
                print("✅ Directory listing completed!")
            except Exception as e:
                print(f"❌ Error listing directory: {e}")
        
        elif choice == "2":
            print("📄 Creating test file...")
            try:
                with open("shadow_ai_test.txt", "w") as f:
                    f.write("This is a test file created by Shadow AI!\n")
                    f.write(f"Created on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                print("✅ Test file 'shadow_ai_test.txt' created!")
            except Exception as e:
                print(f"❌ Error creating file: {e}")
        
        elif choice == "3":
            print("🗂️ File organization features available:")
            print("  • Organize files by type (images, documents, etc.)")
            print("  • Clean up duplicate files")
            print("  • Create backup folders")
            print("  • Find large files")
            if shadow_ai:
                print("  ✅ All features available through Shadow AI!")
            else:
                print("  ⚠️ Full features require Shadow AI initialization")
        
    except Exception as e:
        print(f"❌ Error in file operations: {e}")

def demo_web_search(shadow_ai):
    """Demo web search functionality"""
    query = input("🌐 Enter search query: ").strip()
    if not query:
        query = "Shadow AI automation"
    
    print(f"🔍 Searching for: '{query}'")
    
    if shadow_ai:
        try:
            result = shadow_ai.handle_web_search(f"search Google for {query}")
            if result:
                print("✅ Web search executed using Shadow AI!")
                return
        except Exception as e:
            print(f"⚠️ Shadow AI search failed: {e}")
    
    # Fallback - open browser with search
    print("🌐 Opening browser search...")
    try:
        import webbrowser
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        print("✅ Browser opened with search results!")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")

def demo_system_info(shadow_ai):
    """Demo system information"""
    print("💻 Gathering system information...")
    
    if shadow_ai:
        try:
            result = shadow_ai.handle_system_info("show system information")
            if result:
                print("✅ System info displayed using Shadow AI!")
                return
        except Exception as e:
            print(f"⚠️ Shadow AI system info failed: {e}")
    
    # Fallback system info
    print("📊 Basic system information:")
    try:
        import platform
        import psutil
        
        print(f"  🖥️ System: {platform.system()} {platform.release()}")
        print(f"  🐍 Python: {platform.python_version()}")
        print(f"  💻 CPU: {psutil.cpu_count()} cores")
        print(f"  🧠 Memory: {psutil.virtual_memory().total // (1024**3)} GB")
        print(f"  📈 CPU Usage: {psutil.cpu_percent(interval=1):.1f}%")
        print(f"  🧠 Memory Usage: {psutil.virtual_memory().percent:.1f}%")
        print("✅ System information displayed!")
        
    except ImportError:
        print("⚠️ psutil not available for detailed system info")
        print(f"  🖥️ System: {platform.system()} {platform.release()}")
        print(f"  🐍 Python: {platform.python_version()}")
    except Exception as e:
        print(f"❌ Error getting system info: {e}")

def demo_all_features(shadow_ai):
    """Demo all features quickly"""
    print("🔥 Testing all features quickly...")
    print()
    
    features = [
        ("📝 Notepad", lambda: demo_open_notepad(shadow_ai)),
        ("💻 System Info", lambda: demo_system_info(shadow_ai)),
        ("📁 File Ops", lambda: demo_file_operations(shadow_ai))
    ]
    
    for name, func in features:
        print(f"🎬 Testing {name}...")
        try:
            func()
            time.sleep(1)
        except Exception as e:
            print(f"❌ {name} failed: {e}")
        print()
    
    print("🎉 All features tested!")

if __name__ == "__main__":
    main()
