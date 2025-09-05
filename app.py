import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all domains, allowing cross-origin requests
CORS(app)

# Retrieve the OpenAI API key and API endpoint URL from environment variables
# Note: It's crucial to set these as environment variables in your Render dashboard
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")

# Function to get a response from the LLM model
def _get_llm_response(conversation_history):
    """
    Sends a request to the LLM model and returns the generated content.
    This function has been updated to use the correct 'max_completion_tokens' parameter.
    """
    if not ENDPOINT_URL or not OPENAI_API_KEY:
        # Return an error if API credentials are not set
        return "API credentials are not set."

    json_payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ] + conversation_history,
        # THIS IS THE CORRECTED LINE:
        # The API requires 'max_completion_tokens' for this model, not 'max_tokens'
        "max_completion_tokens": 150
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    try:
        response = requests.post(ENDPOINT_URL, headers=headers, data=json.dumps(json_payload))
        response.raise_for_status() # Raises an HTTPError for bad responses
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as errh:
        return f"Http Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Something went wrong: {err}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/generate', methods=['POST'])
def generate_text():
    """
    Handles the POST request to generate text.
    It takes a conversation history from the request body and uses it to
    get a response from the LLM model.
    """
    try:
        data = request.json
        conversation_history = data.get('conversationHistory')
        if not conversation_history:
            return jsonify({"error": "No conversation history provided"}), 400

        llm_response = _get_llm_response(conversation_history)
        return jsonify({"response": llm_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    A simple health check endpoint.
    """
    return "OK", 200

# Main entry point for the application, used for local development
if __name__ == '__main__':
    # When deploying to Render, this block might be skipped in favor of a
    # production WSGI server like Gunicorn.
    app.run(debug=True, port=int(os.environ.get("PORT", 1000)))
