# voice_input.py
import speech_recognition as sr
import logging
import pyttsx3
import threading
from config import VOICE_ENABLED, VOICE_LANGUAGE, VOICE_TIMEOUT, VOICE_PHRASE_TIME_LIMIT

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.setup_voice_settings()
        self.calibrate_microphone()
    
    def setup_voice_settings(self):
        """Setup text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Try to find a female voice, otherwise use the first available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self.tts_engine.setProperty('voice', voices[0].id)
        
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.8)  # Volume level
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                logging.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logging.info("Microphone calibration complete")
        except Exception as e:
            logging.error(f"Error calibrating microphone: {e}")
    
    def speak(self, text: str):
        """Convert text to speech"""
        try:
            # Use a lock to prevent multiple TTS operations
            if not hasattr(self, '_tts_lock'):
                self._tts_lock = threading.Lock()
            
            def speak_thread():
                with self._tts_lock:
                    try:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    except RuntimeError as e:
                        if "run loop already started" in str(e):
                            # Try direct speech without runAndWait
                            self.tts_engine.say(text)
                        else:
                            raise e
            
            # Run TTS in a separate thread to avoid blocking
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.daemon = True
            thread.start()
            thread.join(timeout=5)  # Wait max 5 seconds for TTS
            
        except Exception as e:
            logging.error(f"Error in text-to-speech: {e}")
    
    def listen(self, prompt: str = None) -> str:
        """Listen for voice input and return recognized text"""
        if not VOICE_ENABLED:
            logging.warning("Voice input is disabled")
            return None
        
        try:
            if prompt:
                print(f"🎤 {prompt}")
                self.speak(prompt)
            else:
                print("🎤 Listening...")
                self.speak("I'm listening")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=VOICE_TIMEOUT, 
                    phrase_time_limit=VOICE_PHRASE_TIME_LIMIT
                )
            
            print("🔄 Processing...")
            
            # Try to recognize speech using Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
                logging.info(f"Voice input recognized: {text}")
                print(f"✅ You said: {text}")
                return text
            except sr.UnknownValueError:
                error_msg = "Sorry, I couldn't understand what you said. Please try again."
                logging.warning("Speech recognition failed - unknown value")
                print(f"❌ {error_msg}")
                self.speak(error_msg)
                return None
            except sr.RequestError as e:
                error_msg = f"Could not request results from speech recognition service: {e}"
                logging.error(error_msg)
                print(f"❌ {error_msg}")
                self.speak("Sorry, there was an error with the speech recognition service.")
                return None
        
        except sr.WaitTimeoutError:
            error_msg = "Listening timeout. No speech detected."
            logging.warning(error_msg)
            print(f"⏰ {error_msg}")
            self.speak("I didn't hear anything. Please try again.")
            return None
        except Exception as e:
            error_msg = f"Error during voice input: {e}"
            logging.error(error_msg)
            print(f"❌ {error_msg}")
            self.speak("Sorry, there was an error with voice input.")
            return None
    
    def listen_for_confirmation(self, question: str) -> bool:
        """Listen for yes/no confirmation"""
        try:
            self.speak(question)
            print(f"🤔 {question}")
            
            response = self.listen()
            if response:
                response_lower = response.lower()
                if any(word in response_lower for word in ['yes', 'yeah', 'yep', 'confirm', 'ok', 'okay', 'sure']):
                    return True
                elif any(word in response_lower for word in ['no', 'nope', 'cancel', 'stop', 'abort']):
                    return False
            
            # If unclear, ask for clarification
            self.speak("I didn't understand. Please say yes or no.")
            return self.listen_for_confirmation("Please confirm: yes or no?")
        
        except Exception as e:
            logging.error(f"Error in confirmation: {e}")
            return False

# Create a global voice input instance
voice_input = VoiceInput()

def get_voice_input(prompt: str = None) -> str:
    """Get voice input from user"""
    return voice_input.listen(prompt)

def speak_response(text: str):
    """Speak a response to the user"""
    voice_input.speak(text)

def confirm_action(question: str) -> bool:
    """Ask for voice confirmation"""
    return voice_input.listen_for_confirmation(question)
