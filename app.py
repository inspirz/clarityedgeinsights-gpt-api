import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up OpenAI client with new SDK (>=1.0.0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    # Get JSON data from the request
    data = request.get_json()
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    # Validate input
    if not hero1 or not hero2:
        return jsonify({"error": "Both hero1 and hero2 are required"}), 400

    # Construct prompt
    prompt = f"Who would win in a battle between {hero1} and {hero2}? Provide a detailed explanation based on their comic book abilities and history."

    try:
        # Call OpenAI API with the new completions endpoint
        response = client.chat.completions.create(
            model="gpt-4",  # Ensure you have access to gpt-4
            messages=[
                {"role": "system", "content": "You are a comic book expert with deep knowledge of superhero abilities and lore."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        # Extract the response content
        result = response.choices[0].message.content.strip()
        return jsonify({"analysis": result}), 200

    except Exception as e:
        # Improved error handling with specific HTTP status
        return jsonify({"error": f"Failed to analyze battle: {str(e)}"}), 500

# Required for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Removed trailing colon and added debug=False for production

