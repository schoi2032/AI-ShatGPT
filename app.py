from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Send input to GPT model
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # You can change model
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    bot_reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
