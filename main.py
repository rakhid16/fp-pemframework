# BUILT IN LIBARIES
from datetime import date, datetime, timedelta

# FRAMEWORKS
from pymongo import MongoClient
from pyrebase import initialize_app
from flask_mail import Mail, Message
from flask import Flask, render_template, url_for, session, request, redirect

# UNTUK ROUTING
app = Flask(__name__)

# AGAR SESSION DAPAT BEKERJA
app.secret_key = "rahasia"

# UNTUK MEMANFAATKAN LAYANAN GMAIL
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rahasia'
app.config['MAIL_PASSWORD'] = 'rahasia'

mail = Mail(app)

# SAMBUNGAN KE FIREBASE CLOUD STORAGE
firebase_config = {"apiKey" : "rahasia",
                   "authDomain" : "rahasia",
                   "databaseURL" : "rahasia",
                   "projectId" : "rahasia",
                   "storageBucket" : "rahasia",
                   "messagingSenderId" : "rahasia",
                   "serviceAccount":"firebase_key.json"}

# VARIABEL UNTUK AKSES FILES YANG TERSIMPAN PADA FIREBASE CLOUD STORAGE
storage = initialize_app(firebase_config).storage()

# SAMBUNGAN KE MONGODB CLOUD DATABASE
client = MongoClient("rahasia")

# SAMBUNGAN KE MASING-MASING COLLECTION
col_admin = client.test.akun_admin
col_dosen = client.test.data_dosen
col_mhs = client.test.data_mhs

# FUNGSI UNTUK MENGIRIM EMAIL
def kirm_email(subjek, pengirim, penerima, pesan):
  msg = Message(subjek, sender= pengirim, recipients = penerima)
  msg.body = pesan
  mail.send(msg)

# LANDING PAGE WEBSITE
@app.route('/', methods=['GET', 'POST'])
def index():
  # APABILA PENGUNJUNG MENGIRIM PESAN MELALUI BAGIAN KONTAK
  if request.method == "POST":
    kirm_email(request.form['sender_subjek'],
              '17081010068@student.upnjatim.ac.id',
              ['roploverz@gmail.com', 'maulidr17@gmail.com', 'putraanggara212@gmail.com', 'fitriauliayuliandiputri@gmail.com'],
              "Email : " + request.form['sender_email'] + '\nNama Pengirim : ' + request.form['sender'] + '\n\nPesan :\n' + request.form['pesan_banyak'])

    return render_template("index.html", pesan = "Pesan berhasil terkirim!")
  return render_template("index.html")

# HALAMAN LOGIN UNTUK ADMIN, DOSEN, DAN MAHASISWA
@app.route('/login', methods=["POST", "GET"])
def login():
  # TIAP USER DENGAN ROLE YANG BERBEDA AKAN LANGSUNG DIARAHKAN KE DASHBOARD MEREKA MASING-MASING
  if request.method == "POST":
    # PROSES AUTENTIKASI AKUN ADMIN
    if col_admin.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      return redirect(url_for('admin'))

    # PROSES AUTENTIKASI AKUN MAHASISWA
    elif col_mhs.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      npm = col_mhs.find_one({"email": request.form['usrnm'] })["_id"]
      return redirect(url_for('mahasiswa', npm = npm))
    
    # PROSES AUTENTIKASI AKUN DOSEN
    elif col_dosen.find_one({"email" : request.form['usrnm'], "sandi" : request.form['pwd']}) is not None:
      session['akun'] = request.form['usrnm']
      nrp = col_dosen.find_one({"email": request.form['usrnm'] })["_id"]
      return redirect(url_for('dosen', nrp = nrp))
    
    else: # JIKA PROSES AUTENTIKASI GAGAL
      return render_template("auth/login.html", pesan = "Email atau kata sandi salah!")
      
  return render_template("auth/login.html")

# HALAMAN LUPA KATA SANDI UNTUK DOSEN DAN MAHASISWA 
@app.route('/forgot_pwd')
def forgot_pwd():
  return render_template("auth/forgot-password.html")

