import os
import sys

# Change to the Shadow directory  
os.chdir(r'k:\Devops\Shadow')

print("🌌 Testing Shadow AI Cyberpunk GUI...")
print("Dark theme with neon effects and matrix rain!")
print()

try:
    # Import and run the cyberpunk GUI
    import gui_cyberpunk
    gui_cyberpunk.main()
except Exception as e:
    print(f"Error launching GUI: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
