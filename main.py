# BUILT IN LIBARIES
import datetime

# FRAMEWORKS
from pymongo import MongoClient
from pyrebase import initialize_app
from flask_mail import Mail, Message
from flask import Flask, render_template, url_for, session, request, redirect

app = Flask(__name__)

# AGAR FLASK-SESSION DAPAT BEKERJA
app.secret_key = "rahasia"

# UNTUK MEMANFAATKAN LAYANAN GMAIL
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rahasia'
app.config['MAIL_PASSWORD'] = 'rahasia'

mail = Mail(app)

# SAMBUNGKAN KE CLOUD STORAGE
firebase_config = {"apiKey" : "rahasia",
                   "authDomain" : "rahasia",
                   "databaseURL" : "rahasia",
                   "projectId" : "rahasia",
                   "storageBucket" : "rahasia",
                   "messagingSenderId" : "rahasia",
                   "serviceAccount":"firebase_key.json"}

# UNTUK MENGAKSES FILES YANG TERSIMPAN PADA Firebase Storage
storage = initialize_app(firebase_config).storage()

# SAMBUNGAN KE CLOUD DATABASE
client = MongoClient("rahasia")
# SAMBUNGAN KE MASING-MASING collection PADA DATABASE MongoDB
col_admin = client.test.akun_admin
col_dosen = client.test.data_dosen
col_mhs = client.test.data_mhs

# LANDING PAGE WEBSITE
@app.route('/', methods=['GET', 'POST'])
def index():
  # APABILA PENGUNJUNG HENDAK MENGIRIM PESAN MELALUI FORM Kontak
  if request.method == "POST":
    msg = Message(request.form['sender_subjek'],
                  # SELURUH KEGIATAN SURAT MENYURAT AKAN DIKIRIM MELALUI 17081010068@student.upnjatim.ac.id
                  sender = '17081010068@student.upnjatim.ac.id',
                  # recipients DI SINI ADALAH EMAIL RESMI ADMINISTRATOR/DEVELOPER FIK-OCW
                  recipients = ['roploverz@gmail.com', 'maulidr17@gmail.com', 'putraanggara212@gmail.com', 'fitriauliayuliandiputri@gmail.com'])
                
    msg.body = "Email : " + request.form['sender_email'] + '\nNama Pengirim : ' + request.form['sender'] + '\n\nPesan :\n' + request.form['pesan_banyak']
    mail.send(msg)

    return render_template("index.html", pesan = "Pesan berhasil terkirim!")
  return render_template("index.html")

# HALAMAN LOGIN UNTUK ADMIN, DOSEN, DAN MAHASISWA
@app.route('/login', methods=["POST", "GET"])
def login():
  # JIKA PROSES AUTENTIKASI BERHASIL MAKA TIAP USER DENGAN ROLE YANG BERBEDA AKAN LANGSUNG
  # DIARAHKAN KE DASHBOARD MEREKA MASING-MASING MELALUI return redirect(url_for(...))
  if request.method == "POST":
    # PROSES AUTENTIKASI AKUN ADMIN
    if col_admin.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      return redirect(url_for('admin'))

    # PROSES AUTENTIKASI AKUN MAHASISWA
    elif col_mhs.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      npm = col_mhs.find_one({"email": request.form['usrnm'] })["_id"]
      return redirect(url_for('dashboard', npm = npm))
    
    # PROSES AUTENTIKASI AKUN DOSEN
    elif col_dosen.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      nrp = col_dosen.find_one({"email": request.form['usrnm'] })["_id"]
      return redirect(url_for('dosen', nrp = nrp))
    
    # JIKA PROSES AUTENTIKASI GAGAL
    else:
      return render_template("auth/login.html", pesan = "Email atau kata sandi salah!")
      
  return render_template("auth/login.html")

# HALAMAN LUPA KATA SANDI UNTUK ADMIN, DOSEN, DAN MAHASISWA 
@app.route('/forgot_pwd')
def forgot_pwd():
  return render_template("auth/forgot-password.html")

