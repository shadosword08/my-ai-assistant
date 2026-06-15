# app.py — Your AI Assistant Server
from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
import os

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# Store conversation history
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Add user message to history
    conversation_history.append({
        'role': 'user',
        'content': user_message
    })

    # Call Claude API
    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=1024,
        system='You are a highly capable AI assistant. Help with any task.',
        messages=conversation_history
    )

    ai_reply = response.content[0].text

    # Save AI reply to history
    conversation_history.append({
        'role': 'assistant',
        'content': ai_reply
    })

    return jsonify({'response': ai_reply})

@app.route('/reset', methods=['POST'])
def reset():
    conversation_history.clear()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True)
