# Simple TTS fallback for Windows SAPI
import os

def speak(text):
    """Simple TTS using Windows SAPI (built-in Windows speech)"""
    try:
        # Use Windows built-in text-to-speech
        os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
    except Exception as e:
        print(f"[TTS] Error: {e}, falling back to print")
        print(f"[SPEECH] {text}")