'''
SEBELUM USER MENGAKSES LAMAN DASHBOARD MASING-MASING
"akun" YANG ADA PADA SESSION DICEK TERLEBIH DAHULU
MELALUI BARIS KODE if "akun" in session
APABILA SUDAH LOGIN MAKA USER TERSEBUT DAPAT MENGAKSES DASHBOARD
JIKA TIDAK MAKA WEBSITE AKAN MENGARAHKAN KE LAMAN LOGIN
MELALUI BARIS KODE return render_template("auth/login.html"....
'''

# HALAMAN DASHBOARD MENU ADMINISTRATOR
@app.route('/admin', methods=["POST", "GET"])
def admin():
  if "akun" in session:
    # UNTUK MENGETAHUI JUMLLAH AKUN MAHASISWA DAN DOSEN
    jumlah = [col_mhs.count_documents({"prodi" : "Sistem Informasi"}),
              col_mhs.count_documents({"prodi" : "Informatika"}),
              col_dosen.count_documents({"prodi" : "Sistem Informasi"}),
              col_dosen.count_documents({"prodi" : "Informatika"})]
    
    sandi = col_admin.find_one({"email" : session['akun']})['sandi']
    
    # TAMBAH AKUN BARU - DILAKUKAN JIKA NPM/NRP TIDAK ADA PADA DATABASE
    if request.method == "POST" and col_dosen.find_one({"_id" : request.form['id']}) is None and col_mhs.find_one({"_id" : request.form['id']}) is None :
      # MENAMBAHKAN AKUN DOSEN KE MongoDB 
      if request.form["peran"] == "dosen":
        col_dosen.insert_one({"_id" : request.form["id"],
                              "nama" : request.form["nama"],
                              "prodi" : request.form["prodi"],
                              "email" : request.form["email"],
                              "sandi" : request.form["sandi_baru2"]})
        # BUAT DIREKTORI BARU UNTUK MENYIMPAN FILES DOSEN
        storage.child(request.form['prodi'] + '/' + request.form['id'] + '/0').put('0.txt')

      # MENAMBAHKAN AKUN MAHASISWA KE MongoDB
      elif request.form["peran"] == "mhs":
        col_mhs.insert_one({"_id" : request.form["id"],
                            "nama" : request.form["nama"],
                            "prodi" : request.form["prodi"],
                            "email" : request.form["email"],
                            "sandi" : request.form["sandi_baru2"]})
      
      # LAMAN AKAN REFRESH JIKA PENAMBAHAN AKUN BERHASIL
      return redirect(url_for('admin'))
    
    # JIKA NPM/NRP SUDAH ADA PADA DATABASE bug
    elif request.method == "POST" and col_dosen.find_one({"_id" : request.form['id']}) is not None and col_mhs.find_one({"_id" : request.form['id']}) is not None :
      return render_template("dashboard_admin/dashboard.html",
                            email = session['akun'],
                            jumlah = jumlah, sandi = sandi,
                            pesan = "NRP/NPM ini sudah ada")
    
    # TAMPILAN DEFAULT DARI .html YANG TERENDER
    return render_template("dashboard_admin/dashboard.html",
                          email = session['akun'],
                          jumlah = jumlah, sandi = sandi)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN DAFTAR AKUN DOSEN
