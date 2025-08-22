from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/gpt-summary", methods=["POST"])
def gpt_summary():
    data = request.json
    hero_a = data.get("heroA")
    hero_b = data.get("heroB")

    if not hero_a or not hero_b:
        return jsonify({"error": "Missing heroA or heroB"}), 400

    prompt = f"""Compare the strengths, weaknesses, and likely battle outcome between {hero_a} and {hero_b}. 
Write two insightful paragraphs based on their known abilities, personalities, and tactics."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return jsonify({"result": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "ClarityEdge GPT API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
