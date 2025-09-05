from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Use environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# Initialize the OpenAI client (new syntax for v1.x)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    data = request.json
    hero1 = data.get('hero1')
    hero2 = data.get('hero2')

    if not hero1 or not hero2:
        return jsonify({'error': 'Missing hero names'}), 400

    prompt = (
        f"Imagine a battle between {hero1} and {hero2}. "
        "Analyze their powers, strategies, and personalities to decide who would win and why. "
        "Explain in two paragraphs, with reasoning, not just power levels."
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a superhero analyst that gives detailed battle breakdowns."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        analysis = response.choices[0].message.content
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "ClarityEdge GPT Battle API is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
