from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.0-flash"

# Initialize Flask app
app = Flask(__name__)

# Gemini response generation function
def generate_gemini_response(user_message):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_message)
        return response.text.strip() if response and response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Home route (serves frontend HTML page)
@app.route("/")
def home():
    return render_template("chatbot.html")  

# API endpoint for receiving user messages and returning chatbot replies
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a valid message."})

        gemini_response = generate_gemini_response(user_message)
        return jsonify({"reply": gemini_response})

    except Exception as e:
        return jsonify({"reply": f"Internal server error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
