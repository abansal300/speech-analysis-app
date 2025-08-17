import pyttsx3
import os
from datetime import datetime

def synthesize_speech(text):
    """
    Convert text to speech and save as WAV file
    Returns the URL path to the generated audio
    """
    try:
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        
        # Set properties for better quality
        engine.setProperty('rate', 150)    # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a good one
        voices = engine.getProperty('voices')
        if voices:
            # Try to use a female voice (often sounds more empathetic)
            for voice in voices:
                if 'female' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.wav"
        filepath = os.path.join("static", filename)
        
        # Generate speech and save to file
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        
        # Return the URL path
        return f"/static/{filename}"
        
    except Exception as e:
        print(f"Error in TTS: {e}")
        # Return a fallback audio file or error message
        return "/static/error.wav"

    