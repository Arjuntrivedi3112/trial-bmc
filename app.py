from flask import Flask, jsonify, request, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='')

# Serve the index.html
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# AI Chat API
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
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': message}]
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)

    if response.status_code != 200:
        raise Exception('Failed to fetch response from OpenAI API')

    response_data = response.json()
    return response_data['choices'][0]['message']['content']

# Fallback for any other routes
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('', path)

if __name__ == '__main__':
    app.run(debug=True)
