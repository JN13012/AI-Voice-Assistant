import base64
import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from worker import speech_to_text, text_to_speech, openai_process_message

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")
    audio_binary = request.data
    text = speech_to_text(audio_binary)
    return jsonify({'text': text})

@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    user_message = request.json['userMessage']
    voice = request.json['voice']
    
    openai_response_text = openai_process_message(user_message)
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])
    openai_response_speech = text_to_speech(openai_response_text, voice)
    openai_response_speech_b64 = base64.b64encode(openai_response_speech).decode('utf-8')

    return jsonify({
        "openaiResponseText": openai_response_text, 
        "openaiResponseSpeech": openai_response_speech_b64
    })

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')