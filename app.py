import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import tempfile
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize AWS Polly client
polly_client = boto3.client(
    'polly',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "ca-central-1")
)

# Function to convert audio to text
def transcribe_audio(audio_bytes, language_code="en-US"):
    """Convert audio bytes to text using Google Speech Recognition"""
    if audio_bytes is None:
        return "[No audio data received]"

    temp_audio_path = None
    try:
        # Initialize recognizer with optimized settings
        recognizer = sr.Recognizer()

        # More sensitive settings for better recognition
        recognizer.energy_threshold = 200  # Lower = more sensitive
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8  # How long to wait for phrase to end
        recognizer.phrase_threshold = 0.3  # Minimum seconds of speaking audio
        recognizer.non_speaking_duration = 0.5  # Seconds of silence before considering speech ended

        # Save audio bytes to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", mode='wb') as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        print(f"[Transcription] Audio saved: {len(audio_bytes)} bytes")

        # Read and transcribe the audio file
        with sr.AudioFile(temp_audio_path) as source:
            # Reduce ambient noise adjustment duration for faster processing
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)

        # Try Google Speech Recognition with language hint
        print(f"[Transcription] Calling Google Speech Recognition API with language: {language_code}...")
        text = recognizer.recognize_google(
            audio_data,
            language=language_code,
            show_all=False     # Return best result only
        )
        print(f"[Transcription] SUCCESS: '{text}'")

        return text

    except sr.UnknownValueError:
        print("[Transcription] FAILED: Could not understand audio")
        return "[Could not understand audio - please speak more clearly and ensure your microphone is working]"
    except sr.RequestError as e:
        print(f"[Transcription] API ERROR: {e}")
        return f"[Speech recognition service error: {e}]"
    except Exception as e:
        print(f"[Transcription] UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"[Error: {e}]"
    finally:
        # Clean up temp file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.unlink(temp_audio_path)
            except Exception as e:
                print(f"Could not delete temp file: {e}")

# Function to convert text to speech
def text_to_speech(text, voice_id="Joanna", language_code="en-US", engine="standard"):
    """Convert text to speech using AWS Polly and return audio bytes"""
    try:
        # Request speech synthesis from AWS Polly
        response = polly_client.synthesize_speech(
            Engine=engine,
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=text,
            LanguageCode=language_code
        )

        # Read audio stream from response
        if "AudioStream" in response:
            audio_stream = response["AudioStream"].read()
            return audio_stream
        else:
            print("[TTS] Error: No AudioStream in response")
            return None

    except (BotoCoreError, ClientError) as e:
        print(f"[TTS] AWS Polly Error: {e}")
        return None
    except Exception as e:
        print(f"[TTS] Error: {e}")
        return None

# Personality configurations
PERSONALITIES = {
    "General Assistant": {
        "system_prompt": "You are a helpful, friendly, and knowledgeable AI assistant. You provide clear, accurate, and thoughtful responses to help users with their questions and tasks.",
        "description": "A balanced, helpful assistant for general purposes",
        "emoji": "🤖"
    },
    "Study Buddy": {
        "system_prompt": "You are an encouraging and patient study buddy. You help students understand concepts, break down complex topics, create study plans, explain difficult material in simple terms, and provide motivation. You use examples, analogies, and step-by-step explanations to make learning easier and more engaging.",
        "description": "Your personal tutor for learning and academic support",
        "emoji": "📖"
    },
    "Fitness Coach": {
        "system_prompt": "You are an enthusiastic and motivating fitness coach. You provide workout advice, create personalized exercise plans, offer nutrition tips, track progress, and encourage healthy habits. You focus on proper form, safety, and sustainable fitness goals. You're supportive and help users stay motivated on their fitness journey.",
        "description": "Your personal trainer for fitness and wellness goals",
        "emoji": "🏋️"
    },
    "Gaming Coach": {
        "system_prompt": "You are an experienced and strategic gaming coach. You provide gameplay tips, strategies, character builds, meta analysis, and help players improve their skills. You're knowledgeable about various games, esports tactics, and competitive play. You offer constructive feedback and help gamers level up their performance.",
        "description": "Your expert guide for gaming strategies and improvement",
        "emoji": "🎮"
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Language configurations
LANGUAGES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Mandarin": "zh-CN",
    "Cantonese": "yue-Hant-HK",  # Cantonese (Traditional Chinese, Hong Kong)
    "Japanese": "ja-JP",
    "Korean": "ko-KR"
}

# Language names for AI prompts
LANGUAGE_NAMES = {
    "English": "English",
    "French": "French",
    "Spanish": "Spanish",
    "Mandarin": "Mandarin Chinese",
    "Cantonese": "Cantonese Chinese",
    "Japanese": "Japanese",
    "Korean": "Korean"
}

# AWS Polly voice configurations by language
# Format: {display_name: (voice_id, engine)}
POLLY_VOICES_BY_LANGUAGE = {
    "English": {
        "Joanna (Female, US)": ("Joanna", "standard"),
        "Matthew (Male, US)": ("Matthew", "standard"),
        "Ivy (Female, US, Child)": ("Ivy", "standard"),
        "Kendra (Female, US)": ("Kendra", "standard"),
        "Kimberly (Female, US)": ("Kimberly", "standard"),
        "Salli (Female, US)": ("Salli", "standard"),
        "Joey (Male, US)": ("Joey", "standard"),
        "Justin (Male, US, Child)": ("Justin", "standard")
    },
    "French": {
        "Chantal (Female, Canadian)": ("Chantal", "standard"),
        "Mathieu (Male)": ("Mathieu", "standard"),
        "Léa (Female)": ("Lea", "standard")
    },
    "Spanish": {
        "Lupe (Female, US)": ("Lupe", "standard"),
        "Miguel (Male, US)": ("Miguel", "standard"),
        "Penélope (Female, US)": ("Penelope", "standard")
    },
    "Mandarin": {
        "Zhiyu (Female, Neural)": ("Zhiyu", "neural")
    },
    "Cantonese": {
        "Hiujin (Female, Neural)": ("Hiujin", "neural")
    },
    "Japanese": {
        "Mizuki (Female, Neural)": ("Mizuki", "neural"),
        "Takumi (Male, Neural)": ("Takumi", "neural"),
        "Kazuha (Female, Neural)": ("Kazuha", "neural"),
        "Tomoko (Female, Neural)": ("Tomoko", "neural")
    },
    "Korean": {
        "Seoyeon (Female, Neural)": ("Seoyeon", "neural"),
        "Sumi (Female, Neural)": ("Sumi", "neural")
    }
}

# Language code mapping for Polly TTS
POLLY_LANGUAGE_CODES = {
    "English": "en-US",
    "French": "fr-CA",
    "Spanish": "es-US",
    "Mandarin": "cmn-CN",
    "Cantonese": "yue-CN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR"
}

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")

    # Personality selector
    st.subheader("Assistant Personality")
    selected_personality = st.selectbox(
        "Choose a personality:",
        options=list(PERSONALITIES.keys()),
        index=0
    )

    st.info(PERSONALITIES[selected_personality]["description"])

    st.markdown("---")
    # Language selector
    st.subheader("Voice Language")
    selected_language = st.selectbox(
        "Choose voice input language:",
        options=list(LANGUAGES.keys()),
        index=0
    )

    st.markdown("---")
    # TTS Voice selector (dynamically shows voices for selected language)
    st.subheader("TTS Voice")
    available_voices = POLLY_VOICES_BY_LANGUAGE.get(selected_language, {})
    selected_voice = st.selectbox(
        "Choose text-to-speech voice:",
        options=list(available_voices.keys()),
        index=0
    )

    st.markdown("---")
    st.subheader("About")
    st.write("This chatbot uses Google's Gemini AI to provide intelligent responses.")
    st.write(f"**Model:** gemini-2.5-flash")
    st.write(f"**Current Personality:** {selected_personality}")
    st.write(f"**Voice Language:** {selected_language}")

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.tts_audio = {}
        st.session_state.processing = False
        st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for voice input
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None

# Initialize session state for TTS
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}
if "processing" not in st.session_state:
    st.session_state.processing = False

# Main chat interface
st.title(f"💬 Chat with {selected_personality} {PERSONALITIES[selected_personality]['emoji']}")

# Display chat history with audio
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Display audio player for assistant messages (outside chat_message)
    if message["role"] == "assistant":
        message_key = f"msg_{idx}"

        # Generate audio if it doesn't exist yet
        if message_key not in st.session_state.tts_audio:
            with st.spinner("🔊 Generating audio..."):
                voice_id, engine = POLLY_VOICES_BY_LANGUAGE[selected_language][selected_voice]
                language_code = POLLY_LANGUAGE_CODES[selected_language]
                audio_bytes = text_to_speech(message["content"], voice_id, language_code, engine)
                if audio_bytes:
                    st.session_state.tts_audio[message_key] = audio_bytes
                else:
                    st.warning("⚠️ TTS temporarily unavailable. Please check your AWS credentials.")

        # Display audio player if audio exists
        if message_key in st.session_state.tts_audio:
            st.audio(st.session_state.tts_audio[message_key], format="audio/mp3")

# Generate AI response if the last message is from the user
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create context with personality and conversation history
                context = PERSONALITIES[selected_personality]["system_prompt"]

                # Add language instruction
                language_instruction = f"\n\nIMPORTANT: You must respond in {LANGUAGE_NAMES[selected_language]} to match the user's language preference."

                # Build conversation history for context
                conversation_history = ""
                for msg in st.session_state.messages[-5:]:  # Last 5 messages for context
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_history += f"{role}: {msg['content']}\n"

                # Generate response with context and language instruction
                full_prompt = f"{context}{language_instruction}\n\nConversation:\n{conversation_history}"
                response = model.generate_content(full_prompt)

                # Display and store response
                ai_response = response.text
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.rerun()

            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                st.rerun()

# Process new audio recording and auto-send
if "pending_audio" in st.session_state and st.session_state.pending_audio:
    audio_bytes = st.session_state.pending_audio
    st.session_state.pending_audio = None

    with st.spinner("🎙️ Transcribing your voice..."):
        # Get the language code for the selected language
        language_code = LANGUAGES[selected_language]
        transcribed = transcribe_audio(audio_bytes, language_code)
        if transcribed and not transcribed.startswith("["):
            # Auto-send the transcribed message
            st.session_state.messages.append({"role": "user", "content": transcribed})
            st.session_state.transcribed_text = ""
            st.session_state.last_audio_bytes = None
            st.rerun()
        else:
            st.error(f"❌ {transcribed}")
            st.session_state.transcribed_text = ""

# Custom CSS to fix input bar at bottom
st.markdown("""
<style>
    /* Center sidebar title */
    [data-testid="stSidebar"] h1 {
        text-align: center;
    }

    /* Make selectbox non-typeable */
    [data-testid="stSidebar"] input[aria-autocomplete="list"] {
        pointer-events: none;
        caret-color: transparent;
    }


    /* Style the form to look integrated */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    /* Make text input column take full width */
    [data-testid="stForm"] [data-testid="column"]:first-child {
        position: relative !important;
        padding-right: 50px !important;
    }

    /* Position send button inside the input field */
    [data-testid="stForm"] [data-testid="column"]:last-child {
        position: absolute !important;
        right: 5px !important;
        top: 0 !important;
        width: 50px !important;
        z-index: 10 !important;
    }

    /* Style the submit button */
    [data-testid="stForm"] button[kind="formSubmit"] {
        background: transparent !important;
        border: none !important;
        padding: 8px !important;
        font-size: 1.3em !important;
        box-shadow: none !important;
        height: 45px !important;
        min-height: 45px !important;
        width: 45px !important;
        border-radius: 50% !important;
    }

    [data-testid="stForm"] button[kind="formSubmit"]:hover {
        background: rgba(0, 0, 0, 0.05) !important;
        border-radius: 50% !important;
    }

    /* Reduce gap between columns */
    [data-testid="column"]:has(.stAudioRecorder) {
        padding-left: 0px !important;
        margin-left: -10px !important;
    }

    /* Style the audio recorder to match send button size */
    .stAudioRecorder {
        height: 45px !important;
        max-height: 45px !important;
        width: 45px !important;
        max-width: 45px !important;
        overflow: hidden !important;
    }

    .stAudioRecorder > div {
        height: 45px !important;
        max-height: 45px !important;
        width: 45px !important;
        max-width: 45px !important;
    }

    .stAudioRecorder button {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        height: 45px !important;
        max-height: 45px !important;
        width: 45px !important;
        max-width: 45px !important;
        font-size: 0 !important;
        line-height: 45px !important;
        border-radius: 50% !important;
    }

    .stAudioRecorder button:hover {
        background: rgba(0, 0, 0, 0.05) !important;
        border-radius: 50% !important;
    }

    /* Completely hide all icons and content */
    .stAudioRecorder button * {
        display: none !important;
        visibility: hidden !important;
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* Show emoji instead */
    .stAudioRecorder button {
        text-align: center !important;
    }

    .stAudioRecorder button::after {
        content: "\1F399\FE0F";
        font-size: 1.3em !important;
        line-height: 45px !important;
        display: block !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 45px !important;
        height: 45px !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom input bar with voice recorder at the bottom
st.markdown("---")
st.markdown("##### 💬 Send a message")

# Create columns for input layout
col_input, col_voice = st.columns([20, 1])

# Text input with integrated send button
with col_input:
    # Use form to allow Enter key submission
    with st.form(key="message_form", clear_on_submit=False):
        col_text, col_btn = st.columns([6, 0.5])

        with col_text:
            # Don't use transcribed_text as value since we auto-send voice messages
            user_input = st.text_input(
                "Message",
                value="",
                placeholder="Type your message or use the microphone...",
                key="message_input",
                label_visibility="collapsed"
            )

        with col_btn:
            send_clicked = st.form_submit_button("✈️", help="Send message")

        if send_clicked and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.rerun()

# Voice recorder button on the right
with col_voice:
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="1x",
        key="voice_recorder"
    )

# Handle new recording
if audio_bytes:
    print(f"Audio bytes received: {len(audio_bytes)} bytes")
    if audio_bytes != st.session_state.last_audio_bytes:
        print("New audio detected, processing...")
        st.session_state.last_audio_bytes = audio_bytes
        st.session_state.pending_audio = audio_bytes
        st.rerun()
    else:
        print("Same audio as before, skipping")