@app.route('/admin/daftar-dosen/<prodi>', methods=["POST", "GET"])
def daftar_dosen(prodi):
  if "akun" in session:
    data_dosen = col_dosen.find({"prodi" : prodi})
    data = []

    # DATA DOSEN DITAMPUNG KE DALAM LIST data
    # INI DILAKUKAN AGAR NILAINYA MUDAH DITAMPILAN PADA TABEL
    for i, akun in enumerate(data_dosen):
      data.append(list(akun.values()))
      data[i].append(i+1)

    # NILAI PADA VARIABEL sandi, keterangan, email, data, dan id
    # MENJADI PARAMETER FUNGSI render_template NANTI AKAN DITAMPILKAN
    # PADA tables.html YANG TERENDER
    return render_template("dashboard_admin/tables.html",
                          sandi = col_admin.find_one({"email" : session['akun']})['sandi'],
                          keterangan = "Daftar Data Dosen",
                          email = session['akun'],
                          data = data, id = "NRP")
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN DAFTAR AKUN MAHASISWA
# CARA KERJANYA SAMA DENGAN YANG
# ADA PADA HALAMAN DAFTAR AKUN DOSEN
@app.route('/admin/daftar-mhs/<prodi>', methods=["POST", "GET"])
def daftar_mhs(prodi):
  if "akun" in session:
    data_mhs = col_mhs.find({"prodi" : prodi})
    data = []

    for i, akun in enumerate(data_mhs):
      data.append(list(akun.values()))
      data[i].append(i+1)

    return render_template("dashboard_admin/tables.html",
                          sandi = col_admin.find_one({"email" : session['akun']})['sandi'],
                          keterangan = "Daftar Data Mahasiswa",
                          email = session['akun'],
                          data = data, id = "NPM")
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HAPUS AKUN DOSEN DAN MAHASISWA
@app.route('/admin/hapus/<peran>/<unik>')
def hapus(peran, unik):
  if "akun" in session:
    # HAPUS AKUN DOSEN PADA MongoDB DAN SELURUH
    # DATA-DATA YANG ADA PADA DIREKTORI storage
    if "@student.upnjatim" not in peran:
      data_dosen = col_dosen.find_one({"_id": unik})

      files = [i.name for i in storage.list_files() if data_dosen['_id'] in i.name]
      for i in files:
        storage.delete(i)

      col_dosen.delete_one({"_id": unik})
      return redirect(url_for('admin'))
    
    # HAPUS AKUN MAHASISWA YANG ADA DI MongoDB
    elif "@student.upnjatim" in peran:
      col_mhs.delete_one({"_id": unik})
      return redirect(url_for('admin'))

    # KARENA TIDAK MENGEMBALIKAN NILAI KEMBALIAN
    pass
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# EDIT AKUN ADMIN, DOSEN, DAN MAHASISWA
@app.route('/admin/edit/<peran>/<unik>', methods=["POST", "GET"])
def edit(peran, unik):
  if "akun" in session and request.method == "POST":
    # EDIT KATA SANDI ADMIN
    if "@admin.fik_ocw" in peran:
      col_admin.update_one({"email" : unik},
                           {"$set" : {"sandi" : request.form['sandi_baru_2']}})
      return redirect(url_for('admin'))

    # EDIT AKUN DOSEN
    elif "@student.upnjatim" not in peran:
      #data_dosen = col_dosen.find_one({"_id" : unik})

      col_dosen.update_one({"_id" : unik},
                           {"$set" : {"nama" : request.form['nama'],
                                      "email" : request.form['email'],
                                      "sandi" : request.form['sandi_baru']}})

      return redirect(url_for('admin'))

    # EDIT AKUN MAHASISWA
    elif "@student.upnjatim" in peran:
      col_mhs.update_one({"_id" : unik},
                         {"$set" : {"nama" : request.form['nama'],
                                    "prodi" : request.form['prodi'],
                                    "email" : request.form['email'],
                                    "sandi" : request.form['sandi_baru']}})
      return redirect(url_for('admin'))

    # KARENA TIDAK MENGEMBALIKAN NILAI KEMBALIAN
    pass
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN DASHBOARD MENU DOSEN
@app.route('/dosen/<nrp>')
def dosen(nrp):
  if "akun" in session :
    data_dosen = col_dosen.find_one({"_id": nrp })
    return render_template("dashboard_dosen/dashboard.html", data_dosen = data_dosen)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN TAMBAH MATA KULIAH OLEH DOSEN