# HALAMAN DASHBOARD MENU ADMINISTRATOR
@app.route('/admin', methods=["POST", "GET"])
def admin():
  if "akun" in session:
    # UNTUK MENGETAHUI JUMLLAH AKUN MAHASISWA DAN DOSEN
    jumlah = [col_mhs.count_documents({"prodi" : "Sistem Informasi"}), col_mhs.count_documents({"prodi" : "Informatika"}),
              col_dosen.count_documents({"prodi" : "Sistem Informasi"}), col_dosen.count_documents({"prodi" : "Informatika"})]
    
    sandi = col_admin.find_one({"email" : session['akun']})['sandi']
    
    # TAMBAH AKUN BARU - DILAKUKAN JIKA NPM/NRP TIDAK ADA PADA DATABASE
    if request.method == "POST":
      if col_dosen.find_one({"_id" : request.form['id']}) is None and col_mhs.find_one({"_id" : request.form['id']}) is None :
        # MENAMBAHKAN AKUN DOSEN KE MONGODB
        if request.form["peran"] == "dosen":
          col_dosen.insert_one({"_id" : request.form["id"],
                                "nama" : request.form["nama"],
                                "prodi" : request.form["prodi"],
                                "email" : request.form["email"],
                                "sandi" : request.form["sandi_baru2"]})
          # BUAT DIREKTORI BARU UNTUK MENYIMPAN FILES DOSEN PADA FIREBASE CLOUD STORGAE
          storage.child(request.form['prodi'] + '/' + request.form['id'] + '/0').put('0.txt')

        # MENAMBAHKAN AKUN MAHASISWA KE MONGODB
        elif request.form["peran"] == "mhs":
          col_mhs.insert_one({"_id" : request.form["id"],
                              "nama" : request.form["nama"],
                              "prodi" : request.form["prodi"],
                              "email" : request.form["email"],
                              "sandi" : request.form["sandi_baru2"]})

        # LAMAN AKAN REFRESH JIKA PENAMBAHAN AKUN BERHASIL
        return redirect(url_for('admin'))
    
      # JIKA NPM/NRP SUDAH ADA PADA DATABASE
      if col_dosen.find_one({"_id" : request.form['id']}) is not None or col_mhs.find_one({"_id" : request.form['id']}) is not None :
        return render_template("admin/dashboard.html", email = session['akun'], jumlah = jumlah, sandi = sandi, pesan = "NRP/NPM ini sudah ada")
    
    return render_template("admin/dashboard.html", email = session['akun'], jumlah = jumlah, sandi = sandi, pesan = '')
  else:
    return redirect(url_for('login'))

# HALAMAN DAFTAR AKUN DOSEN
@app.route('/admin/daftar-dosen/<prodi>', methods=["POST", "GET"])
def daftar_dosen(prodi):
  if "akun" in session:
    data_dosen = col_dosen.find({"prodi" : prodi})
    data = []

    # DATA DOSEN DITAMPUNG KE DALAM LIST AGAR MUDAH DITAMPILAN PADA TABEL
    for i, akun in enumerate(data_dosen):
      data.append(list(akun.values()))
      data[i].append(i+1)

    # NILAI PADA VARIABEL sandi, keterangan, email, data, dan id
    # MENJADI PARAMETER FUNGSI render_template NANTI AKAN DITAMPILKAN
    # PADA tables.html YANG TERENDER
    return render_template("admin/tabel.html", sandi = col_admin.find_one({"email" : session['akun']})['sandi'],
                          keterangan = "Daftar Data Dosen", email = session['akun'], data = data, id = "NRP")
  else:
    return redirect(url_for('login'))

# HALAMAN DAFTAR AKUN MAHASISWA - CARA KERJANYA SAMA DENGAN DAFTAR AKUN DOSEN
@app.route('/admin/daftar-mhs/<prodi>', methods=["POST", "GET"])
def daftar_mhs(prodi):
  if "akun" in session:
    data_mhs = col_mhs.find({"prodi" : prodi})
    data = []

    for i, akun in enumerate(data_mhs):
      data.append(list(akun.values()))
      data[i].append(i+1)

    return render_template("admin/tabel.html", sandi = col_admin.find_one({"email" : session['akun']})['sandi'],
                          keterangan = "Daftar Data Mahasiswa", email = session['akun'], data = data, id = "NPM")
  else:
    return redirect(url_for('login'))

# HAPUS AKUN DOSEN DAN MAHASISWA
@app.route('/admin/hapus/<peran>/<unik>')
def hapus(peran, unik):
  if "akun" in session:
    # HAPUS AKUN DOSEN PADA MONGODB DAN FILES YANG ADA PADA FIREBASE CLOUD STORAGE
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

    pass
  else:
    return redirect(url_for('login'))

# EDIT DATA ADMIN, DOSEN, DAN MAHASISWA
@app.route('/admin/edit/<peran>/<unik>', methods=["POST", "GET"])
def edit(peran, unik):
  if "akun" in session and request.method == "POST":
    # EDIT KATA SANDI ADMIN
    if "@admin.fik_ocw" in peran:
      col_admin.update_one({"email" : unik}, {"$set" : {"sandi" : request.form['sandi2']}})
      return redirect(url_for('admin'))

    # EDIT DATA DOSEN
    elif "@student.upnjatim" not in peran:
      col_dosen.update_one({"_id" : unik},
                           {"$set" : {"email" : request.form['email'],
                                      "sandi" : request.form['sandi']}})
      return redirect(url_for('admin'))

    # EDIT AKUN MAHASISWA
    elif "@student.upnjatim" in peran:
      col_mhs.update_one({"_id" : unik},
                         {"$set" : {"email" : request.form['email'],
                                    "sandi" : request.form['sandi']}})        
      return redirect(url_for('admin'))

    pass
  else:
    return redirect(url_for('login'))

