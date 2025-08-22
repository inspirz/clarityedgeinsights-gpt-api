from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    data = request.get_json()
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if not hero1 or not hero2:
        return jsonify({"error": "Both hero1 and hero2 are required"}), 400

    prompt = f"""You are a Marvel expert AI. Analyze a one-on-one fight between {hero1} and {hero2}. 
Compare their abilities and give a 2-paragraph summary of who would win and why."""

    try:
        response = openai.ChatCompletion.create(
            model=os.getenv("MODEL_NAME", "gpt-5"),  # Default to gpt-5 if env var not set
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        result = response.choices[0].message.content.strip()
        return jsonify({"analysis": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/healthz", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run()
