#!/usr/bin/env python3
"""
Shadow AI - Complete Demo Showcase
Demonstrates all the enhanced features and capabilities
"""

import sys
import os
import time
import subprocess

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Print the demo banner"""
    print("=" * 80)
    print("🚀 SHADOW AI - COMPLETE FEATURE DEMONSTRATION")
    print("=" * 80)
    print("🎉 Welcome to the most advanced AI assistant with stunning visuals!")
    print("✨ This demo showcases all the enhanced features and capabilities")
    print("=" * 80)
    print()

def demo_menu():
    """Show the demo menu"""
    print("🎯 DEMO MENU - Choose what to experience:")
    print()
    print("1. 🎨 Enhanced Ultra GUI Demo (RECOMMENDED)")
    print("   ⚡ Particle effects, holographic buttons, neural networks")
    print("   🌊 Matrix rain background, dynamic themes")
    print()
    print("2. 🎭 Orpheus Emotional AI Demo")
    print("   💝 Emotional intelligence, empathetic conversations")
    print("   📊 Real-time emotion visualization")
    print()
    print("3. 📝 Notepad Task Demonstration")
    print("   🔧 The specific task that was fixed and enhanced")
    print("   📄 Complete file creation with AI article")
    print()
    print("4. 🎪 All GUI Collection Showcase")
    print("   🎨 See all 6 different interface themes")
    print("   ⭐ Modern, Premium, Ultra, Cyberpunk, Orpheus, Enhanced")
    print()
    print("5. 🧠 Core AI Engine Test")
    print("   🔍 Test command processing and execution")
    print("   ⚙️ Verify all components are working")
    print()
    print("6. 🚀 Complete System Showcase (All Features)")
    print("   🎆 Experience everything Shadow AI can do")
    print()
    print("0. ❌ Exit Demo")
    print()

def demo_enhanced_gui():
    """Demo the enhanced GUI"""
    print("🎨 Launching Enhanced Ultra GUI...")
    print("=" * 50)
    print("🌟 FEATURES YOU'LL SEE:")
    print("  ⚡ Real-time particle effects")
    print("  🎭 Holographic buttons with glow animations")
    print("  🧠 Live neural network visualization")
    print("  🌊 Matrix rain background animation")
    print("  🎪 Dynamic theme switching")
    print("  🚀 Advanced task progress visualization")
    print("  💫 Particle burst effects for feedback")
    print()
    print("📝 TRY THESE COMMANDS:")
    print("  • Type: 'open a notepad and create a new file and name it new.txt then write an article about ai'")
    print("  • Click the 'Test Notepad' quick action button")
    print("  • Try the theme switcher buttons")
    print("  • Watch the particle effects and neural network")
    print()
    
    try:
        print("🚀 Starting Enhanced GUI...")
        subprocess.run([sys.executable, "gui_enhanced.py"])
        print("✅ Enhanced GUI demo completed!")
    except Exception as e:
        print(f"❌ Error launching Enhanced GUI: {e}")
        print("💡 Try running: python gui_enhanced.py")

def demo_orpheus():
    """Demo Orpheus emotional AI"""
    print("🎭 Launching Orpheus Emotional AI...")
    print("=" * 50)
    print("💝 EMOTIONAL AI FEATURES:")
    print("  🎯 12+ emotion types with real-time recognition")
    print("  💭 Empathetic and contextual responses")
    print("  🎨 Beautiful visual emotion indicators")
    print("  📊 Real-time emotional state visualization")
    print("  🔄 Dual mode: Emotional + Functional AI")
    print("  📋 Conversation export and analytics")
    print()
    print("🗣️ TRY THESE EMOTIONAL MESSAGES:")
    print("  • 'I'm feeling really excited about my new project!'")
    print("  • 'I'm worried about my presentation tomorrow'")
    print("  • 'Thank you for being so understanding'")
    print("  • 'I had the most amazing day today!'")
    print()
    
    try:
        print("🎭 Starting Orpheus Emotional AI...")
        subprocess.run([sys.executable, "gui_orpheus.py"])
        print("✅ Orpheus demo completed!")
    except Exception as e:
        print(f"❌ Error launching Orpheus: {e}")
        print("💡 Try running: python gui_orpheus.py")

def demo_notepad_task():
    """Demo the specific notepad task"""
    print("📝 Demonstrating Enhanced Notepad Task...")
    print("=" * 50)
    print("🎯 THE TASK: 'open a notepad and create a new file and name it new.txt then write an article about ai'")
    print()
    print("🔧 WHAT HAPPENS:")
    print("  1. 🚀 Launches Notepad.exe")
    print("  2. 📝 Generates comprehensive AI article (500+ words)")
    print("  3. ⌨️ Types the article content automatically")
    print("  4. 💾 Uses Ctrl+S to open save dialog")
    print("  5. 📄 Types filename 'new.txt'")
    print("  6. ✅ Presses Enter to save the file")
    print("  7. 🎉 Returns success confirmation")
    print()
    
    choice = input("🚀 Ready to run the notepad task? (y/n): ").lower()
    if choice == 'y':
        try:
            print("🔄 Testing notepad task...")
            subprocess.run([sys.executable, "test_notepad_task.py"])
            print("✅ Notepad task demo completed!")
            print("📁 Check your Desktop for the 'new.txt' file!")
        except Exception as e:
            print(f"❌ Error running notepad task: {e}")
    else:
        print("⏭️ Skipping notepad task demo")

def demo_all_guis():
    """Demo all GUI interfaces"""
    print("🎪 GUI Collection Showcase...")
    print("=" * 50)
    
    guis = [
        ("🎨 Enhanced Ultra GUI", "gui_enhanced.py", "Most advanced with particles & animations"),
        ("🎭 Orpheus Emotional AI", "gui_orpheus.py", "Emotional intelligence interface"),
        ("🚀 Modern GUI", "gui_modern.py", "Sleek modern animated interface"),
        ("💎 Premium GUI", "gui_premium.py", "Business glassmorphism design"),
        ("⚡ Ultra GUI", "gui_ultra.py", "Ultra-modern with advanced effects"),
        ("🌆 Cyberpunk GUI", "gui_cyberpunk.py", "Dark neon cyberpunk theme")
    ]
    
    print("Available GUI Interfaces:")
    for i, (name, file, desc) in enumerate(guis, 1):
        print(f"  {i}. {name}")
        print(f"     {desc}")
        print()
    
    choice = input("🎯 Which GUI would you like to see? (1-6, or 'all' for batch launcher): ")
    
    if choice.lower() == 'all':
        try:
            subprocess.run(["launch_all_guis.bat"], shell=True)
        except Exception as e:
            print(f"❌ Error launching all GUIs: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= 6:
        try:
            gui_file = guis[int(choice)-1][1]
            print(f"🚀 Launching {guis[int(choice)-1][0]}...")
            subprocess.run([sys.executable, gui_file])
        except Exception as e:
            print(f"❌ Error launching GUI: {e}")
    else:
        print("Invalid choice")

def demo_ai_engine():
    """Demo the core AI engine"""
    print("🧠 Core AI Engine Testing...")
    print("=" * 50)
    print("🔍 Testing all components...")
    print()
    
    tests = [
        ("🧠 Universal Processor", "from brain.universal_processor import UniversalProcessor; print('✅ Processor working')"),
        ("⚡ Universal Executor", "from brain.universal_executor import universal_executor; print('✅ Executor working')"),
        ("🎭 Orpheus AI", "from brain.orpheus_ai import EmotionalAI; print('✅ Orpheus working')"),
        ("🖥️ Desktop Control", "from control.desktop import desktop_controller; print('✅ Desktop control working')"),
        ("🌐 Browser Control", "from control.intelligent_browser import IntelligentBrowser; print('✅ Browser control working')"),
        ("📄 Document Control", "from control.documents import document_controller; print('✅ Document control working')")
    ]
    
    for name, test_code in tests:
        try:
            print(f"Testing {name}...")
            subprocess.run([sys.executable, "-c", test_code], check=True)
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
    
    print()
    print("🎯 Running comprehensive system test...")
    try:
        subprocess.run([sys.executable, "test_orpheus.py"])
        print("✅ All AI engine tests completed!")
    except Exception as e:
        print(f"❌ System test error: {e}")

def demo_complete_showcase():
    """Complete system showcase"""
    print("🚀 Complete Shadow AI Showcase...")
    print("=" * 50)
    print("🎆 This will demonstrate ALL features in sequence:")
    print("  1. 🧠 AI Engine verification")
    print("  2. 🎭 Orpheus emotional conversation")
    print("  3. 📝 Enhanced notepad task")
    print("  4. 🎨 Enhanced GUI with all effects")
    print()
    
    choice = input("🚀 Ready for the complete showcase? (y/n): ").lower()
    if choice != 'y':
        print("⏭️ Skipping complete showcase")
        return
    
    print("\n🔄 Starting complete showcase...")
    time.sleep(2)
    
    # 1. AI Engine test
    print("\n📊 Step 1: AI Engine Verification")
    demo_ai_engine()
    time.sleep(2)
    
    # 2. Quick Orpheus test
    print("\n🎭 Step 2: Orpheus Quick Test")
    try:
        subprocess.run([sys.executable, "-c", """
