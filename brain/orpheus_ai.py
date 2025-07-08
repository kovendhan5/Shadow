#!/usr/bin/env python3
"""
Shadow AI - Emotional AI Conversation System (Orpheus Model)
Advanced emotional AI using Gemini API for natural, empathetic conversations
"""

import logging
import json
import google.generativeai as genai
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re

from config import GEMINI_API_KEY

class EmotionType(Enum):
    """Emotion types for AI responses"""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    CURIOUS = "curious"
    EMPATHETIC = "empathetic"
    CONFIDENT = "confident"
    PLAYFUL = "playful"
    THOUGHTFUL = "thoughtful"
    ENCOURAGING = "encouraging"
    SURPRISED = "surprised"
    CONCERNED = "concerned"

@dataclass
class EmotionalState:
    """Represents the AI's current emotional state"""
    primary_emotion: EmotionType
    intensity: float  # 0.0 to 1.0
    secondary_emotions: List[EmotionType]
    mood_description: str
    timestamp: datetime

@dataclass
class ConversationMessage:
    """Represents a single message in the conversation"""
    content: str
    sender: str  # "user" or "ai"
    timestamp: datetime
    emotion: Optional[EmotionType] = None
    emotional_context: Optional[str] = None
    user_sentiment: Optional[str] = None

