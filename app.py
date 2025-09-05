from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Use your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return 'ClarityEdge GPT API is running!'

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    data = request.get_json()

    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if not hero1 or not hero2:
        return jsonify({"error": "Missing hero names"}), 400

    try:
        # GPT-4 Turbo call without unsupported parameters
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You're a battle analyst. Given two characters, analyze who would win and why."
                },
                {
                    "role": "user",
                    "content": f"Who would win in a battle between {hero1} and {hero2}? Provide a detailed breakdown of their abilities, weaknesses, and tactics."
                }
            ]
        )

        # Extract and safely strip the result
        content = response.choices[0].message.content
        result = content.strip() if content else "No analysis was generated."

        return jsonify({"analysis": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

