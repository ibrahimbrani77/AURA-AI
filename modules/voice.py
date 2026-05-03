from gtts import gTTS
import base64
import io

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