# DASHBOARD MENU DOSEN
@app.route('/dosen/<nrp>')
def dosen(nrp):
  if "akun" in session :
    data_dosen = col_dosen.find_one({"_id": nrp })
    return render_template("dosen/dashboard.html", data_dosen = data_dosen)
  else:
    return redirect(url_for('login'))

# TAMBAH MATA KULIAH OLEH DOSEN
@app.route('/dosen/<nrp>/tambah-mata-kulah', methods=['POST', 'GET'])
def tambah_mata_kuliah(nrp):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    
    daftar_matkul = [ i.name.split('/')[2] for i in storage.list_files() if data_dosen['_id'] in i.name ]
    daftar_matkul.pop(0)
    a = set(daftar_matkul)
    daftar_matkul = list(a)
    del a

    # TAMBAH MATA KULIAH BARU
    if request.method == "POST":
      # UNTUK MENENTUKAN SEMESTER PERKULIAHAN
      if date.today() < date(date.today().year, 7, 1):
        smt = "GENAP"
      else:
        smt = "GANJIL"
      tahun = str(date.today().year)
      
      # JIKA MATA KULIAH YANG DIAMPU SUDAH ADA
      if str(request.form['nama_mata_kuliah']+" "+request.form['kelas_paralel']+" "+tahun+" "+smt) in daftar_matkul:
        return render_template("dosen/tambah_matkul.html", pesan = "Mata kuliah tersebut sudah ada!",
                              data_dosen = data_dosen, daftar_matkul = daftar_matkul)
      
      # JIKA MATA KULIAH YANG DIAMPU ADALAH MATA KULIAH BARU
      else:
        storage.child(data_dosen['prodi']+"/"+data_dosen['_id']+"/"+request.form['nama_mata_kuliah']+" "+request.form['kelas_paralel']+" "+tahun+" "+smt+'/0').put('0.txt')
        return redirect(url_for('tambah_mata_kuliah', nrp = data_dosen['_id']))

    return render_template("dosen/tambah_matkul.html", data_dosen = data_dosen, daftar_matkul = daftar_matkul)
  else:
    return redirect(url_for('login'))

# HAPUS MATA KULIAH
@app.route('/dosen/<nrp>/<matkul>/hapus-mata-kulah', methods=['POST', 'GET'])
def hapus_mata_kuliah(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })

    daftar_matkul = [i.name for i in storage.list_files() if data_dosen['_id'] and matkul in i.name]
    
    # HAPUS SELURUH FILES YANG BERADA PADA DIREKTORI MATA KULIAH TERSEBUT
    for i in daftar_matkul:
      storage.delete(i)

    return redirect(url_for('tambah_mata_kuliah', nrp = data_dosen['_id']))
  else :
    return redirect(url_for('login'))

