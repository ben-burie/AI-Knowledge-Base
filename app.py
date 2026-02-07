from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from llm import query_llm

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('user-interface', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('user-interface', path)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/question', methods=['POST'])
def ask_question():
    data = request.get_json()
    user_prompt = data.get('question', '')
    print(f"Received question: {user_prompt}")

    response = query_llm(user_prompt)
    print(f"LLM response: {response}")

    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)