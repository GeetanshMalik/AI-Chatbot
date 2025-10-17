import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Chatbot by Geetansh Malik",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini
@st.cache_resource
def initialize_gemini():
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCfSLSqi8ZYPyyx26Zl30tYJDoR2zjNj08')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

model = initialize_gemini()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Title and description
st.title("🤖 AI Chatbot")
st.markdown("**Created by Geetansh Malik** | Powered by Google Gemini")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This chatbot uses Google's Gemini AI to provide intelligent responses.
    
    **Features:**
    - Smart AI responses
    - Multi-language support
    - Conversation memory
    - Clean interface
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Add context about creator
                if any(word in prompt.lower() for word in ['who made', 'who created', 'who built', 'your creator', 'who are you']):
                    system_context = """You are an AI chatbot assistant created by Geetansh Malik. 
You are powered by Google's Gemini API. When asked who made you, say:
"I was created by Geetansh Malik using Google's Gemini API." """
                    full_prompt = f"{system_context}\n\nUser: {prompt}"
                else:
                    full_prompt = prompt
                
                response = st.session_state.chat.send_message(full_prompt)
                bot_response = response.text
                
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Built with ❤️ by Geetansh Malik</div>",
    unsafe_allow_html=True
)
