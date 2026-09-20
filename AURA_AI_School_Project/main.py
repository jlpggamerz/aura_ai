import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(**name**)

# ============================================================

# AURA AI CONFIGURATION

# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
print("WARNING: GEMINI_API_KEY is not configured.")

if API_KEY:
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
You are AURA AI, the voice AI assistant of AURA Group.

PERSONALITY:

* Friendly
* Helpful
* Natural
* Concise
* Conversational
* Do not sound robotic

LANGUAGE RULE:
Always respond in the same language style as the user.

If the user speaks English:
Reply in English.

If the user speaks Hindi:
Reply in Hindi.

If the user speaks Hinglish:
Reply in natural Hinglish.

If the user mixes Hindi and English:
You can naturally mix Hindi and English.

Do not unnecessarily translate the user's language.

JLPG INFORMATION:

JLPG is the owner and founder of AURA Group.

JLPG is involved in:

* Technology
* AI development
* Gaming
* Esports
* Digital projects

JLPGGaming is associated with JLPG's gaming and esports activities.

If the user asks:
"Who is JLPG?"
"JLPG kaun hai?"
"Who owns AURA Group?"
"JLPG kya karta hai?"
or similar questions, answer naturally using only the information above.

Do not invent private information about JLPG.

VOICE RULE:
Your response will be spoken aloud by the browser.
Keep normal answers reasonably concise unless the user asks for detail.

Do not use unnecessary markdown in normal conversational answers.
"""

# ============================================================

# GEMINI MODEL

# ============================================================

model = None

if API_KEY:
try:
model = genai.GenerativeModel(
"gemini-2.0-flash",
system_instruction=SYSTEM_PROMPT
)
except Exception as e:
print("MODEL ERROR:", e)

# ============================================================

# HOME PAGE

# ============================================================

@app.route("/")
def index():
return render_template("index.html")

# ============================================================

# AI CHAT API

# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

```
try:

    data = request.get_json(silent=True) or {}

    message = str(
        data.get("message", "")
    ).strip()

    if not message:
        return jsonify({
            "reply": "Please say something."
        })

    if not model:

        return jsonify({
            "reply": "AURA AI is not configured yet. Please add the GEMINI_API_KEY environment variable."
        }), 500

    response = model.generate_content(message)

    reply = ""

    if response and response.text:
        reply = response.text.strip()

    if not reply:
        reply = "Sorry, I couldn't generate a response."

    return jsonify({
        "reply": reply
    })

except Exception as e:

    print("CHAT ERROR:", repr(e))

    return jsonify({
        "reply": "Sorry, something went wrong while processing your request."
    }), 500
```

# ============================================================

# HEALTH CHECK

# ============================================================

@app.route("/health")
def health():

```
return jsonify({
    "status": "online",
    "name": "AURA AI"
})
```

# ============================================================

# RUN LOCALLY

# ============================================================

if **name** == "**main**":

```
port = int(
    os.environ.get("PORT", 5000)
)

app.run(
    host="0.0.0.0",
    port=port,
    debug=False
)
```
