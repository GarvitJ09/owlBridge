from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_socketio import SocketIO, emit
from modules.text_conversion import translate_text, getLangName, all_languages
from modules.text_to_voice import generate_audio_file
from langdetect import detect
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@socketio.on('translate_chunk')
def handle_translation(data):
    try:
        text = data['text']
        to_lang = data['to_lang']

        if not text or not to_lang:
            emit('translation_error', {"error": "Missing text or 'to_lang' in request"})
            return

        from_lang = detect(text)
        from_lang_name = getLangName(from_lang)

        to_lang = to_lang.lower()
        if to_lang not in all_languages:
            emit('translation_error', {"error": "Unsupported target language"})
            return

        to_lang_code = all_languages[all_languages.index(to_lang) + 1]

        translated_text = translate_text(text, to_lang_code)

        # Generate audio file
        audio_io = generate_audio_file(translated_text, to_lang_code)
        audio_data = base64.b64encode(audio_io.getvalue()).decode('utf-8')

        emit('translation_response', {
            'translated_text': translated_text,
            'audio_data': audio_data
        })

    except Exception as e:
        emit('translation_error', {"error": str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)