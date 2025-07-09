#!/usr/bin/env python3
"""
Simple GUI launcher and tester for Shadow AI
"""
import sys
import os
import subprocess

def test_gui_import(gui_name):
    """Test if a GUI can be imported"""
    try:
        print(f"Testing {gui_name} import...")
        if gui_name == "premium":
            import gui_premium
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "ultra":
            import gui_ultra
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "cyberpunk":
            import gui_cyberpunk
            print(f"✅ {gui_name} GUI imported successfully")
            return True
        elif gui_name == "working":
            import gui_working
            print(f"✅ {gui_name} GUI imported successfully")
            return True
    except Exception as e:
        print(f"❌ {gui_name} GUI import failed: {e}")
        return False

def launch_gui(gui_name):
    """Launch a specific GUI"""
    gui_files = {
        "premium": "gui_premium.py",
        "ultra": "gui_ultra.py", 
        "cyberpunk": "gui_cyberpunk.py",
        "working": "gui_working.py",
        "modern": "gui_modern.py"
    }
    
    if gui_name not in gui_files:
        print(f"❌ Unknown GUI: {gui_name}")
        print(f"Available GUIs: {', '.join(gui_files.keys())}")
        return False
    
    gui_file = gui_files[gui_name]
    
    if not os.path.exists(gui_file):
        print(f"❌ GUI file not found: {gui_file}")
        return False
    
    print(f"🚀 Launching {gui_name} GUI...")
    try:
        # Launch GUI in a new process
        process = subprocess.Popen([sys.executable, gui_file])
        print(f"✅ {gui_name} GUI launched successfully (PID: {process.pid})")
        return True
    except Exception as e:
        print(f"❌ Failed to launch {gui_name} GUI: {e}")
        return False

def main():
    """Main launcher interface"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    Shadow AI - GUI Launcher                 ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Test imports first
    print("Testing GUI imports...")
    guis = ["premium", "ultra", "cyberpunk", "working"]
    working_guis = []
    
    for gui in guis:
        if test_gui_import(gui):
            working_guis.append(gui)
    
    print(f"\n✅ Working GUIs: {len(working_guis)}/{len(guis)}")
    
    if not working_guis:
        print("❌ No working GUIs found!")
        return
    
    print("\nAvailable GUI options:")
    print("1. Premium GUI     - Professional glassmorphism design")
    print("2. Ultra GUI       - Advanced animations and effects")
    print("3. Cyberpunk GUI   - Dark theme with neon effects")
    print("4. Working GUI     - Minimal, stable interface")
    print("5. Modern GUI      - Standard modern interface")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nSelect GUI to launch (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                launch_gui("premium")
            elif choice == "2":
                launch_gui("ultra")
            elif choice == "3":
                launch_gui("cyberpunk")
            elif choice == "4":
                launch_gui("working")
            elif choice == "5":
                launch_gui("modern")
            else:
                print("❌ Invalid choice. Please select 0-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
        print("❌ Dependency check failed. Please install required modules.")
        return
    
    # Check .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("⚠️  Warning: .env file not found. Please create it with your API keys.")
        print("   You can copy .env.template to .env and fill in your keys.")
    
    try:
        # Import and run the modern GUI
        from gui_modern import ModernShadowGUI
        
        print("✅ Dependencies loaded successfully")
        print("🚀 Starting Shadow AI Modern GUI...")
        print("📱 The GUI window should open shortly...")
        
        # Create and run the GUI
        app = ModernShadowGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all Shadow AI modules are available.")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        logging.error(f"GUI startup error: {e}")

if __name__ == "__main__":
    main()
