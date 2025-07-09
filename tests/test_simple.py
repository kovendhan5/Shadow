import sys
import os
sys.path.append('.')

try:
    from brain.universal_processor import UniversalProcessor
    print("✓ Import successful")
    
    processor = UniversalProcessor()
    print(f"✓ Processor created, AI available: {processor.ai_available}")
    
    if processor.ai_available:
        print("✓ Testing Gemini API...")
        response = processor.ai_model.generate_content('Say "Hello"')
        print(f"✓ API Response: {response.text}")
        print("✓ Gemini API is working with gemini-1.5-flash!")
    else:
        print("❌ AI not available")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
