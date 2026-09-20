import os

from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing")
    client = None
else:
    client = Groq(api_key=GROQ_API_KEY)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"reply": "Please type or say something."})

        if client is None:
            return jsonify({
                "reply": "Groq API key is not configured on the server."
            }), 500

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are AURA AI, an intelligent and friendly AI assistant created for AURA Group.

Reply in the same language/style as the user:
English -> English
Hindi -> Hindi
Hinglish -> Hinglish

Keep normal answers natural and conversational.

JLPG is the owner and founder of AURA Group and is involved in technology, AI, gaming, esports and digital projects.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        print("GROQ ERROR:", repr(e))

        return jsonify({
            "reply": "Groq se response lene mein problem aa rahi hai."
        }), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "ai": "Groq"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
