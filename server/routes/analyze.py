from flask import Blueprint, request, jsonify
from utils.stt import transcribe_audio
from utils.sentiment import analyze_sentiment
from utils.response import generate_response
from tts.speak import synthesize_speech

analyze_bp = Blueprint('analyze', __name__)

@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']
    
    # STT
    transcript = transcribe_audio(audio_file)
    
    # Sentiment
    sentiment = analyze_sentiment(transcript)
    
    # Generate response
    reply = generate_response(sentiment, transcript)
    
    # TTS
    audio_path = synthesize_speech(reply)

    return jsonify({
        "transcript": transcript,
        "sentiment": sentiment,
        "response": reply,
        "audio_url": audio_path
    }) 