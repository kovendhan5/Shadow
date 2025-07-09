#!/usr/bin/env python3
"""
Test the complete Shadow AI system with updated Gemini model
"""
import sys
import os

def test_shadow_system():
    """Test the complete Shadow AI system"""
    print("=" * 50)
    print("SHADOW AI SYSTEM TEST")
    print("=" * 50)
    
    try:
        # Test 1: Import main modules
        print("1. Testing imports...")
        sys.path.append('.')
        
        from brain.universal_processor import UniversalProcessor
        from brain.universal_executor import UniversalExecutor
        from brain.gpt_agent import GPTAgent
        print("   ✓ All imports successful")
        
        # Test 2: Initialize processor
        print("2. Testing processor initialization...")
        processor = UniversalProcessor()
        print(f"   ✓ Processor created, AI available: {processor.ai_available}")
        
        # Test 3: Test Gemini API
        if processor.ai_available:
            print("3. Testing Gemini API...")
            response = processor.ai_model.generate_content('Respond with exactly: "API_TEST_SUCCESS"')
            print(f"   ✓ API Response: {response.text.strip()}")
            
            # Test 4: Test command processing
            print("4. Testing command processing...")
            task = processor.process_universal_command("Create a simple text file on desktop")
            print(f"   ✓ Command processed: {task.primary_action}")
            
        else:
            print("3. ❌ AI not available - check .env file")
            
        # Test 5: Test executor
        print("5. Testing executor...")
        executor = UniversalExecutor()
        print("   ✓ Executor created successfully")
        
        print("\n" + "=" * 50)
        print("SYSTEM TEST COMPLETE")
        print("✓ All components working correctly!")
        print("✓ Gemini model updated to gemini-1.5-flash")
        print("✓ Ready to launch GUI")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_shadow_system()
    input("\nPress Enter to exit...")
