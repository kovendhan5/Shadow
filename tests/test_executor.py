import sys
import traceback

try:
    from brain.universal_executor import execute_universal_task
    print("SUCCESS: universal_executor imported")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
