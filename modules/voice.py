from gtts import gTTS
import base64
import io
import os
from groq import Groq

def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_bytes = audio_buffer.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        return audio_b64
    except Exception:
        return None

def speech_to_text(audio_bytes):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3",
            language="en"
        )
        return transcription.text
    except Exception as e:
        return f"ERROR: {str(e)}"