import os

from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# ============================================================
# GROQ
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = None

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    print("WARNING: GROQ_API_KEY is not configured.")


# ============================================================
# AURA AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are AURA AI, the AI assistant of AURA Group.

PERSONALITY:
- Friendly
- Natural
- Helpful
- Conversational
- Smart
- Concise when speaking

LANGUAGE RULE:

If the user asks in English:
Reply in English.

If the user asks in Hindi:
Reply in Hindi.

If the user asks in Hinglish:
Reply in natural Hinglish.

If the user mixes Hindi and English:
Reply naturally using the same mixed style.

Do not unnecessarily translate the user's language.

JLPG INFORMATION:

JLPG is the owner and founder of AURA Group.

JLPG is involved in:
- Technology
- AI development
- Gaming
- Esports
- Digital projects

JLPGGaming is associated with JLPG's gaming and esports activities.

If someone asks:
"Who is JLPG?"
"JLPG kaun hai?"
"Who owns AURA Group?"
"JLPG kya karta hai?"
or similar questions:

Answer naturally using the information above.

Do not invent private information about JLPG.

VOICE RULE:

Your answer will be spoken by a browser voice.

Keep normal answers concise and natural.

Do not use unnecessary markdown, tables, or complicated formatting
unless the user specifically asks for them.
"""


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# CHAT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True) or {}

        message = str(
            data.get("message", "")
        ).strip()

        if not message:

            return jsonify({
                "reply": "Please say something."
            })


        if not client:

            return jsonify({
                "reply": "AURA AI is not configured. Please add the GROQ_API_KEY in Render."
            }), 500


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": message
                }

            ],

            temperature=0.7,

            max_tokens=500

        )


        reply = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        return jsonify({
            "reply": reply
        })


    except Exception as e:

        print(
            "GROQ ERROR:",
            repr(e)
        )

        return jsonify({
            "reply": "Sorry, something went wrong."
        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "name": "AURA AI",
        "ai": "Groq"
    })


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
