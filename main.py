from flask import Flask, render_template, url_for

app = Flask(__name__)

#mongodb+srv://coba:<coba123>@fik-3aig6.mongodb.net/test?retryWrites=true&w=majority
# AIzaSyAfX9o359mJJTmagp_lotw5m0ISHdkHXc0 -- YOUTUBE


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/dashboard')
def dashboard():
  return render_template("dashboard.html")

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/forgot_pwd')
def forgot_pwd():
  return render_template("forgot-password.html")