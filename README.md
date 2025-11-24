[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant 🤖🗣️

A sophisticated voice-enabled AI chatbot powered by Google's Gemini AI featuring multi-language support, customizable personalities, and high-quality text-to-speech using AWS Polly. Communicate naturally in 7 different languages with real-time voice transcription and AI-generated audio responses.

## Features

### 🎙️ Voice Input & Recognition
- **Multi-Language Voice Input**: Record voice messages in 7 languages
- **Real-time Transcription**: Automatic voice-to-text conversion using Google Speech Recognition
- **Language-Specific Recognition**: Optimized recognition for each language

### 🌍 Multi-Language Support
Support for **7 languages** with native voice options:
- 🇺🇸 **English** (US)
- 🇫🇷 **French** (Canadian)
- 🇪🇸 **Spanish** (US)
- 🇨🇳 **Mandarin Chinese**
- 🇭🇰 **Cantonese Chinese**
- 🇯🇵 **Japanese**
- 🇰🇷 **Korean**

### 🔊 High-Quality Text-to-Speech (AWS Polly)
- **19 Voice Options** across all languages
- **Standard Engine**: English, French, Spanish, Japanese (cost-effective, high quality)
- **Neural Engine**: Mandarin, Cantonese, Korean (premium quality, more natural)
- **Automatic Language Matching**: AI responds in your selected language
- **Dynamic Voice Selection**: Voice options update based on chosen language

### 🎭 Multiple AI Personalities
- **General Assistant** - Balanced, helpful responses for everyday tasks
- **Study Buddy** - Patient tutor for learning and academic support
- **Fitness Coach** - Motivating workout and nutrition guidance
- **Gaming Coach** - Strategic gaming tips and competitive analysis

### 💬 Smart Conversation Features
- **Context-Aware Responses**: Maintains conversation history (last 5 messages)
- **Personality-Based Responses**: AI adapts tone and style to selected personality
- **Language-Aware AI**: AI automatically responds in your selected language
- **Chat History**: Full conversation history with audio playback
- **Auto-Generated Audio**: Every AI response is automatically converted to speech

### 🎨 Modern User Interface
- **Clean Streamlit Interface**: Professional, easy-to-use design
- **Sidebar Controls**: Easy access to all settings
- **Audio Players**: Inline audio playback for all AI responses
- **Visual Feedback**: Loading spinners and status messages

## Technologies Used

| Technology | Purpose | Details |
|------------|---------|---------|
| **Streamlit** | Web Interface | Modern, responsive UI framework |
| **Google Gemini AI** | AI Responses | gemini-2.5-flash model for fast, intelligent responses |
| **Google Speech Recognition** | Voice Transcription | Real-time speech-to-text conversion |
| **AWS Polly** | Text-to-Speech | High-quality audio generation (Standard & Neural engines) |
| **boto3** | AWS SDK | Python library for AWS service integration |
| **Python 3.8+** | Backend | Core application logic |

## Key Highlights

✅ **19 Professional Voices** across 7 languages
✅ **Language-Aware AI** - Automatically responds in your selected language
✅ **Neural TTS** for Mandarin, Cantonese, and Korean
✅ **4 Unique Personalities** tailored for different use cases
✅ **Real-Time Voice Input** with automatic transcription
✅ **Context-Aware Conversations** remembering recent messages
✅ **No Rate Limits** - Powered by AWS Polly instead of free gTTS
✅ **Production-Ready** - Professional audio quality

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Gemini API key
- AWS Account with Polly access
- AWS Access Key ID and Secret Access Key

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
   - Add your API keys and AWS credentials to `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=ca-central-1
```

4. Run the application:
```bash
streamlit run app.py
```

## Available Voices

### English (8 voices - Standard Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Joanna | Female | US English (default) |
| Matthew | Male | US English |
| Kendra | Female | US English |
| Kimberly | Female | US English |
| Salli | Female | US English |
| Joey | Male | US English |
| Ivy | Female | US English (Child) |
| Justin | Male | US English (Child) |

### French (3 voices - Standard Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Chantal | Female | Canadian French |
| Mathieu | Male | French |
| Léa | Female | French |

### Spanish (3 voices - Standard Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Lupe | Female | US Spanish |
| Miguel | Male | US Spanish |
| Penélope | Female | US Spanish |

### Mandarin Chinese (1 voice - Neural Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Zhiyu | Female | Mandarin Chinese (High Quality) |

### Cantonese Chinese (1 voice - Neural Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Hiujin | Female | Cantonese Chinese (High Quality) |

### Japanese (2 voices - Standard Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Mizuki | Female | Japanese |
| Takumi | Male | Japanese |

### Korean (2 voices - Neural Engine)
| Voice Name | Gender | Description |
|------------|--------|-------------|
| Seoyeon | Female | Korean (High Quality) |
| Sumi | Female | Korean (High Quality, Warm) |

## Usage

1. **Select a Personality**: Choose from General Assistant, Study Buddy, Fitness Coach, or Gaming Coach
2. **Choose Language**: Select your preferred voice input language (English, French, Spanish, Mandarin, Cantonese, Japanese, or Korean)
3. **Select TTS Voice**: Choose your preferred text-to-speech voice from the available options for your selected language
4. **Start Chatting**:
   - Type messages in the text box, or
   - Click the microphone icon to record voice messages
   - AI will respond in the same language you selected
   - AI responses are automatically converted to speech and played
5. **Listen to Responses**: Click the audio player to hear the AI's response
6. **Clear History**: Use the "Clear Chat History" button in the sidebar to start a new conversation

### Example Workflow
1. Select "French" as your language
2. Choose "Mathieu (Male)" as your TTS voice
3. Record or type "Bonjour, comment ça va?"
4. AI responds in French with Mathieu's voice
5. All subsequent responses will be in French

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

### Google Gemini API Key
Get your Gemini API key at: https://makersuite.google.com/app/apikey

### AWS Credentials
1. Create an AWS account at https://aws.amazon.com
2. Create an IAM user with Polly access permissions
3. Generate access keys for the IAM user
4. Add the credentials to your `.env` file

### IAM Policy for AWS Polly
Your IAM user needs the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "polly:SynthesizeSpeech"
            ],
            "Resource": "*"
        }
    ]
}
```

## Troubleshooting

### TTS Audio Not Playing
- **Check AWS Credentials**: Verify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `.env`
- **Check Region**: Ensure `AWS_REGION` is set to `ca-central-1` (or your preferred region)
- **IAM Permissions**: Verify your IAM user has `polly:SynthesizeSpeech` permission
- **Check Console**: Look for error messages in the terminal where Streamlit is running

### Voice Recognition Not Working
- **Microphone Access**: Ensure your browser has microphone permissions
- **Audio Quality**: Speak clearly and ensure minimal background noise
- **Language Match**: Ensure you've selected the correct language for voice input
- **Browser Compatibility**: Use Chrome or Edge for best results

### AI Not Responding in Selected Language
- **Clear Chat History**: Click "Clear Chat History" and try again
- **Language Selection**: Verify the correct language is selected in the sidebar
- **Reload Page**: Refresh the browser page to reset the session

### Installation Issues
- **Python Version**: Ensure you're using Python 3.8 or higher
- **Dependencies**: Run `pip install -r requirements.txt` again
- **Virtual Environment**: Consider using a virtual environment to avoid conflicts

### AWS Polly Costs
- **Standard Engine**: ~$4 per 1 million characters
- **Neural Engine**: ~$16 per 1 million characters
- **Free Tier**: 5 million characters per month for first 12 months (Standard voices)
- Typical usage: A 100-word response costs approximately $0.001-$0.004

## License

This project is part of a classroom assignment.