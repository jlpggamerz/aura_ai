import os

from flask import Flask, render_template, request, jsonify
from groq import Groq


# ==========================================
# AURA AI
# Flask + Groq Backend
# ==========================================

app = Flask(__name__)


# ==========================================
# GROQ CONFIGURATION
# ==========================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = None

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
    print("AURA AI: Groq API key loaded successfully.")
else:
    print("AURA AI ERROR: GROQ_API_KEY is missing.")


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are AURA AI, the AI assistant of AURA Group.

Your personality:
- Friendly
- Natural
- Helpful
- Smart
- Conversational
- Clear
- Concise when speaking

LANGUAGE RULES:

If the user speaks English:
Reply in English.

If the user speaks Hindi:
Reply in Hindi.

If the user speaks Hinglish:
Reply naturally in Hinglish.

If the user mixes Hindi and English:
Reply naturally using the same mixed style.

Do not unnecessarily translate the user's language.

VOICE RULE:

Your answers may be spoken aloud by a browser voice.

Keep normal answers natural and reasonably concise.

Do not use unnecessary markdown, tables, or complicated formatting
unless the user specifically asks for them.


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
"Who founded AURA Group?"
or similar questions,

answer naturally using the information above.

Do not invent private or personal information about JLPG.

If you don't know something, say that you don't have that information.


GENERAL RULE:

Answer the user's actual question.

Do not claim to have abilities that you don't have.

Do not pretend to have accessed something if you haven't.

Be helpful and honest.
"""


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# CHAT API
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        # --------------------------------------
        # Read JSON
        # --------------------------------------

        data = request.get_json(silent=True) or {}

        message = str(
            data.get("message", "")
        ).strip()


        # --------------------------------------
        # Empty message
        # --------------------------------------

        if not message:

            return jsonify({
                "reply": "Please type or say something."
            })


        # --------------------------------------
        # Check Groq
        # --------------------------------------

        if client is None:

            return jsonify({
                "reply": "Groq API is not configured. Please add GROQ_API_KEY in Render Environment Variables."
            }), 500


        # --------------------------------------
        # Groq Request
        # --------------------------------------

        response = client.chat.completions.create(

            # Current Groq production model
            model="openai/gpt-oss-120b",

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


        # --------------------------------------
        # Get AI response
        # --------------------------------------

        reply = response.choices[0].message.content


        if not reply:

            reply = "Sorry, I couldn't generate a response."


        reply = reply.strip()


        # --------------------------------------
        # Return response
        # --------------------------------------

        return jsonify({
            "reply": reply
        })


    # ==========================================
    # ERROR HANDLING
    # ==========================================

    except Exception as e:

        print(
            "GROQ ERROR:",
            repr(e)
        )

        return jsonify({
            "reply": "Sorry, Groq se response lene mein problem aa rahi hai."
        }), 500


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "name": "AURA AI",
        "ai": "Groq",
        "model": "openai/gpt-oss-120b"
    })


# ==========================================
# START SERVER
# ==========================================

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
