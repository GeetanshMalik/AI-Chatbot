from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
import google.generativeai as genai
import os
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# Configure Gemini API
try:
    from config import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    # Fallback to environment variable if config.py doesn't exist
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
    else:
        print("⚠️ WARNING: No API key found! Please create config.py or set GEMINI_API_KEY environment variable")

# Initialize Gemini model (using current available model)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Conversation history for context
conversation_sessions = {}

def get_gemini_response(user_input, session_id="default"):
    """Get response from Google Gemini AI"""
    try:
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = model.start_chat(history=[])
        
        chat = conversation_sessions[session_id]
        
        system_context = """You are an AI chatbot assistant created by Geetansh Malik. 
You are powered by Google's Gemini API, which provides your intelligence and language capabilities.
When someone asks who made you or who created you, you should say:
"I was created by Geetansh Malik using Google's Gemini API for my AI capabilities."

You can chat in multiple languages including English, Hindi, and others.
Be helpful, friendly, and informative.

IMPORTANT FORMATTING RULES:
- When providing code, ALWAYS wrap it in triple backticks with the language name (```python, ```javascript, etc.)
- Use **bold** for emphasis
- Use bullet points with - or * for lists
- Use numbered lists with 1. 2. 3. for steps
- Keep responses well-structured and formatted
- For multi-step explanations, use clear numbered steps
- For code snippets, always use proper markdown code blocks"""

        # Prepend context only for questions about creator/identity
        if any(word in user_input.lower() for word in ['who made', 'who created', 'who built', 'your creator', 'your maker', 'who are you']):
            full_input = f"{system_context}\n\nUser question: {user_input}"
        else:
            full_input = user_input
        
        # Send message and get response
        response = chat.send_message(full_input)
        
        return response.text
    
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return get_fallback_response(user_input)

def get_fallback_response(user_input):
    """Provide intelligent fallback responses when API fails"""
    user_input_lower = user_input.lower()
    
    # Greetings
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! How can I assist you today?"
    
    # About the bot
    elif any(phrase in user_input_lower for phrase in ['who are you', 'what are you', 'your name']):
        return "I'm an AI chatbot & I was created by Geetansh Malik using Google's Gemini API for my AI capabilities. I'm here to chat and help you with questions!"
    
    # How are you
    elif any(phrase in user_input_lower for phrase in ['how are you', 'how do you do']):
        return "I'm functioning great! Thanks for asking. How can I help you today?"
    
    # Help
    elif any(word in user_input_lower for word in ['help', 'what can you do']):
        return "I can chat with you about various topics, answer questions, help with information, and have meaningful conversations! Try asking me anything."
    
    # Thanks
    elif any(word in user_input_lower for word in ['thank', 'thanks']):
        return "You're welcome! Feel free to ask me anything else."
    
    # Goodbye
    elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you']):
        return "Goodbye! Have a wonderful day! Come back anytime."
    
    # Time/Date
    elif any(word in user_input_lower for word in ['time', 'date', 'today']):
        now = datetime.now()
        return f"The current date and time is {now.strftime('%B %d, %Y at %I:%M %p')}."
    
    # Default
    else:
        return "I'm having trouble connecting to my AI service right now. Please check if the API key is configured correctly, or try again in a moment."

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get Gemini AI response
        bot_response = get_gemini_response(user_message, session_id)
        
        return jsonify({'response': bot_response})
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': 'Sorry, I encountered an error. Please make sure the API key is configured correctly.'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Chatbot is running!',
        'ai_model': 'Google Gemini 1.5 Flash'
    })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_sessions:
            conversation_sessions[session_id] = model.start_chat(history=[])
        
        return jsonify({'message': 'Conversation reset successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 Starting AI Chatbot Server with Google Gemini Integration")
    print("=" * 70)
    print("✅ Server running on http://localhost:5000")
    print("✅ Using Google Gemini 1.5 Flash AI Model")
    print("✅ Smart responses with conversation memory")
    print("\n💡 Make sure your API key is configured in config.py")
    print("📝 Open chatbot_frontend.html in your browser to start chatting!")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
