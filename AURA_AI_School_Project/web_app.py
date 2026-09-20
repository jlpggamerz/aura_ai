from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# =========================
# GROQ AI SETUP
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("AI API: CONNECTED")
else:
    groq_client = None
    print("AI API: NOT CONNECTED")
    print("Please set GROQ_API_KEY first.")


# =========================
# AURA AI
# =========================

def ai_response(message):
    if not groq_client:
        return "AURA AI: Groq API key connected nahi hai. Pehle GROQ_API_KEY set karo."

    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are AURA AI, a friendly personal AI assistant.

Rules:
- Reply naturally like a helpful AI assistant.
- Understand English, Hindi and Hinglish.
- If the user says "hi", "hello", "kya haal hai", etc., reply naturally.
- For Class 9 school questions, explain step-by-step at Class 9 level.
- Keep answers clear and useful.
- Do not pretend to have abilities you don't have.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Error:", e)
        return f"AURA AI Error: {str(e)}"


# =========================
# WEB ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "response": "Message nahi mila."
            }), 400

        message = data["message"].strip()

        if not message:
            return jsonify({
                "response": "Kuch message type ya bolo."
            }), 400

        answer = ai_response(message)

        return jsonify({
            "response": answer
        })

    except Exception as e:
        print("Server Error:", e)

        return jsonify({
            "response": f"Server error: {str(e)}"
        }), 500


@app.route("/api/clear", methods=["POST"])
def clear():
    return jsonify({
        "success": True
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    print("")
    print("======================================")
    print("              AURA AI")
    print("======================================")
    print("AI API:", "CONNECTED" if GROQ_API_KEY else "NOT CONNECTED")
    print("Voice: Browser Speech API")
    print("Server: http://127.0.0.1:5000")
    print("======================================")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )