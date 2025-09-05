# LLM Chatbot

A chatbot built with Streamlit and Groq's API.

## Features

- Web-based chat interface
- Connects to Groq's language models (Llama 3.1)
- Maintains conversation history during session
- ~60 lines of Python

## Setup

### Requirements

- Python 3.8+
- Groq API key from [console.groq.com/keys](https://console.groq.com/keys)

### Installation

```bash
git clone https://github.com/AshDubey8/the-most-basic-ai-chatbot-ever.git
cd the-most-basic-ai-chatbot-ever
pip install streamlit requests
```

### Configuration

1. Get a Groq API key from [console.groq.com/keys](https://console.groq.com/keys)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

## Usage

```bash
streamlit run app.py
```

Opens at http://localhost:8501

## How It Works

1. **User input** → Streamlit text field
2. **API call** → POST request to Groq
3. **Response** → JSON parsing
4. **Display** → Streamlit chat UI
5. **History** → Session state storage

## Configuration Options

**Model (line 16):**
```python
"model": "llama-3.1-8b-instant"
```
Alternatives: `gemma2-9b-it`, `llama-3.3-70b-versatile`

**Response Length (line 18):**
```python
"max_tokens": 150
```

**Temperature (line 19):**
```python
"temperature": 0.7  # 0.0-1.0
```

## File Structure

```
chatbot/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Troubleshooting

- **401 Error**: Check API key
- **429 Error**: Rate limit, wait and retry
- **Model deprecated**: Check current models

## Current Limitations

- Chat history clears on page refresh  
- Each message is sent independently without conversation context
- Basic error handling only
- No streaming responses (displays after generation completes)

## License

MIT
