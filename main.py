from flask import Flask, render_template, url_for

app = Flask(__name__)

#mongodb+srv://coba:<coba123>@fik-3aig6.mongodb.net/test?retryWrites=true&w=majority
# AIzaSyAfX9o359mJJTmagp_lotw5m0ISHdkHXc0 -- YOUTUBE


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/dashboard')
def dashboard():
  return render_template("dashboard/dashboard.html")

@app.route('/login')
def login():
  return render_template("auth/login.html")

@app.route('/forgot_pwd')
def forgot_pwd():
  return render_template("auth/forgot-password.html")

@app.route('/404')
def not_found():
  return render_template("dashboard/404.html")

@app.route('/blank')
def blank():
  return render_template("dashboard/blank.html")

@app.route('/buttons')
def buttons():
  return render_template("dashboard/buttons.html")

@app.route('/cards')
def cards():
  return render_template("dashboard/cards.html")

@app.route('/charts')
def charts():
  return render_template("dashboard/charts.html")

@app.route('/tables')
def tables():
  return render_template("dashboard/tables.html")

@app.route('/utilities_a')
def utilities_a():
  return render_template("dashboard/utilities-animation.html")

@app.route('/utilities_b')
def utilities_b():
  return render_template("dashboard/utilities-border.html")

@app.route('/utilities_c')
def utilities_c():
  return render_template("dashboard/utilities-color.html")

@app.route('/utilities_o')
def utilities_o():
  return render_template("dashboard/utilities-other.html")