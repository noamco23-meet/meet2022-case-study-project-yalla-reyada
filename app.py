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

@app.route('/index', methods=['GET', 'POST'])
def start():
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')



@app.route('/select_signup', methods=['GET', 'POST'])
def select_signup():
    return render_template('select_signup.html')

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
            login_session['user']['type'] = "Trainer"
            user = {
                "email": email, "age":age, "password": password, "name": name, "phone_number": phone_number,
                "sex": sex, "city": city, "country":country, "training_type": training_type,
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
        phone_number = request.form['phone_number']
        sex = request.form['sex']
        city = request.form['city']
        target = request.form['target']
        training_type = request.form['training_type']
        experience = request.form['experience']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            login_session['user']['type'] = "Trainee"
            user = {
                "email": email, "password": password, "name": name, "phone_number": phone_number,
                "sex": sex, "city": city, "target": target, "training_type": training_type,
                "experience": experience
                }

            db.child("Users").child("Trainees").child(login_session['user']['localId']).set(user)
            return redirect(url_for('for_you_trainee'))
        except:
           error = "Authentication failed"
           print(error)
    return render_template('signup_trainee.html')
    
@app.route('/for_you_trainer', methods=['GET', 'POST'])
def for_you_trainer():
    return render_template("for_you_trainer.html")
    
@app.route('/for_you_trainee', methods=['GET', 'POST'])
def for_you_trainee():
    return render_template('for_you_trainee.html')


@app.route('/foryou', methods=['GET', 'POST'])
def foryou():
    return render_template("foryou.html", user_type = login_session['user']['type'], training_type = db.child(login_session['user']['type']).child(login_session['user']['localId']).get().val()['training_type'])

if __name__ == '__main__':
    app.run(debug=True)