import openai
import os
from google.cloud import aiplatform

# Voice configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
endpoint_id = "6296186210691842048"

def setup_voice_connection():
    # Initialize voice endpoint
    voice_config = {
        "model": "tts-1-hd",
        "voice": "shimmer",
        "response_format": "mp3"
    }
    
    # Test voice generation
    try:
        response = openai.audio.speech.create(
            model=voice_config["model"],
            voice=voice_config["voice"],
            input="Dr. Lucy voice test initialization."
        )
        print("Voice synthesis working")
        return True
    except Exception as e:
        print(f"Voice error: {e}")
        return False

if __name__ == "__main__":
    setup_voice_connection()