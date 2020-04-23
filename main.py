from pymongo import MongoClient
from flask import Flask, render_template, url_for, session, request, redirect

app = Flask(__name__)
app.secret_key = "rahasia"

client = MongoClient("mongodb+srv://ikal:123@forusers-3aig6.mongodb.net/test?retryWrites=true&w=majority")

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    if client.test.akun_admin.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      return redirect(url_for('admin'))
    
    elif client.test.data_mhs.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      return redirect(url_for('dashboard', npm = client.test.data_mhs.find_one({"email": request.form['usrnm'] })["_id"]))
    
    elif client.test.data_dosen.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      return redirect(url_for('dosen', nrp = client.test.data_dosen.find_one({"email": request.form['usrnm'] })["_id"]))
    
    else:
      return render_template("auth/login.html", pesan = "Email atau kata sandi salah!")
  return render_template("auth/login.html")

@app.route('/forgot_pwd')
def forgot_pwd():
  return render_template("auth/forgot-password.html")

@app.route('/admin', methods=["POST", "GET"])
def admin():
  if "akun" in session:
    if request.method == "POST":
      if request.form["peran"] == "dosen":
        client.test.data_dosen.insert_one({"_id" : request.form["id"], "nama" : request.form["nama"], "prodi" : request.form["prodi"], "email" : request.form["email"], "sandi" : request.form["sandi"]})  
      elif request.form["peran"] == "mhs":
        client.test.data_mhs.insert_one({"_id" : request.form["id"], "nama" : request.form["nama"], "prodi" : request.form["prodi"], "email" : request.form["email"], "sandi" : request.form["sandi"]})
      return render_template("dashboard_admin/dashboard.html", email = session['akun'])
    return render_template("dashboard_admin/dashboard.html", email = session['akun'])
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/admin/daftar-dosen/<prodi>', methods=["POST", "GET"])
def daftar_dosen(prodi):
  if "akun" in session:
    cursor = client.test.data_dosen.find({"prodi" : prodi})
    data = []

    for i, item in enumerate(cursor):
      data.append(list(item.values()))
      data[i].append(i+1)

    return render_template("dashboard_admin/tables.html", email = session['akun'], data = data, id = "NRP", keterangan = "Daftar Data Dosen")
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/admin/daftar-mhs/<prodi>')
def daftar_mhs(prodi):
  if "akun" in session:
    cursor = client.test.data_mhs.find({"prodi" : prodi})
    data = []

    for i, item in enumerate(cursor):
      data.append(list(item.values()))
      data[i].append(i+1)

    return render_template("dashboard_admin/tables.html", email = session['akun'], data = data, id = "NPM", keterangan = "Daftar Data Mahasiswa")
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/admin/hapus/<peran>/<unik>')
def hapus(peran, unik):
  if "akun" in session:
    if "@student.upnjatim" not in peran:
      client.test.data_dosen.delete_one({"_id": unik})
      return redirect(url_for('admin'))
    elif "@student.upnjatim" in peran:
      client.test.data_mhs.delete_one({"_id": unik})
      return redirect(url_for('admin'))
    pass
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/admin/edit/<peran>/<unik>', methods=["POST", "GET"])
def edit(peran, unik):
  if "akun" in session and request.method == "POST":
    if "@student.upnjatim" not in peran:
      client.test.data_dosen.update_one({"_id" : unik},
                                        {"$set" : {"nama" : request.form['nama'],
                                                  "prodi" : request.form['prodi'],
                                                  "email" : request.form['email'],
                                                  "sandi" : request.form['sandi']}})
      return redirect(url_for('admin'))

    elif "@student.upnjatim" in peran:
      client.test.data_mhs.update_one({"_id" : unik},
                                      {"$set" : {"nama" : request.form['nama'],
                                                 "prodi" : request.form['prodi'],
                                                 "email" : request.form['email'],
                                                 "sandi" : request.form['sandi']}})
      return redirect(url_for('admin'))
    pass
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/dashboard/<npm>')
def dashboard(npm):
  if "akun" in session:
    data_mhs = client.test.data_mhs.find_one({"_id" : npm})
    return render_template("dashboard/dashboard.html", data_mhs = data_mhs)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.route('/dosen/<nrp>')
def dosen(nrp):
  if "akun" in session :
    data_dosen = client.test.data_dosen.find_one({"_id": nrp })
    return render_template("dashboard_dosen/dashboard.html", data_dosen = data_dosen)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

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

@app.route('/keluar')   # LOG OUT
def keluar():
  if 'akun' in session :
    session.pop('akun')
    return redirect('/')
  else:
    return redirect('/')