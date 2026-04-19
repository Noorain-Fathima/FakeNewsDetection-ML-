from flask import Flask, render_template, request
from model import model, vectorizer, stemming

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    news = request.form.get('news')

    if not news:
        return render_template('index.html', prediction_text="Please enter news text.")

    news_processed = stemming(news)

    vector = vectorizer.transform([news_processed])

    prediction = model.predict(vector)

    if prediction[0] == 1:
        result = "🔴 This news is likely FAKE"
    else:
        result = "🟢 This news is likely REAL"

    return render_template('index.html', prediction_text=result)

if __name__ == "__main__":
    app.run(debug=True)