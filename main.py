

from flask import Flask, render_template, request
import datetime
import random
import requests
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

def get_random_quote():
    quotes = [
        "Believe you can and you're halfway there.",
        "The only way to do great work is to love what you do.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Don't watch the clock; do what it does. Keep going.",
        "You miss 100% of the shots you don't take.",
        "If you're going through hell, keep going.",
         "Keep your eyes on the stars, and your feet on the ground.",
         "You are never too old to set another goal or to dream a new dream.",
         "The future belongs to those who believe in the beauty of their dreams.",
         "Happiness can be found even in the darkest of times if one only remembers to turn on the light.",
         "Do something today that your future self will thank you for.",
         "You don't have to be great to start, but you have to start to be great." ,
         "The best way to predict your future is to create it.",
         "You are stronger than you seem, braver than you believe, and smarter than you think." ,
         "The only limit to our realization of tomorrow will be our doubts of today."     
    ]
    return random.choice(quotes)

@app.route('/submit', methods=['POST'])
def handle_submit():
    name = request.form['name']
    email = request.form['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return f'Thank you, {name}! Your email is {email}.'

@app.route('/data')
def display_data():
    users = User.query.all()
    return render_template('data.html', users=users)

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return render_template("index.html", message="Data submitted successfully!")
    else:
        api_key = '30b267d8ac0094a6e6b59c58f19626eb'
        city = 'hyderabad'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = str(round(weather_data['main']['temp'] - 273.15))
            humidity = weather_data["main"]["humidity"]
            weather_description = weather_data["weather"][0]["description"]
        else:
            temperature = "N/A"
            humidity = "N/A"
            weather_description = "Failed to retrieve weather data"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        random_quote = get_random_quote()
        users = User.query.all()
        return render_template('homepage.html', current_time=current_time, quote=random_quote, temperature=temperature, humidity=humidity, weather_description=weather_description, city=city, users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



    
    
    
    