# LAMAN MATA KULIAH
@app.route('/dosen/<nrp>/<matkul>')
def mata_kuliah_dos(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    return render_template("dosen/mata_kuliah.html", data_dosen = data_dosen, mata_kul = matkul)
  else :
    return redirect(url_for('login'))

# HALAMAN TAMBAH/EDIT MATERI
@app.route('/dosen/<nrp>/<matkul>/tambah-materi/<pekan>', methods=['GET', 'POST'])
def tambah_edit_materi(nrp, matkul, pekan):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    # UNTUK MENDAPATKAN FILES MATERI PADA PEKAN TERSEBUT
    materi = [ i.name.split('/')[5] for i in storage.list_files() if data_dosen['_id'] and matkul+'/Materi/Pekan '+pekan in i.name ]
    
    # VARIABEL BANTU
    pdf, video = '', ''
    pdf_dir = data_dosen['prodi']+'/'+data_dosen['_id']+'/'+matkul+'/Materi/Pekan '+pekan+'/'+'dokumen.pdf'
    video_dir = data_dosen['prodi']+'/'+data_dosen['_id']+'/'+matkul+'/Materi/Pekan '+pekan+'/'+'video.mp4'

    # JIKA MATERI ADA PADA DIREKTORI PENYIMPANAN MAKA AKAN DITAMPILKAN MELALUI LAMAN HTML
    if not materi == False:
      if "video.mp4" in materi:
        video = storage.child(video_dir).get_url(None)
      if "dokumen.pdf" in materi:
        pdf = storage.child(pdf_dir).get_url(None)
    else:
      pass

    # PROSES PENGUNGGAHAN MATERI YANG DILAKUKAN OLEH DOSEN
    if request.method == "POST":
      if request.files['materi_video']:
        storage.child(video_dir).put(request.files['materi_video'])
      if request.files['materi_pdf']:
        storage.child(pdf_dir).put(request.files['materi_pdf'])
     
      return redirect(url_for('tambah_edit_materi', nrp=data_dosen['_id'], matkul=matkul, pekan = pekan))

    return render_template("dosen/tambah_edit_materi.html",
                           data_dosen = data_dosen, mata_kul = matkul,
                           pekan = pekan, url_video = video, url_pdf = pdf)
  else :
    return redirect(url_for('login'))

# LAMAN UNTUK MENGHAPUS MATERI
@app.route('/dosen/<nrp>/<matkul>/hapus_tugas/<pekan>/<jenis>')
def hapus_materi(nrp, matkul, pekan, jenis):
  if "akun" in session:
    data_dosen = col_dosen.find_one({'_id' : nrp})

    # HAPUS MATERI VIDEO ATAU PDF
    if jenis == "video":
      storage.delete(data_dosen['prodi']+'/'+nrp+'/'+matkul+'/Materi/Pekan '+pekan+'/video.mp4')
    elif jenis == "pdf":
      storage.delete(data_dosen['prodi']+'/'+nrp+'/'+matkul+'/Materi/Pekan '+pekan+'/dokumen.pdf')

    return redirect(url_for('tambah_edit_materi', nrp = nrp, matkul = matkul, pekan = pekan))
  else:
    render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# LAMAN UNTUK MENGHAPUS DAN MENGEDIT TUGAS 
@app.route('/dosen/<nrp>/<matkul>/tambah-tugas/<pekan>', methods=['GET', 'POST'])
def tambah_edit_tugas(nrp, matkul, pekan):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    
    # JIKA TUGAS PERNAH DIBUAT SEBELUMNYA MAKA
    # PROGRAM AKAN MENGAMBIL DATA PADA MONGODB
    if ("Mata kuliah" in col_dosen.find_one({"_id" : data_dosen['_id']})) is True and (matkul in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah']) is True and ("Pekan " + pekan in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah'][matkul]) is True:
      isian = [data_dosen['Mata kuliah'][matkul]["Pekan " + pekan]['Nama Tugas'],
               data_dosen['Mata kuliah'][matkul]["Pekan " + pekan]['Tanggal batas pengumpulan'],
               data_dosen['Mata kuliah'][matkul]["Pekan " + pekan]['Pukul batas pengumpulan'].split(':')[0],
               data_dosen['Mata kuliah'][matkul]["Pekan " + pekan]['Pukul batas pengumpulan'].split(':')[1],
               data_dosen['Mata kuliah'][matkul]["Pekan " + pekan]['Deskripsi Tugas']]
    
    # JIKA TIDAK MAKA PROGRAM AKAN MELAKUKAN
    # PENUGASAN PADA VARIABEL SEPERTI BERIKUT
    else:
      isian = ["Masukkan Judul", '', '', '', "Tulis deskripsi"]

    # JIKA DOSEN MELAKUKAN PENAMBAHAN/PERUBAHAN TUGAS
    if request.method == "POST":
      # MENAMPUNG NILAI MASUKAN DARI WEBSITE
      tugas_pekan = {"Tugas pekan ke" : pekan,
                    "Nama Tugas" : request.form['nama_tugas'],
                    "Tanggal batas pengumpulan" : request.form['dedline'],
                    "Pukul batas pengumpulan" : request.form['jam'] + ':' + request.form['menit'],
                    "Deskripsi Tugas" : request.form['deskripsi_tugas']}

      # TUGAS AKAN TERSIMPAN PADA MONGODB
      # POTONGAN KODE DI BAWAH INI MENAMBAHKAN FIELD/OBJECT 'MATA KULIAH' PADA DOCUMENT
      # AKUN DOSEN APABILA FIELD TERSEBUT BELUM ADA SAMA SEKALI
      if ("Mata kuliah" in col_dosen.find_one({"_id" : data_dosen['_id']})) is False :
        document = col_dosen.find_one({"_id" : data_dosen['_id']})
        document['Mata kuliah'] = {matkul:{"Pekan " + pekan : tugas_pekan}}
        col_dosen.update_one({'_id': data_dosen['_id']}, {"$set": document})
      
      # MENAMBAHKAN FIELD SESUAI DENGAN NAMA MATA KULIAH KARENA FIELD
      # 'MATA KULIAH' SUDAH ADA PADA DOCUMENT DOSEN MASING-MASING
      elif ("Mata kuliah" in col_dosen.find_one({"_id" : data_dosen['_id']})) is True and (matkul in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah']) is False:
        document = col_dosen.find_one({"_id" : data_dosen['_id']})
        document['Mata kuliah'][matkul] = {"Pekan "+pekan : tugas_pekan}
        col_dosen.update_one({'_id': data_dosen['_id']}, {"$set": document})

      # MENAMBAHKAN FIELD TUGAS TIAP PEKAN KARENA FIELD
      # 'MATA KULIAH'/'NAMA MATAK ULIAH' SUDAH ADA SEBELUMNYA
      elif ("Mata kuliah" in col_dosen.find_one({"_id" : data_dosen['_id']})) is True and (matkul in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah']) is True and ("Pekan " + pekan in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah'][matkul]) is False:
        document = col_dosen.find_one({"_id" : data_dosen['_id']})
        document['Mata kuliah'][matkul]["Pekan " + pekan] = tugas_pekan
        col_dosen.update_one({'_id': data_dosen['_id']}, {"$set": document})

      # MENGUBAH ISI PADA FIELD TUGAS PER PEKAN KARENA
      # ISI DARI FIELD TERSEBUT SUDAH ADA SEBELUMNYA
      elif ("Mata kuliah" in col_dosen.find_one({"_id" : data_dosen['_id']})) is True and (matkul in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah']) is True and ("Pekan " + pekan in col_dosen.find_one({"_id" : data_dosen['_id']})['Mata kuliah'][matkul]) is True:
        document = col_dosen.find_one({"_id" : data_dosen['_id']})
        document['Mata kuliah'][matkul]["Pekan " + pekan]['Nama Tugas'] = request.form['nama_tugas']
        document['Mata kuliah'][matkul]["Pekan " + pekan]['Tanggal batas pengumpulan'] = request.form['dedline']
        document['Mata kuliah'][matkul]["Pekan " + pekan]['Pukul batas pengumpulan'] = request.form['jam'] + ':' + request.form['menit']
        document['Mata kuliah'][matkul]["Pekan " + pekan]['Deskripsi Tugas'] = request.form['deskripsi_tugas']

        col_dosen.update_one({'_id': data_dosen['_id']}, {"$set": document})

      return redirect(url_for('tambah_edit_tugas', nrp = data_dosen['_id'], matkul = matkul, pekan = pekan))

    return render_template("dosen/tambah_edit_tugas.html", data_dosen = data_dosen, mata_kul = matkul, pekan = pekan, isian = isian)
  else:
    return redirect(url_for('login'))

# UNTUK MENGHAPUS TUGAS YANG DIBERIKAN OLEH DOSEN ITU SENDIRI
@app.route('/dosen/<nrp>/<matkul>/<pekan>')
def hapus_tugas_dos(nrp, matkul, pekan):
  if "akun" in session:

    if ("Mata kuliah" in col_dosen.find_one({"_id" : nrp})) is True and (matkul in col_dosen.find_one({"_id" : nrp})['Mata kuliah']) is True and ("Pekan " + pekan in col_dosen.find_one({"_id" : nrp})['Mata kuliah'][matkul]) is True:  
      dokumen = col_dosen.find_one({'_id' : nrp})
      
      # HAPUS TUGAS TERSEBUT
      del dokumen['Mata kuliah'][matkul]['Pekan '+pekan]
      col_dosen.update_one({'_id' : nrp}, {"$set": dokumen})
      
      return redirect(url_for('tambah_edit_tugas', nrp = nrp, matkul = matkul, pekan = pekan))
    else:
      pass

    return redirect(url_for('tambah_edit_tugas', nrp = nrp, matkul = matkul, pekan = pekan))
  else :
    return redirect(url_for('login'))

# UNTUK LAMAN TUGAS TERKUMPUL
@app.route('/dosen/<nrp>/tugas-terkumpul')
def tugas_terkumpul(nrp):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })

    # CARI DAFTAR TUGAS TERKUMPUL
    daftar_matkul = [ i.name.split('/')[2] for i in storage.list_files() if data_dosen['_id'] in i.name ]
    daftar_matkul.pop(0)
    a = set(daftar_matkul)
    
    # TUGAS TERKUMPUL DITUGASKAN PADA VARIABEL daftar_matkul 
    daftar_matkul = list(a)
    del a

    return render_template("dosen/tugas_terkumpul.html", data_dosen = data_dosen, daftar_matkul = daftar_matkul) 
  else:
    return redirect(url_for('login'))