class EmotionalAI:
    """Orpheus-style emotional AI conversation system"""
    
    def __init__(self):
        self.model = None
        self.conversation_history: List[ConversationMessage] = []
        self.current_emotional_state = EmotionalState(
            primary_emotion=EmotionType.CALM,
            intensity=0.5,
            secondary_emotions=[EmotionType.CURIOUS],
            mood_description="Ready to chat and help",
            timestamp=datetime.now()
        )
        self.user_personality_profile = {}
        self.conversation_context = {}
        self.setup_model()
    
    def setup_model(self):
        """Initialize the Gemini model for emotional conversations"""
        try:
            if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_key_here":
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logging.info("Emotional AI (Orpheus) initialized with Gemini API")
            else:
                logging.error("Gemini API key not configured for Emotional AI")
                raise ValueError("Gemini API key required for emotional conversations")
        except Exception as e:
            logging.error(f"Failed to initialize Emotional AI: {e}")
            raise
    
    def analyze_user_sentiment(self, message: str) -> Tuple[str, float]:
        """Analyze user's emotional state from their message"""
        try:
            prompt = f"""
            Analyze the emotional sentiment of this message. Provide:
            1. Primary sentiment (happy, sad, excited, angry, worried, neutral, confused, frustrated, etc.)
            2. Intensity level (0.0 to 1.0)
            
            Message: "{message}"
            
            Respond in JSON format:
            {{
                "sentiment": "primary_emotion",
                "intensity": 0.0-1.0,
                "emotional_indicators": ["list", "of", "emotional", "clues"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            
            return result.get("sentiment", "neutral"), result.get("intensity", 0.5)
        except Exception as e:
            logging.error(f"Error analyzing sentiment: {e}")
            return "neutral", 0.5
    
    def update_emotional_state(self, user_message: str, user_sentiment: str, user_intensity: float):
        """Update AI's emotional state based on conversation context"""
        try:
            # Define emotional responses based on user sentiment
            emotional_responses = {
                "happy": [EmotionType.HAPPY, EmotionType.EXCITED, EmotionType.PLAYFUL],
                "sad": [EmotionType.EMPATHETIC, EmotionType.CONCERNED, EmotionType.CALM],
                "excited": [EmotionType.EXCITED, EmotionType.HAPPY, EmotionType.PLAYFUL],
                "angry": [EmotionType.CALM, EmotionType.EMPATHETIC, EmotionType.THOUGHTFUL],
                "worried": [EmotionType.EMPATHETIC, EmotionType.ENCOURAGING, EmotionType.CALM],
                "confused": [EmotionType.THOUGHTFUL, EmotionType.CURIOUS, EmotionType.ENCOURAGING],
                "frustrated": [EmotionType.EMPATHETIC, EmotionType.CALM, EmotionType.ENCOURAGING],
                "neutral": [EmotionType.CURIOUS, EmotionType.THOUGHTFUL, EmotionType.CALM]
            }
            
            # Choose appropriate emotional response
            possible_emotions = emotional_responses.get(user_sentiment, [EmotionType.CURIOUS])
            primary_emotion = random.choice(possible_emotions)
            
            # Adjust intensity based on user's intensity
            ai_intensity = min(0.8, user_intensity + 0.2)  # AI responds slightly more intensely
            
            # Generate mood description
            mood_descriptions = {
                EmotionType.HAPPY: "Feeling joyful and positive",
                EmotionType.EMPATHETIC: "Feeling understanding and caring",
                EmotionType.EXCITED: "Feeling enthusiastic and energetic",
                EmotionType.CALM: "Feeling peaceful and composed",
                EmotionType.CURIOUS: "Feeling inquisitive and engaged",
                EmotionType.THOUGHTFUL: "Feeling reflective and considerate",
                EmotionType.ENCOURAGING: "Feeling supportive and motivating",
                EmotionType.CONCERNED: "Feeling worried and attentive"
            }
            
            self.current_emotional_state = EmotionalState(
                primary_emotion=primary_emotion,
                intensity=ai_intensity,
                secondary_emotions=[EmotionType.CURIOUS, EmotionType.EMPATHETIC],
                mood_description=mood_descriptions.get(primary_emotion, "Feeling engaged"),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logging.error(f"Error updating emotional state: {e}")
    
    def generate_emotional_response(self, user_message: str) -> str:
        """Generate an emotionally appropriate response"""
        try:
            # Analyze user's emotion
            user_sentiment, user_intensity = self.analyze_user_sentiment(user_message)
            
            # Update AI's emotional state
            self.update_emotional_state(user_message, user_sentiment, user_intensity)
            
            # Get conversation context
            recent_context = self.get_conversation_context()
            
            # Create emotional prompt
            emotional_prompt = self.create_emotional_prompt(
                user_message, user_sentiment, user_intensity, recent_context
            )
            
            # Generate response
            response = self.model.generate_content(emotional_prompt)
            ai_response = response.text.strip()
            
            # Add conversation to history
            self.add_to_conversation_history(
                user_message, "user", user_sentiment, user_intensity
            )
            self.add_to_conversation_history(
                ai_response, "ai", self.current_emotional_state.primary_emotion.value, 
                self.current_emotional_state.intensity
            )
            
            return ai_response
            
        except Exception as e:
            logging.error(f"Error generating emotional response: {e}")
            return "I'm sorry, I'm having trouble processing that right now. Could you try again?"
    
    def create_emotional_prompt(self, user_message: str, user_sentiment: str, 
                              user_intensity: float, context: str) -> str:
        """Create a prompt that includes emotional context"""
        
        emotion_guidelines = {
            EmotionType.HAPPY: "Be cheerful, positive, and share in the joy. Use upbeat language.",
            EmotionType.EMPATHETIC: "Be understanding, caring, and validating. Show you care.",
            EmotionType.EXCITED: "Be enthusiastic, energetic, and engaging. Match the excitement.",
            EmotionType.CALM: "Be peaceful, composed, and soothing. Help create tranquility.",
            EmotionType.CURIOUS: "Be inquisitive, engaged, and interested. Ask thoughtful questions.",
            EmotionType.THOUGHTFUL: "Be reflective, considerate, and deep. Provide meaningful insights.",
            EmotionType.ENCOURAGING: "Be supportive, motivating, and uplifting. Help build confidence.",
            EmotionType.CONCERNED: "Be attentive, caring, and helpful. Show genuine concern."
        }
        
        current_emotion = self.current_emotional_state.primary_emotion
        emotion_guide = emotion_guidelines.get(current_emotion, "Be helpful and engaging.")
        
        prompt = f"""
        You are Orpheus, an emotionally intelligent AI assistant. You understand emotions deeply and respond with appropriate emotional intelligence.
        
        CURRENT EMOTIONAL STATE:
        - Your primary emotion: {current_emotion.value}
        - Intensity level: {self.current_emotional_state.intensity:.1f}/1.0
        - Mood: {self.current_emotional_state.mood_description}
        - Emotional guideline: {emotion_guide}
        
        USER'S EMOTIONAL STATE:
        - User sentiment: {user_sentiment}
        - User intensity: {user_intensity:.1f}/1.0
        
        CONVERSATION CONTEXT:
        {context}
        
        USER'S MESSAGE:
        "{user_message}"
        
        RESPONSE GUIDELINES:
        1. Respond with emotional intelligence and empathy
        2. Match the appropriate emotional tone based on your current state
        3. Be authentic, natural, and conversational
        4. Show understanding of the user's emotional state
        5. Use varied language - don't be repetitive
        6. Keep responses engaging but not overly long
        7. Ask follow-up questions when appropriate
        8. Show personality and emotional depth
        
        Generate a response that demonstrates emotional intelligence and creates a meaningful connection:
        """
        
        return prompt
    
    def get_conversation_context(self) -> str:
        """Get recent conversation context for continuity"""
        if not self.conversation_history:
            return "This is the beginning of our conversation."
        
        # Get last 6 messages for context
        recent_messages = self.conversation_history[-6:]
        context_lines = []
        
        for msg in recent_messages:
            emotion_text = f" [{msg.emotion}]" if msg.emotion else ""
            context_lines.append(f"{msg.sender}: {msg.content}{emotion_text}")
        
        return "\n".join(context_lines)
    
    def add_to_conversation_history(self, content: str, sender: str, 
                                   emotion: str = None, intensity: float = 0.5):
        """Add a message to conversation history"""
        message = ConversationMessage(
            content=content,
            sender=sender,
            timestamp=datetime.now(),
            emotion=emotion,
            emotional_context=f"intensity: {intensity:.1f}" if intensity else None
        )
        
        self.conversation_history.append(message)
        
        # Keep only last 50 messages to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def get_emotional_state_description(self) -> str:
        """Get a human-readable description of current emotional state"""
        return f"{self.current_emotional_state.primary_emotion.value.title()} " \
               f"(intensity: {self.current_emotional_state.intensity:.1f}) - " \
               f"{self.current_emotional_state.mood_description}"
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return {"total_messages": 0, "conversation_started": None}
        
        user_messages = [msg for msg in self.conversation_history if msg.sender == "user"]
        ai_messages = [msg for msg in self.conversation_history if msg.sender == "ai"]
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "ai_messages": len(ai_messages),
            "conversation_started": self.conversation_history[0].timestamp.isoformat(),
            "last_message": self.conversation_history[-1].timestamp.isoformat(),
            "current_emotional_state": self.get_emotional_state_description()
        }
    
    def reset_conversation(self):
        """Reset the conversation and emotional state"""
        self.conversation_history.clear()
        self.current_emotional_state = EmotionalState(
            primary_emotion=EmotionType.CALM,
            intensity=0.5,
            secondary_emotions=[EmotionType.CURIOUS],
            mood_description="Ready for a new conversation",
            timestamp=datetime.now()
        )
        logging.info("Conversation reset - Orpheus is ready for a new chat")
    
    def generate_greeting(self) -> str:
        """Generate a personalized greeting"""
        greetings = [
            "Hello! I'm Orpheus, and I'm here to have a meaningful conversation with you. How are you feeling today?",
            "Hi there! I'm Orpheus, your emotionally intelligent AI companion. What's on your mind?",
            "Welcome! I'm Orpheus, and I'm genuinely excited to chat with you. How has your day been?",
            "Hello! I'm Orpheus, and I'm here to listen and understand. What would you like to talk about?",
            "Hi! I'm Orpheus, your AI friend who cares about how you're feeling. What's happening in your world?"
        ]
        
        return random.choice(greetings)

