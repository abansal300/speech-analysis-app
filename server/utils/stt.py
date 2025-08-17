import speech_recognition as sr
import tempfile
import os

def transcribe_audio(audio_file):
    """
    Convert uploaded audio file to text using speech recognition
    """
    try:
        # Create a recognizer instance
        recognizer = sr.Recognizer()
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            temp_path = temp_file.name
        
        # Read the audio file
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        
        # Perform speech recognition
        transcript = recognizer.recognize_google(audio)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return transcript
        
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return "Could not transcribe audio"
