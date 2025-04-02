from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
OPENAI_API_KEY = "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"

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    data = request.json
    match_data = data.get("match_data", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            api_key=OPENAI_API_KEY,
            messages=[
                {"role": "system", "content": "You are a professional sports journalist writing engaging summaries of NBA games in English."},
                {"role": "user", "content": f"Write a professional, engaging, and detailed NBA game summary based on the following statistics:\n{match_data}"}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return jsonify({"summary": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
