from gtts import gTTS
from io import BytesIO

def generate_audio_file(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    audio_io = BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return audio_io