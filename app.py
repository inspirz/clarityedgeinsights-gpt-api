import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from openai import APIError

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up OpenAI client using env variable
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route('/analyze-battle', methods=['POST'])
def analyze_battle():
    data = request.get_json()
    hero1 = data.get("hero1")
    hero2 = data.get("hero2")

    if not hero1 or not hero2:
        return jsonify({"error": "Both hero1 and hero2 are required"}), 400

    try:
        response = client.chat.completions.create(
            # Using the environment variable for the model name is a good practice.
            model=os.getenv("MODEL_NAME", "gpt-4o"),
            messages=[
                {"role": "system", "content": "You are a Marvel expert AI."},
                {"role": "user", "content": f"Analyze a one-on-one fight between {hero1} and {hero2}. Compare their abilities and give a 2-paragraph summary of who would win and why."}
            ],
            # This parameter was changed back to `max_completion_tokens`
            # as per the error message.
            max_completion_tokens=500
        )

        # Added logging to inspect the full API response in the Render logs.
        print(f"OpenAI API Response: {response}")

        # Validate that the response contains a valid choice before trying to access it.
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            result = response.choices[0].message.content
            return jsonify({"analysis": result})
        else:
            # If the response is empty or unexpected, return a clear error.
            return jsonify({"error": "OpenAI API returned an empty or invalid response."}), 500

    except APIError as e:
        # This block will catch specific errors from the OpenAI API,
        # such as an invalid API key or a rate limit error.
        print(f"OpenAI APIError: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # This block will catch any other unexpected errors.
        print(f"Unexpected Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/healthz", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
