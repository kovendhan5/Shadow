#!/usr/bin/env python3
"""
Quick test to verify Gemini API is working with updated model
"""
import sys
import os
sys.path.append('.')

from brain.universal_processor import UniversalProcessor

def test_gemini_model():
    """Test the updated Gemini model"""
    print("Testing Gemini API with updated model...")
    
    try:
        processor = UniversalProcessor()
        print(f"AI available: {processor.ai_available}")
        
        if processor.ai_available:
            print("Model loaded successfully with gemini-1.5-flash")
            
            # Test a simple API call
            test_response = processor.ai_model.generate_content('Hello, say hi back in one word')
            print(f"Test response: {test_response.text}")
            print("✓ Gemini API is working correctly!")
            return True
        else:
            print("❌ AI not available - check API key")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        return False

if __name__ == "__main__":
    test_gemini_model()
