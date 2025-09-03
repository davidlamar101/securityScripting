from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    # Fetch advice
    response = requests.get("https://api.adviceslip.com/advice")
    advice_text = "Could not fetch advice"
    if response.status_code == 200:
        data = response.json()
        advice_text = data['slip']['advice']
    
    # Combine greeting and advice
    return f"Hello to my Python App for Security Scripting!<br>Advice: {advice_text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
