import streamlit as st
import requests
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, try to load .env manually
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except:
        GROQ_API_KEY = ""

# Professional page config
st.set_page_config(
    page_title="Assistant",
    page_icon="◉",
    layout="centered"
)

# Ultra-professional CSS
st.markdown("""
<style>
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Clean white/gray theme */
    .stApp {
        background: #f5f5f5;
    }
    
    /* Minimalist title */
    h1 {
        color: #2c2c2c !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 200;
        font-size: 24px;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    /* Chat container */
    [data-testid="stChatMessageContainer"] {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Message styling */
    .stChatMessage {
        background-color: transparent;
        padding: 10px 0;
    }
    
    /* User messages - aligned right */
    [data-testid="chat-message-user"] {
        background: #f8f8f8;
        border-left: 3px solid #888;
        padding-left: 10px;
        margin: 10px 0;
    }
    
    /* Assistant messages - aligned left */
    [data-testid="chat-message-assistant"] {
        background: white;
        border-left: 3px solid #333;
        padding-left: 10px;
        margin: 10px 0;
    }
    
    /* Text color */
    [data-testid="chatMessageContent"] {
        color: #333;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Input field */
    .stChatInput > div > div {
        background-color: white !important;
        border: 1px solid #ddd !important;
        border-radius: 4px;
        color: #333 !important;
    }
    
    .stChatInput textarea {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Clean button */
    .stButton > button {
        background-color: white;
        color: #666;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-weight: 400;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 8px 16px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #f8f8f8;
        border-color: #999;
        color: #333;
    }
    
    /* Spinner */
    .stSpinner {
        color: #666;
    }
    
    /* Avatar overrides */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {
        background: transparent;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

def get_response(message, history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build conversation history for context
    messages = []
    for msg in history[-6:]:  # Last 3 exchanges for context
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return "I apologize, but I'm unable to process your request at the moment."

# Title
st.markdown("# Assistant")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Professional avatars - using simple text
AVATARS = {
    "user": "U",      # Simple "U" for User
    "assistant": "A"  # Simple "A" for Assistant
}

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
        st.write(msg["content"])

# Input handling
if prompt := st.chat_input("Message"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        with st.spinner(""):
            response = get_response(prompt, st.session_state.messages)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Minimalist clear button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("CLEAR", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
