from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='')

# Serve the index.html
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# API for AI Chat
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400

    try:
        reply = get_ai_response(user_message)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_ai_response(message):
    api_key = os.getenv('OPENAI_API_KEY')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
