import os
import sys

# Change to the Shadow directory
os.chdir(r'k:\Devops\Shadow')

print("🚀 Testing Shadow AI Premium GUI...")
print("If the GUI opens successfully, you can test all features!")
print()

try:
    # Import and run the premium GUI
    import gui_premium
    gui_premium.main()
except Exception as e:
    print(f"Error launching GUI: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
