from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.analyze import analyze_bp
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Allow cross-origin requests

# Create static directory if it doesn't exist
os.makedirs('static', exist_ok=True)

# Register API routes
app.register_blueprint(analyze_bp)

# Serve static files (for TTS audio output)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