from brain.orpheus_ai import EmotionalAI
ai = EmotionalAI()
print('🎭 Orpheus:', ai.generate_greeting())
response = ai.generate_emotional_response('I am excited to see Shadow AI!')
print('🎭 Orpheus:', response[:100] + '...')
print('📊 Emotional state:', ai.get_emotional_state_description())
"""])
    except Exception as e:
        print(f"❌ Orpheus test error: {e}")
    
    time.sleep(2)
    
    # 3. Notepad task
    print("\n📝 Step 3: Enhanced Notepad Task")
    demo_notepad_task()
    time.sleep(2)
    
    # 4. Enhanced GUI
    print("\n🎨 Step 4: Enhanced GUI (Final Experience)")
    demo_enhanced_gui()
    
    print("\n🎉 Complete showcase finished!")
    print("✨ Shadow AI is ready for advanced AI assistance!")

def main():
    """Main demo function"""
    print_banner()
    
    while True:
        demo_menu()
        
        try:
            choice = input("🎯 Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for exploring Shadow AI!")
                print("🚀 All systems are ready for your AI assistance needs!")
                break
            elif choice == "1":
                demo_enhanced_gui()
            elif choice == "2":
                demo_orpheus()
            elif choice == "3":
                demo_notepad_task()
            elif choice == "4":
                demo_all_guis()
            elif choice == "5":
                demo_ai_engine()
            elif choice == "6":
                demo_complete_showcase()
            else:
                print("❌ Invalid choice. Please enter 0-6.")
            
            print("\n" + "="*50)
            input("Press Enter to continue...")
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
