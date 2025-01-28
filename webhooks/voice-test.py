import openai
import os

def test_voice():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        # Simple test message
        speech = openai.audio.speech.create(
            model="tts-1-hd",
            voice="shimmer",
            input="Hello, I am Dr. Lucy. Voice test initialized and working."
        )
        
        # Save test audio
        speech.stream_to_file("dr_lucy_test.mp3")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_voice()
    print("Test successful" if success else "Test failed")