# UNTUK MELIHAT TUGAS TERKUMPUL TIAP MATKUL DARI MAHASISWA
@app.route('/dosen/<nrp>/tugas-terkumpul/<matkul>')
def tugas_terkumpul_permatkul(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    return render_template("dosen/tugas_terkumpul_permatkul.html", data_dosen = data_dosen, mata_kul = matkul)
  else:
    return redirect(url_for('login'))

# UNTUK MELIHAT MAHASISWA YANG MENGUMPULKAN TUGAS TIAP PEKAN
@app.route('/dosen/<nrp>/tugas-terkumpul/<matkul>/<pekan>')
def tugas_terkumpul_per_pekan(nrp, matkul, pekan):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })
    
    # AMBIL FILES YANG BERADA PADA FIREBASE CLOUD STORGAE
    daftar_mhs = [ i.name.split('/')[5] for i in storage.list_files() if data_dosen['prodi']+'/'+data_dosen['_id']+'/'+matkul+'/'+'Tugas Terkumpul/Pekan '+pekan in i.name]
    url_unduh_tugas_mhs = [storage.child(data_dosen['prodi']+'/'+data_dosen['_id']+'/'+matkul+'/'+'Tugas Terkumpul/Pekan '+pekan+'/'+i).get_url(None) for i in daftar_mhs]
    
    # JADIKAN KE DALAM BENTUK DICTIONARIES
    tugas_mhs = dict(zip(daftar_mhs,url_unduh_tugas_mhs))
    
    return render_template("dosen/tugas_terkumpul_per_pekan.html", data_dosen = data_dosen, mata_kul = matkul, matkul= matkul, pekan = pekan, tugas_mhs = tugas_mhs)
  else:
    return redirect(url_for('login'))