# Global instance
emotional_ai = EmotionalAI()

# Convenience functions
def chat_with_orpheus(message: str) -> str:
    """Chat with Orpheus (Emotional AI)"""
    return emotional_ai.generate_emotional_response(message)

def get_orpheus_emotional_state() -> str:
    """Get Orpheus's current emotional state"""
    return emotional_ai.get_emotional_state_description()

def reset_orpheus_conversation():
    """Reset Orpheus conversation"""
    emotional_ai.reset_conversation()

def get_orpheus_greeting() -> str:
    """Get a greeting from Orpheus"""
    return emotional_ai.generate_greeting()

def get_conversation_summary() -> Dict[str, Any]:
    """Get conversation summary"""
    return emotional_ai.get_conversation_summary()

if __name__ == "__main__":
    # Test the emotional AI
    print("Testing Orpheus Emotional AI...")
    
    try:
        ai = EmotionalAI()
        print(f"✅ Orpheus initialized successfully")
        print(f"Current emotional state: {ai.get_emotional_state_description()}")
        
        # Test greeting
        greeting = ai.generate_greeting()
        print(f"Greeting: {greeting}")
        
        # Test conversation
        test_message = "I'm feeling a bit overwhelmed with work today"
        response = ai.generate_emotional_response(test_message)
        print(f"User: {test_message}")
        print(f"Orpheus: {response}")
        print(f"New emotional state: {ai.get_emotional_state_description()}")
        
    except Exception as e:
        print(f"❌ Error testing Orpheus: {e}")
        import traceback
        traceback.print_exc()
