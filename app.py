from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDZAmDLLK4glPeEyzyX1B1HkW65RoidRHo",
  "authDomain": "case-study-yalla-reyada.firebaseapp.com",
  "projectId": "case-study-yalla-reyada",
  "storageBucket": "case-study-yalla-reyada.appspot.com",
  "messagingSenderId": "395694763700",
  "appId": "1:395694763700:web:5219bacf7b4b0fe5adf1e1",
  "measurementId": "G-J6PGT8PB2D",
  "databaseURL":"https://case-study-yalla-reyada-default-rtdb.europe-west1.firebasedatabase.app"}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def start():
    return render_template('index.html')
@app.route('/select_signup')
def select_signup():
    return render_template('select_signup.html')
@app.route('/signup_trainer')
def signup_trainer():
    return render_template('signup_trainer.html')
@app.route('/signup_trainee')
def signup_trainee():
    return render_template('signup_trainee.html')
@app.route('/for_you_trainer')
def for_you_trainer():
    return render_template('for_you_trainer.html')
@app.route('/for_you_trainee')
def for_you_trainee():
    return render_template('for_you_trainee.html')


if __name__ == '__main__':
    app.run(debug=True)