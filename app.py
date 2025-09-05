import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    data = request.get_json()
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if not hero1 or not hero2:
        return jsonify({"error": "Both hero1 and hero2 are required"}), 400

    prompt = f"Who would win in a battle between {hero1} and {hero2}? Provide a detailed explanation based on comic book lore."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a comic book expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        return jsonify({"analysis": result}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to analyze battle: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
