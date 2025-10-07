from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "my_simple_secret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        heart_rate = float(request.form['heart_rate'])
        bp = float(request.form['bp'])
        steps = float(request.form['steps'])
        calories = float(request.form['calories'])

        # Simple rule-based logic
        score = 0
        if temperature > 35 or humidity > 80: score += 1
        if heart_rate > 100 or bp > 140: score += 1
        if steps < 2000 or calories > 2500: score += 1