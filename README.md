# AI Chatbot with Voice Support

An intelligent chatbot created by Geetansh Malik, powered by Google Gemini API.

## Features
- 🤖 Smart AI responses using Google Gemini
- 💬 Text chat interface
- 🎤 Voice input support
- 🔊 Voice output (text-to-speech)
- ⚙️ Settings panel with dark mode
- 🌍 Multi-language support (English, Hindi, etc.)

## Setup Instructions

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `config.example.py` to `config.py`
4. Get your free Gemini API key from https://aistudio.google.com/app/apikey
5. Add your API key to `config.py`
6. Run: `python chatbot_backend.py`
7. Open `index.html` in your browser

## Technologies Used
- Backend: Python, Flask, Google Gemini API
- Frontend: HTML, CSS, JavaScript
- NLP: NLTK
- Speech: Web Speech API

## Update `requirements.txt`

Make sure it has:

Flask==3.0.0
flask-cors==4.0.0
nltk==3.8.1
google-generativeai>=0.8.0
gunicorn==21.2.0

## Creator
Geetansh Malik