# LAMAN UNTUK MELIHAT NILAI MAHASISWA
@app.route('/dosen/<nrp>/nilai-mhs')
def nilai_mhs(nrp):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })

    # MENDAPATKAN DAFTAR MATA KULIAH YANG DIAMPU OLEH DOSEN TERSEBUT
    daftar_matkul = [ i.name.split('/')[2] for i in storage.list_files() if data_dosen['_id'] in i.name ]
    daftar_matkul.pop(0)
    a = set(daftar_matkul)
    daftar_matkul = list(a)
    del a

    return render_template("dosen/nilai_mhs.html", data_dosen = data_dosen, daftar_matkul = daftar_matkul)
  else:
    return redirect(url_for('login'))

# LAMAN UNTUK MELIHAT NILAI MAHASISWA PER MATKUL
@app.route('/dosen/<nrp>/nilai-mhs/<matkul>')
def nilai_mhs_permatkul(nrp, matkul):
  if "akun" in session:
    data_dosen = col_dosen.find_one({"_id": nrp })

    daftar_mhs = [ i for i in col_mhs.find({'prodi' : data_dosen['prodi']}) if 'Mata kuliah' in i]
    nama = [i['nama']+'!'+i['_id'] for i in daftar_mhs if matkul in i['Mata kuliah']]
    nilai = [i['Mata kuliah'][matkul] for i in daftar_mhs if matkul in i['Mata kuliah']]
    
    # NAMA, NILAI, DAN NPM DI JADIKAN KE DALAM BENTUK DICTIONARIES
    # AGAT DAPAT MUDAH DIAKSES PADA FILE HTML YANG AKAN DIRENDER
    daftar_mhs = dict(zip(nama, nilai))

    return render_template("dosen/nilai_mhs_permatkul.html", data_dosen = data_dosen, mata_kul = matkul, daftar_mhs = daftar_mhs)
  else:
    return redirect(url_for('login'))

# MENGUBAH NILAI MAHASISWA PERMATKUL
@app.route('/dosen/<nrp>/nilai-mhs/<matkul>/<npm>', methods=['GET', 'POST'])
def nilai_mhs_permatkul_ubah(nrp, matkul, npm):
  if "akun" in session and request.method=="POST":
    data_dosen = col_dosen.find_one({"_id": nrp })
    document = col_mhs.find_one({'_id' : npm})
    
    # INPUTAN DARI FILE HTML
    document['Mata kuliah'][matkul] = [request.form['pekan_0'], request.form['pekan_1'], request.form['pekan_2'], request.form['pekan_3'],
                                       request.form['pekan_4'], request.form['pekan_5'], request.form['pekan_6'], request.form['pekan_7'],
                                       request.form['pekan_8'], request.form['pekan_9'], request.form['pekan_10'], request.form['pekan_11'],
                                       request.form['pekan_12'], request.form['pekan_13'], request.form['pekan_14'], request.form['pekan_15']]
    # PROSES PENGUBAHAN NILAI
    col_mhs.update_one({'_id':npm}, {'$set':document})
    return redirect(url_for('nilai_mhs_permatkul', nrp=data_dosen['_id'], matkul=matkul))
  else:
    return redirect(url_for('login'))

# HALAMAN DASHBOARD MENU MAHASISWA
@app.route('/mhs/<npm>')
def mahasiswa(npm):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})
    return render_template("mhs/dashboard.html", data_mhs = data_mhs)
  else:
    return redirect(url_for('login'))

# HALAMAN AMBIL MATA KULIAH OLEH MAHASISWA
@app.route('/mhs/<npm>/ambil-mata-kuliah/<mata_kul>', methods=['GET', 'POST'])
def ambil_matkul(npm, mata_kul):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})

    # MENGAMBIL SELURUH DAFTAR MATA KULIAH PADA FIK-OCW
    daftar_matkul = [ i.name.split('/')[2] for i in storage.list_files() if data_mhs['prodi'] in i.name ]
    a = set(daftar_matkul)
    daftar_matkul = list(a)
    daftar_matkul.remove('0')
    del a
    
    # PROSES PENAMBAHAN MATA KULIAH BARU
    if mata_kul != 'baru':
      if ("Mata kuliah" in col_mhs.find_one({"_id" : npm})) is False :
        document = col_mhs.find_one({"_id" : npm})
        document['Mata kuliah'] = {mata_kul: [0 for i in range(16)]}
        col_mhs.update_one({'_id': npm}, {"$set": document})
      
      # PROSES PENAMBAHAN APABILA FIELD 'MATA KULIAH'
      # PADA DOCUMENT MAHASISWA TERSEBUT SUDAH ADA
      else:
        document = col_mhs.find_one({"_id" : npm})
        document['Mata kuliah'][mata_kul] = [0 for i in range(16)]
        col_mhs.update_one({'_id': npm}, {"$set": document})

      return redirect(url_for('matkul_terambil', npm = data_mhs['_id']))
    
    # APABILA MATA KULIAH TERSEBUT SUDAH ADA
    # MAKA PROGRAM HANYA AKAN MEREFRESH HALAMAN SAJA
    return render_template("mhs/ambil_matkul.html", data_mhs = data_mhs, mata_kuliah = daftar_matkul)
  else:
    return redirect(url_for('login'))

