from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Read environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# Initialize OpenAI client correctly (>=1.0.0)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return "GPT Battle API is live."

@app.route("/analyze-battle", methods=["POST"])
def analyze_battle():
    try:
        data = request.get_json()
        hero1 = data.get("hero1", "").strip()
        hero2 = data.get("hero2", "").strip()

        if not hero1 or not hero2:
            return jsonify({"error": "Both 'hero1' and 'hero2' are required"}), 400

        prompt = (
            f"Imagine a battle between {hero1} and {hero2}. "
            f"Analyze their powers, tactics, weaknesses, and personalities. "
            f"Who wins and why? Give a two-paragraph breakdown."
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a superhero analyst who gives detailed battle outcomes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Safely extract analysis
        analysis = response.choices[0].message.content.strip() if response.choices else "No analysis returned."

        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

