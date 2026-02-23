# Personal Finance Chatbot - Setup Instructions

## Getting Started with Groq API

### 1. Get your Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key

### 2. Configure Environment Variables
1. Open the `.env` file in your project directory
2. Replace `your_groq_api_key_here` with your actual Groq API key:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 3. Run the Application
```powershell
.venv\Scripts\Activate
streamlit run app.py
```

## Features

### Demographic-Aware Responses
- **Student Mode**: Simple language, budget basics, student-specific advice
- **Professional Mode**: Advanced strategies, investment advice, tax optimization

### AI-Powered Financial Guidance
- Personalized advice using Groq's fast LLaMA models
- Context-aware responses based on user demographic
- Real-time financial question answering

### Interactive Features
- Chat history tracking
- Quick-access sample questions
- Demographic-specific tips in sidebar
- Responsive user interface

## Supported Topics
- Budgeting and expense tracking
- Savings strategies
- Investment advice
- Tax planning
- Credit score improvement
- Emergency fund planning
- Debt management
- Retirement planning (professionals)
- Student loan advice (students)

## Troubleshooting
- If you see "Please configure your Groq API key", check your `.env` file
- Ensure your API key is valid and has not expired
- Check your internet connection for API calls
