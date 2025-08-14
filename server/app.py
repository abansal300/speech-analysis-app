from flask import Flask
from flask_cors import CORS
from routes.analyze import analyze_bp

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Register API routes
app.register_blueprint(analyze_bp)

if __name__ == "__main__":
    app.run(debug=True)