# LAMAN DAFTAR MATA KULIAH YANG DIAMBIL OLEH MAHASISWA
@app.route('/mhs/<npm>/mata-kuliah-terambil')
def matkul_terambil(npm):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})

    # AMBIL NAMA MATA KULIAH TERAMBIL MAHASISWA
    if ("Mata kuliah" in col_mhs.find_one({"_id" : npm})) is True :
      document = col_mhs.find_one({"_id" : npm})
      document = document['Mata kuliah'].keys()
      return render_template("mhs/matkul_terambil.html", data_mhs = data_mhs, matkul_terambil= document)
    else:
      return render_template("mhs/matkul_terambil.html", data_mhs = data_mhs)
  else:
    return redirect(url_for('login'))

# LAMAN TIAP MATA KULIAH YANG DIAMBIL OLEH MAHASISWA
@app.route('/mhs/<npm>/<matkul>')
def mata_kuliah_mhs(npm, matkul):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})
    return render_template("mhs/mata_kuliah.html", data_mhs = data_mhs, mata_kul = matkul)
  else:
    return redirect(url_for('login'))

# UNTUK MENGHAPUS MATA KULIAH YANG DIAMBIL OLEH MAHASISWA
@app.route('/mhs/<npm>/<matkul>/hapus')
def hapus_mata_kuliah_mhs(npm, matkul):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})
    
    # PROSES PENGHAPUSAN
    del data_mhs['Mata kuliah'][matkul]
    col_mhs.update_one({'_id' : npm}, {"$set" : data_mhs})

    return redirect(url_for('matkul_terambil', npm = data_mhs['_id']))
  else:
    return redirect(url_for('login'))

# UNTUK BELAJAR DARING TIAP MAHASISWA
@app.route('/mhs/<npm>/<matkul>/materi_tugas/<pekan>', methods=['POST', 'GET'])
def kerjakan_tugas(npm, matkul, pekan):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})

    # UNTUK MENDAPATKAN NAMA FILES, NRP, FILES TUGAS TERKUMPUL
    files, nrp = [ i.name for i in storage.list_files() if matkul in i.name and "Materi/Pekan "+pekan in i.name ], [ i.name for i in storage.list_files() if matkul in i.name]
    tugas_terkumpul = [ i.name.split('/')[5] for i in storage.list_files() if data_mhs['_id'] and matkul+ '/Tugas Terkumpul/Pekan ' + pekan in i.name ]
    
    # NILAI DEFAULT DARI MASING-MASING VARIABEL
    nrp, video, pdf, a = nrp[0].split('/')[1], '', '', ''

    # UNTUK MENGAMBIL NILAI/TUGAS YANG DIBERIKAN OLEH DOSEN MELALUI MONGODB
    try:
      isian = list(col_dosen.find_one({'_id': nrp})['Mata kuliah'][matkul]['Pekan '+pekan].values())
    except:
      isian = ['', '', '', "0:0", '']

    # JIKA TERDAPAT FILES MATERI YANG TELAH DIUNGGAH DOSEN MAKA FILES TERSEBUT DAPAT DIAKSES OLEH MAHASISWA
    if files != []:
      if "dokumen.pdf" in files[0]:
        pdf = storage.child(files[0]).get_url(None)
      if "video.mp4" in files[0] or "video.mp4" in files[1]:
        video = storage.child(files[1]).get_url(None)

    # JIKA MAHASISWA SUDAH MENGUMPULKAN TUGAS SEBELUMNYA MAKA URL UNTUK MENGUNDUH TUGAS TERSEBUT DAPAT BEKERJA
    if tugas_terkumpul != []:
      a = storage.child(data_mhs['prodi']+'/'+nrp+'/'+matkul+'/Tugas Terkumpul/Pekan '+pekan+'/'+data_mhs['_id']+'-'+data_mhs['nama']+'.zip').get_url(None)

    # PROSES PENGUNGGAHAN TUGAS MAHASISWA
    if request.method == "POST":
      storage.child(data_mhs['prodi']+'/'+nrp+'/'+matkul+'/Tugas Terkumpul/Pekan '+pekan+'/'+data_mhs['_id']+'-'+data_mhs['nama']+'.zip').put(request.files['tugas_mhs'])

      dedlen = col_dosen.find_one({"_id" : nrp})['Mata kuliah'][matkul]['Pekan '+pekan]
      dedlen = datetime.strptime(dedlen['Tanggal batas pengumpulan']+' '+dedlen['Pukul batas pengumpulan'], '%Y-%m-%d %H:%M')
      waktu_sisa = dedlen-datetime.now()
      
      if waktu_sisa > timedelta(0):
        pesan_mhs = "Anda telah mengumpulkan tugas "+matkul+" untuk pertemuan pekan ke "+pekan+" dan tidak melebihi batas waktu yang ditentukan.\n\nSisa waktu anda adalah "+str(waktu_sisa)
        pesan_dosen = "Mahasiswa dengan NPM "+data_mhs['_id']+" telah mengumpulkan tugas mata kuliah "+matkul+" untuk pertemuan/pekan ke "+pekan+" tanpa terlambat/tepat waktu."
      else:
        pesan_mhs = "Anda telah mengumpulkan tugas "+matkul+" untuk pertemuan pekan ke "+pekan+" namun melebihi batas waktu yang ditentukan.\n\nSelisih waktu pengumpulan anda dengan batas waktunya adalah "+str(waktu_sisa)
        pesan_dosen = "Mahasiswa dengan NPM "+data_mhs['_id']+" telah mengumpulkan tugas mata kuliah "+matkul+" untuk pertemuan/pekan ke "+pekan+" dengan keterlambatan "+str(waktu_sisa)

      # KIRIM EMAIL PEMERITAHUAN KE MAHASISWA DAN DOSEN
      kirm_email("Pengiriman tugas berhasil!", '17081010068@student.upnjatim.ac.id', [data_mhs['email']], pesan_mhs)
      kirm_email("Tugas mahasiswa " + data_mhs['_id'], '17081010068@student.upnjatim.ac.id', [col_dosen.find_one({"_id" : nrp})['email']], pesan_dosen)

      return redirect(url_for('kerjakan_tugas', npm = data_mhs['_id'], matkul= matkul, pekan=pekan))

    return render_template("mhs/materi_tugas.html", data_mhs = data_mhs, pekan = pekan, url_video = video, url_pdf = pdf, nrp = nrp, tugas = isian, matkul = matkul, unggahan = a)
  else:
    return redirect(url_for('login'))

