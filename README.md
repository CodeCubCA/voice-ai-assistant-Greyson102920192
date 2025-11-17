[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant

A voice-enabled AI chatbot powered by Google's Gemini AI with multi-language support and customizable personalities.

## Features

- **Voice Input**: Record voice messages in multiple languages
- **Multi-Language Support**: English, French, Spanish, Mandarin, and Cantonese
- **Multiple Personalities**:
  - General Assistant - Balanced, helpful responses
  - Study Buddy - Patient tutor for learning
  - Fitness Coach - Motivating workout and nutrition guide
  - Gaming Coach - Strategic gaming tips and analysis
- **Real-time Transcription**: Automatic voice-to-text conversion
- **Chat History**: Maintains conversation context
- **Modern UI**: Clean Streamlit interface

## Technologies Used

- **Streamlit**: Web interface
- **Google Gemini AI**: AI responses (gemini-2.5-flash model)
- **Google Speech Recognition**: Voice transcription
- **Python**: Backend logic

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeCubCA/voice-ai-assistant-Greyson102920192.git
cd voice-ai-assistant-Greyson102920192
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Select a Personality**: Choose from General Assistant, Study Buddy, Fitness Coach, or Gaming Coach
2. **Choose Language**: Select your preferred voice input language
3. **Start Chatting**:
   - Type messages in the text box, or
   - Click the microphone icon to record voice messages
4. **Clear History**: Use the "Clear Chat History" button in the sidebar to start fresh

## Project Structure

```
voice-ai-assistant/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # API keys (not committed)
└── README.md          # This file
```

## API Keys

You need a Google Gemini API key to run this project. Get yours at:
https://makersuite.google.com/app/apikey

## License

This project is part of a classroom assignment.