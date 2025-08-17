# 🎤 Emotional Support AI - Speech Analysis & Response System

A sophisticated AI-powered mental health support application that listens to users' emotional states through speech, analyzes their feelings using advanced sentiment analysis, and responds with personalized, empathetic support through both text and synthesized speech.

## 🚀 Features

### **Core AI Capabilities**
- **🎯 Real-time Speech Recognition** - Converts spoken words to text using Google's Speech Recognition API
- **🧠 Advanced Sentiment Analysis** - Analyzes emotional states using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **💬 Intelligent Response Generation** - Creates contextually appropriate, supportive responses based on detected emotions
- **🔊 Text-to-Speech Synthesis** - Converts AI responses to natural-sounding speech using pyttsx3

### **Technical Architecture**
- **Backend**: Flask REST API with modular, scalable design
- **Frontend**: React.js with modern UI/UX (in development)
- **Audio Processing**: Support for multiple audio formats (WAV, MP3, M4A)
- **Real-time Processing**: End-to-end emotional analysis pipeline
- **Cross-Origin Support**: CORS-enabled for web integration

## 🏗️ System Architecture

```
User Speech → STT → Sentiment Analysis → Response Generation → TTS → Audio Response
     ↓           ↓           ↓              ↓              ↓         ↓
  Microphone  Google SR   VADER AI    Custom Logic    pyttsx3   User Hears
```

## 🛠️ Technology Stack

### **Backend Technologies**
- **Python 3.12** - Core application logic
- **Flask** - RESTful API framework
- **Flask-CORS** - Cross-origin resource sharing
- **SpeechRecognition** - Google Speech-to-Text integration
- **VADER Sentiment** - Advanced emotional analysis
- **pyttsx3** - Text-to-speech synthesis
- **Werkzeug** - File handling and utilities

### **Frontend Technologies** (In Development)
- **React 19** - Modern JavaScript framework
- **Audio Recording** - Real-time microphone input
- **Responsive Design** - Mobile and desktop optimized

### **Development Tools**
- **Git** - Version control
- **VS Code** - Development environment
- **Anaconda** - Python environment management

## 🚀 Getting Started

### **Prerequisites**
- Python 3.12+
- Anaconda (recommended)
- Node.js 18+ (for frontend development)

### **Backend Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd speech

# Navigate to backend
cd server

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### **Frontend Setup** (Coming Soon)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🔌 API Endpoints

### **POST /analyze**
Analyzes uploaded audio and returns emotional analysis with AI response.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `audio` file (WAV, MP3, M4A)

**Response:**
```json
{
  "transcript": "I'm feeling anxious about my presentation",
  "sentiment": {
    "sentiment": "negative",
    "compound": -0.6,
    "positive": 0.0,
    "negative": 0.8,
    "neutral": 0.2
  },
  "response": "I understand that presentations can be really stressful...",
  "audio_url": "/static/response_20240816_193000.wav"
}
```

## 🔬 How It Works

### **1. Speech Input**
Users can upload audio files or record directly through the interface (frontend in development).

### **2. Speech-to-Text Processing**
Audio is processed using Google's Speech Recognition API for high-accuracy transcription.

### **3. Emotional Analysis**
VADER sentiment analysis examines the text for emotional content, providing:
- Overall sentiment classification (positive/negative/neutral)
- Compound sentiment score (-1.0 to +1.0)
- Individual positive, negative, and neutral scores

### **4. Intelligent Response Generation**
Custom logic generates contextually appropriate responses based on:
- Detected emotional state
- Sentiment intensity
- User's specific words and context

### **5. Speech Synthesis**
AI responses are converted to natural speech using pyttsx3, creating an immersive conversational experience.