# UNTUK MENGHAPUS TUGAS YANG DIKIRIM OLEH MAHASISWA ITU SENDIRI
@app.route('/mhs/<npm>/<matkul>/hapus_tugas/<nrp>/<pekan>')
def hapus_tugas_mhs(npm, nrp, matkul, pekan):
  if "akun" in session:
    if nrp == 'kosong':
      return redirect(url_for('kerjakan_tugas', npm = npm, matkul = matkul, pekan = pekan))
    else:
      data_mhs = col_mhs.find_one({'_id' : npm})
      # PROSES PENGHAPUSAN FILE
      storage.delete(data_mhs['prodi']+'/'+nrp+'/'+matkul+'/Tugas Terkumpul/Pekan '+pekan+'/'+data_mhs['_id']+'-'+data_mhs['nama']+'.zip')
    
    return redirect(url_for('kerjakan_tugas', npm = npm, matkul = matkul, pekan = pekan))
  else:
    render_template("auth/login.html", pesan = "Anda harus masuk terlebih dahulu")

# UNTUK SEKADAR MELIHAT NILAI-NILAI MATA KULIAH PADA MASING2 MHS
@app.route('/mhs/<npm>/nilai-mata-kuliah')
def nilai_matkul(npm):
  if "akun" in session:
    data_mhs = col_mhs.find_one({"_id" : npm})
    return render_template("mhs/nilai_matkul.html",data_mhs = data_mhs)
  else:
    return redirect(url_for('login'))

# EDIT All
@app.route('/edit/<peran>/<unik>', methods=["POST", "GET"])
def edit_dosen_mhs(peran, unik):
  if "akun" in session and request.method == "POST":
    # EDIT DATA DOSEN
    if "@student.upnjatim" not in peran:
      col_dosen.update_one({"_id" : unik},
                           {"$set" : {"email" : request.form['email'],
                                      "sandi" : request.form['sandi']}})
      
      return redirect(url_for('dosen', nrp = request.form['id']))

    # EDIT AKUN MAHASISWA
    elif "@student.upnjatim" in peran:
      col_mhs.update_one({"_id" : unik},
                         {"$set" : {"email" : request.form['email'],
                                    "sandi" : request.form['sandi']}})
                                    
      return redirect(url_for('mahasiswa', npm = request.form['id']))
    pass
  else:
    return redirect(url_for('login'))

# UNTUK LOG OUT
@app.route('/keluar')
def keluar():
  if 'akun' in session :
    session.pop('akun')
    return redirect('/')
  else:
    return redirect('/')

# APABILA MENEMUKAN ROUTING URL YANG TIDAK SESUAI DENGAN KETENTUAN FIK-OCW
@app.errorhandler(404)
def page_not_found(e):
  return render_template('auth/404.html'), 404
