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

@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html')


@app.route('/select_signup', methods=['GET', 'POST'])
def select_signup():
    return render_template('select_signup.html')

@app.route('/signup_trainer', methods=['GET', 'POST'])
def signup_trainer():
    error  =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phonenumber = request.form['phonenumber']
        sex = request.form['sex']
        city = request.form['city']
        specialty_in_training = request.form['specialty_in_training']
        specialty_in_nutrition = request.form['specialty_in_nutrition']
        expertise = request.form['expertise']
        experience = request.form['experience']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password": password, "full_name": full_name, "phonenumber": phonenumber,
             "sex": sex, "city": city, "specialty_in_training": specialty_in_training, "specialty_in_nutrition": specialty_in_nutrition,
             "expertise": expertise, "experience": experience}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('for_you_trainer'))
        except:
           error = "Authentication failed"
           print(error)
    return render_template('signup_trainer.html')

@app.route('/signup_trainee', methods=['GET', 'POST'])
def signup_trainee():
        error  =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phonenumber = request.form['phonenumber']
        sex = request.form['sex']
        city = request.form['city']
        target = request.form['target']
        training_type = request.form['training_type']
        nutrition_type = request.form['nutrition_type']
        nutrition_problems = request.form['nutrition_problems']
        experience = request.form['experience']


        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password": password, "full_name": full_name, "phonenumber": phonenumber,
             "sex": sex, "city": city, "target": target, "training_type": training_type,
             "nutrition_type": nutrition_type, "nutrition_problems": nutrition_problems, "experience": experience}
            db.child("Users").child(login_session['user']['localId']).set(user)
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
    login_session['user'] = auth.create_user_with_email_and_password(email, password)
    return render_template('for_you_trainee.html')


if __name__ == '__main__':
    app.run(debug=True)1