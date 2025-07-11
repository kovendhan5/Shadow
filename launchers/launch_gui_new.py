#!/usr/bin/env python3
"""
Shadow AI GUI Launcher
Enhanced GUI launcher for all Shadow AI interfaces
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gui_import(gui_name):
    """Test if a GUI can be imported"""
    try:
        print(f"Testing {gui_name} GUI import...")
        
        if gui_name == "working":
            from gui.gui_working import ShadowWorkingGUI
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "premium":
            from gui.gui_premium import ShadowPremiumGUI
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "cyberpunk":
            from gui.gui_cyberpunk import ShadowCyberpunkGUI
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "modern":
            try:
                from gui.gui_modern import ShadowModernGUI
                print(f"✅ {gui_name} GUI imported successfully")
                return True
            except ImportError as e:
                print(f"⚠️ {gui_name} GUI import failed (CustomTkinter may not be available): {e}")
                return False
    except Exception as e:
        print(f"❌ {gui_name} GUI import failed: {e}")
        return False

def launch_gui(gui_name):
    """Launch a specific GUI"""
    print(f"🚀 Launching {gui_name} GUI...")
    
    try:
        if gui_name == "working":
            from gui.gui_working import main as working_main
            working_main()
        elif gui_name == "premium":
            from gui.gui_premium import main as premium_main
            premium_main()
        elif gui_name == "cyberpunk":
            from gui.gui_cyberpunk import main as cyberpunk_main
            cyberpunk_main()
        elif gui_name == "modern":
            from gui.gui_modern import main as modern_main
            modern_main()
        else:
            print(f"❌ Unknown GUI: {gui_name}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Failed to launch {gui_name} GUI: {e}")
        return False

def main():
    """Main launcher interface"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                Shadow AI - GUI Launcher v2.0                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Test imports first
    print("🔍 Testing GUI availability...")
    guis = {
        "working": "Simple, reliable interface",
        "premium": "Elegant glassmorphism design", 
        "cyberpunk": "Futuristic neon-themed interface",
        "modern": "Clean CustomTkinter interface"
    }
    
    working_guis = {}
    
    for gui_name, description in guis.items():
        if test_gui_import(gui_name):
            working_guis[gui_name] = description
    
    print(f"\n✅ Available GUIs: {len(working_guis)}/{len(guis)}")
    
    if not working_guis:
        print("❌ No working GUIs found!")
        print("Please check your installation and dependencies.")
        return
    
    print("\n🎨 Available Shadow AI Interfaces:")
    print("-" * 50)
    
    gui_options = list(working_guis.keys())
    for i, (gui_name, description) in enumerate(working_guis.items(), 1):
        print(f"{i}. {gui_name.title()} GUI - {description}")
    
    print("0. Exit")
    print("-" * 50)
    
    while True:
        try:
            choice = input(f"\nSelect interface to launch (0-{len(gui_options)}): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(gui_options):
                    selected_gui = gui_options[choice_num - 1]
                    print(f"\n🎯 Selected: {selected_gui.title()} GUI")
                    
                    if launch_gui(selected_gui):
                        print(f"✅ {selected_gui.title()} GUI launched successfully!")
                        break
                    else:
                        print(f"❌ Failed to launch {selected_gui} GUI")
                        print("Please try another interface.")
                        continue
                else:
                    print("❌ Invalid choice. Please select a valid option.")
            except ValueError:
                print("❌ Please enter a valid number.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