@app.route('/dosen/<nrp>/tambah-mata-kulah', methods=['POST', 'GET'])
def tambah_mata_kuliah(nrp):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    daftar_matkul = [ i.name.split('/')[2] for i in storage.list_files() if data_dosen['_id'] in i.name ]
    daftar_matkul.pop(0)

    # TAMBAH MATA KULIAH BARU
    if request.method == "POST":
      # UNTUK MENENTUKAN SEMESTER PERKULIAHAN
      if datetime.date.today() < datetime.date(datetime.date.today().year, 7, 1):
        smt = "GENAP"
      else:
        smt = "GANJIL"
      tahun = str(datetime.date.today().year)
      
      if str(request.form['nama_mata_kuliah'] + " " + request.form['kelas_paralel']+ " " + tahun + " " + smt) in daftar_matkul:
        return render_template("dashboard_dosen/tambah_matkul.html",
                               data_dosen = data_dosen, pesan = "Mata kuliah tersebut sudah ada!",
                               daftar_matkul = daftar_matkul)
      
      else:
        storage.child(data_dosen['prodi'] + "/" +
                    data_dosen['_id'] + "/" +
                    request.form['nama_mata_kuliah'] + " " +
                    request.form['kelas_paralel']+ " " +
                    tahun + " " + smt +'/0').put('0.txt')

        return redirect(url_for('tambah_mata_kuliah', nrp = data_dosen['_id']))

    return render_template("dashboard_dosen/tambah_matkul.html",
                           data_dosen = data_dosen,
                           daftar_matkul = daftar_matkul)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# LAMAN HAPUS MATA KULIAH
@app.route('/dosen/<nrp>/<matkul>/hapus-mata-kulah', methods=['POST', 'GET'])
def hapus_mata_kuliah(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })

    daftar_matkul = [i.name for i in storage.list_files() if data_dosen['_id'] and matkul in i.name]
    for i in daftar_matkul:
      storage.delete(i)

    return redirect(url_for('tambah_mata_kuliah', nrp = data_dosen['_id']))
  else :
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# LAMAN MATA KULIAH
@app.route('/dosen/<nrp>/<matkul>')#, methhods=['GET', 'POST'])
def mata_kuliah_dos(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    return render_template("dashboard_dosen/mata_kuliah.html", data_dosen = data_dosen, mata_kul = matkul)
  else :
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN TAMBAH MATERI/TUGAS
@app.route('/dosen/<nrp>/<matkul>/tambah-tugas/<pekan>')
def tambah_edit_tugas(nrp, matkul, pekan):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    
    if request.method == "POST" and request.form['judul_materi'] is not None:
      if request.files['materi_video'] is not None:
        storage.child(data_dosen['prodi'] + '/' + data_dosen['_id'] + '/ '+ matkul + 'Materi/Pekan ' + pekan + '/' + request.files['materi_video'])
      if request.files['materi_pdf_zip'] is not None:
        storage.child(data_dosen['prodi'] + '/' + data_dosen['_id'] + '/ '+ matkul + 'Materi/Pekan ' + pekan + '/' + request.files['materi_pdf_zip'])

    if request.method == "POST" and request.form['judul_tugas'] is not None:
      pass

    return redirect(url_for('tambah_edit_tugas', nrp=data_dosen['_id'], matkul=matkul, pekan = pekan))# render_template("dashboard_dosen/tambah_edit_tugas.html", data_dosen = data_dosen, mata_kul = matkul, pekan = pekan )
  else :
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# HALAMAN DASHBOARD MENU MAHASISWA
@app.route('/dashboard/<npm>')
def dashboard(npm):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})
    return render_template("dashboard/dashboard.html", data_mhs = data_mhs)
  else:
    return render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('auth/404.html'), 404

# LOG OUT
@app.route('/keluar')
def keluar():
  if 'akun' in session :
    session.pop('akun')
    return redirect('/')
  else:
    return redirect('/')

app.run(debug=True)
