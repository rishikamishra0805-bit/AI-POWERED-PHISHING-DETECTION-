from flask import Flask, render_template, request
import joblib
from feature_extraction import extract_features

app = Flask(__name__)

# Saved model load
model = joblib.load("model/phishing_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        url = request.form["url"]

        features = extract_features(url)

        prediction = model.predict([features])

        # Suspicious keyword check
        suspicious_words = [
            "login",
            "verify",
            "update",
            "secure",
            "account",
            "password",
            "bank",
            "confirm"
        ]

        suspicious = any(word in url.lower() for word in suspicious_words)

        if suspicious:
            result = "⚠️ Phishing Website"

        elif prediction[0] == -1:
            result = "⚠️ Phishing Website"

        else:
            result = "✅ Safe Website"


    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)