from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "✅ ClarityEdge GPT API is live."

@app.route("/healthz", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/analyze-battle", methods=["POST"])
def analyze_battle():
    data = request.get_json()
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if not hero1 or not hero2:
        return jsonify({"error": "Both hero1 and hero2 are required"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a Marvel power-scaling expert."},
                {"role": "user", "content": f"Who would win in a fight between {hero1} and {hero2}? Give a 2-paragraph summary comparing powers, weaknesses, and why one would win."}
            ]
        )
        result = response.choices[0].message.content.strip()
        return jsonify({"analysis": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# REQUIRED FOR RENDER DEPLOYMENT
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets this
    app.run(host='0.0.0.0', port=port)
