# Personal Finance Chatbot

This project is an intelligent conversational AI system that leverages Groq's fast AI inference to provide personalized financial guidance.

## Features
- **Personalized financial advice** (savings, taxes, investments)
- **AI-generated responses** using Groq's LLaMA models
- **Demographic-aware communication** (student vs. professional)
- **Interactive chat interface** with history tracking
- **Quick-access sample questions** and financial tips

## Technologies
- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Groq API** - Fast AI inference for financial advice
- **LLaMA 3** - Advanced language model for responses

## Quick Setup

### 1. Install Dependencies
```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Configure Groq API
1. Get your free API key from [Groq Console](https://console.groq.com/)
2. Update `.env` file:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 3. Run the App
```powershell
streamlit run app.py
```

## Usage
1. Select your demographic (Student or Professional)
2. Ask financial questions in natural language
3. Get personalized, AI-powered advice
4. View chat history and explore sample questions

## Example Questions
- "How should I start building an emergency fund?"
- "What's the best investment strategy for a beginner?"
- "How can I optimize my taxes as a professional?"
- "Should I pay off student loans or invest?"

## File Structure
```
d:\gvpce\
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies (streamlit, groq, python-dotenv, requests)
├── .env               # API keys and configuration
├── .gitignore         # Git ignore file
├── README.md          # Project overview
└── SETUP.md           # Detailed setup instructions
```

## Dependencies
- **streamlit** - Web application framework
- **groq** - Fast AI inference API
- **python-dotenv** - Environment variable management  
- **requests** - HTTP library for API calls
