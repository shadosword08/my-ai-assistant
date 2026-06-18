from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

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
    conversation_history.append({'role': 'user', 'content': user_message})
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': 'You are a highly capable AI assistant.'},
            *conversation_history
        ]
    )
    ai_reply = response.choices[0].message.content
    conversation_history.append({'role': 'assistant', 'content': ai_reply})
    return jsonify({'response': ai_reply})

@app.route('/reset', methods=['POST'])
def reset():
    conversation_history.clear()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True)
