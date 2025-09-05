import streamlit as st
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

def get_response(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",  # Change this if model gets deprecated
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 150
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"

st.title("ChatBot")

if not GROQ_API_KEY:
    st.error("groq API key not found, set the GROQ_API_KEY environment variable or add it to streamlit secrets.")
    st.info("💡 Get your API key from: https://console.groq.com/keys")
    st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Clear"):
    st.session_state.messages = []
    st.rerun()