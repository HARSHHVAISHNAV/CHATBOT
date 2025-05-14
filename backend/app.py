from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv() 
app = Flask(__name__)
CORS(app) 

api_key = os.getenv("GROQ_API_KEY") 

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant named Invisio for helping in developers in code generation."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    # 🧪 DEBUG PRINT
    print("Groq response:", response.status_code, response.text)

    try:
        groq_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": groq_reply})
    except KeyError:
        return jsonify({"error": "Groq API error", "details": response.json()}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
