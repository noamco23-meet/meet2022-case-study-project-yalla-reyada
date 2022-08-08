from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyAb9fdK1LcLldQeTw7xaa0ojviPRX4aYXk",
  "authDomain": "mini-project-summer-y2.firebaseapp.com",
  "projectId": "mini-project-summer-y2",
  "storageBucket": "mini-project-summer-y2.appspot.com",
  "messagingSenderId": "859721328860",
  "appId": "1:859721328860:web:fa77f49eaa61ce367bec19",
  "measurementId": "G-71QX0TPLJE",
  "databaseURL":"https://mini-project-summer-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return render_template("index.html")
       except:
           error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error  =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        class_of = request.form['class']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email": email, "password": password, "full_name": full_name, "username": username, "class_of": class_of}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return render_template("index.html")
        except:
           error = "Authentication failed"
           print(error)
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error  =""
    if request.method == 'POST':
        year = request.form['year']
        journey = request.form['journey']
        project = request.form['project']
        today = datetime.now()
        today = today.strftime("%d/%m/%Y %H:%M:%S")
        try:
            tweet = {"year": year, "journey": journey, 'project': project, 'time': today}
            db.child("Tweet").push(tweet)
            return redirect(url_for('all_tweet'))
        except:
           error = "Authentication failed"
           print(error)
    return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweet():
    all_tweets2 = db.child("Tweet").get().val().values()
    return render_template("all_tweets.html", all_tweets2 = all_tweets2)


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return render_template("signin.html")
if __name__ == '__main__':
    app.run(debug=True)