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
  "databaseURL":"https://case-study-yalla-reyada-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

SEX = ['Male', 'Female']
TRAINING_TYPES = ['Bodybuilding', 'Fitness', 'Yoga', 'Job Training', 'Other']

def find_opposite_user(user_type):
    if user_type == "Trainers":     
        return "Trainees"
    return "Trainers"


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')


@app.route('/all_trainers')
def select_signup():
    return render_template('all_trainers.html', users = db.child("Users").child("Trainers").get().val())

@app.route('/signup_trainer', methods=['GET', 'POST'])
def signup_trainer():

    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']
        phone_number = request.form['phone_number']
        sex = request.form.get('sex')
        city = request.form['city']
        country = request.form['country'] 
        training_type = request.form.get('training_type')
        expertise_training = request.form['expertise_training']
        expertise_nutrition = request.form['expertise_nutrition']
        experience = request.form['experience']
    

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            login_session['user']['type'] = "Trainers"
            user = {
                "email": email, "age":age, "password": password, "name": name, "phone_number":phone_number,
                "sex": sex, "city": city, "country": country, "training_type": training_type,
                "expertise_training": expertise_training, "expertise_nutrition": expertise_nutrition, "experience":experience
                }
            db.child("Users").child("Trainers").child(login_session['user']['localId']).set(user)
            return redirect(url_for('foryou'))
        except:
            error = "Authentication failed"
            print(error)
    return render_template('signup_trainer.html', SEX=SEX, TRAINING_TYPES=TRAINING_TYPES)

@app.route('/signup_trainee', methods=['GET', 'POST'])
def signup_trainee():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        sex = request.form.get('sex')
        city = request.form['city']
        country = request.form['country']
        training_type = request.form.get('training_type')
        experience = request.form['experience']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            login_session['user']['type'] = "Trainees"
            user = {
                "email": email, "password": password, "name": name, "age":age, "phone_number": phone_number,
                "sex": sex, "city": city, "country":country, "training_type": training_type,
                "experience": experience
                }

            db.child("Users").child("Trainees").child(login_session['user']['localId']).set(user)
            return redirect(url_for('foryou'))
        except:
           error = "Authentication failed"
           print(error)
    return render_template('signup_trainee.html', SEX=SEX, TRAINING_TYPES=TRAINING_TYPES)
    
@app.route('/foryou', methods=['GET', 'POST'])
def foryou():
    user_type = login_session['user']['type']
    print(user_type)
    training_type = db.child("Users").child(user_type).child(login_session['user']['localId']).get().val()['training_type']
    suggested_users = db.child("Users").child(find_opposite_user(user_type)).get().val()
    print(suggested_users)
    return render_template("foryou.html", user_type=user_type, training_type=training_type, suggested_users=suggested_users, username = db.child("Users").child(user_type).get().val()['name'])

if __name__ == '__main__':
    app.run(debug=True)