# :computer: FIK <i>Open Courseware</i>

<p align="right">
بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم 
</p>

<p align="justify">
&emsp;&emsp;&emsp;FIK <i>Open Courseware</i> (FIK-OCW) adalah sebuah <i>platform</i> belajar bagi Mahasiswa Fakultas Ilmu Komputer UPN "VETERAN" Jawa Timur. <i>Platform</i> ini mengadopsi dari <i>platform</i> belajar lain seperti Dicoding, Codepolitan dan sebagainya. <i>Platform</i> ini mendukung media belajar seperti pemberian materi dari dosen dalam bentuk unduh PDF maupun video pembelajaran. Selain itu, <i>Platform</i> ini dapat menampung tugas dari mahasiswa FIK UPNVJATIM yang akan mengumpulkan tugasnya ke dosen.
</p>

<p align="center">
  <img src="https://i.imgur.com/kmJGkFX.png" width=400px height=300px>
</p>

<p align="justify">
&emsp;&emsp;&emsp;Web ini menggunakan Flask sebagai <i>Backend Framework</i> yang ditulis dalam bahasa pemrograman Python, MongoDB sebagai <i>database</i>, dan Firebase sebagai <i>storage</i>. Ada 3 tipe <i>user</i> dalam program ini, yaitu Admin, Dosen, dan Mahasiswa. Fitur untuk ketiga tipe pengguna tersebut akan dijelaskan lebih lanjut. Berikut ini adalah ilustrasi hubungan antar <i>tools</i> yang kami gunakan dalam membangun FIK-OCW :
</p>

<p align="center">
  <img src="https://i.imgur.com/mpRwEEU.jpg">
</p>
Keterangan tiap tools :<br>
1. <i>Frontend</i> kami menggunakan <a href="https://getbootstrap.com/">Bootstrap</a> yang beberapa .css dan .js nya ada yang kami buat/kustom sendiri.<br>
2. Layanan email kami menggunakan <a href="https://pythonhosted.org/Flask-Mail/">Flask Mail</a> yang langsung terintegrasi dengan Google Mail.<br>
3. Kami menggunakan <a href="https://palletsprojects.com/p/flask/">Flask</a> sebagai framework utama.<br>
4. Untuk mengakses <i>database</i> yang tersimpan pada Cloud MongoDB server kami menggunakan <a href="https://pymongo.readthedocs.io/en/stable/">PyMongo</a>.<br>
5. Untuk mengakses <i>cloud storage</i> yang berada pada Firebase server kami menggunakan <a href="https://github.com/thisbejim/Pyrebase">Pyrebase</a>.<br>
6. Website ini dihosting pada Heroku yang memanfaatkan <a href="https://gunicorn.org/">Gunicorn</a> sebagai server <i>deployment</i>'nya Flask.<br><br>

## :memo: Panduan memulai
Silahkan ketik perintah berikut ini secara berurutan pada terminal(Linux/Mac) atau CMD(Windows) kalian jika ingin mencoba untuk menjalankannya pada <i>localhost</i> masing-masing :
### 1 <i>pull</i> atau <i>clone</i> repositori ini

```
git clone https://github.com/rakhid16/fp-pemframework.git
cd fp-pemframework
```
atau
```
mkdir fik_ocw
cd fik_ocw
git init
git pull https://github.com/rakhid16/fp-pemframework.git
```

### 2 Instal <i>libraries</i>/<i>frameworks</i>
```
pip3 install -r requirements.txt
```
atau
```
pip install -r requirements.txt
```

### 3 Jalankan di localhost
```
python3 main.py
```
atau
```
python main.py
```

### 4 Akses http://127.0.0.1:5000/
<i>Landing page</i> FIK-OCW :<br><br>
![permalink setting demo](https://i.ibb.co/k09ySM3/Screenshot-from-2020-05-14-22-20-51.png)
Ketik <b>ctrl + c</b> pada terminal/CMD kalian jika ingin mematikan server flask'nya.<br>
<p align="justify">
<b><i>DISCLAIMER</i></b> : Karena memperhatikan faktor keamanan pada <i>cloud storage/database</i>, kami tidak mencantumkan <i>API keys</i> dari Firebase dan MongoDB serta akun yang digunakan untuk menggunakan flask mail. Jadi merupakan hal yang wajar apabila jika menjalankan program ini secara <i>default</i> setelah kalian melakukan <i>pull</i>/<i>clone</i> repositori ini akan terjadi kegagalan.
<p>

## :handshake: Kontribusi
Silahkan <i>fork</i> repositori ini terlebih dahulu setelah itu kalian bebas mengembangkan proyek ini.

## :paperclip: Lisensi
<a href="https://github.com/Rakhid16/fp-pemframework/blob/master/LICENSE">Creative Commons Zero v1.0 Universal</a>

## :wink: Pengembang proyek
<i>Jazakumullah khairan</i> kepada :<br>
:man: <a href="https://github.com/maulidr">Maulana Idris</a><br>
:smile: <a href="https://github.com/fitriaulia">Fitri Aulia Y P</a><br>
:boy: <a href="https://github.com/rakhid16">Rakhman Wahid</a><br>
:man: <a href="https://github.com/amirfanani">Amir Fanani</a><br>
Atas kerja sama dan bantuan'nya selama pengerjaan proyek ini!

## :sunglasses: Fitur Aplikasi
<b>1. Pengunjung Umum</b>
- [x] <i>Landing Page</i>
- [x] <i>Login</i>
- [x] Akses laman lupa sandi
- [x] Kirim pesan kepada tim pengembang

<b>2. Admin</b>
- [x] Ubah sandi akun
- [x] Lihat data dosen dan mahasiswa
- [x] Hapus data dosen dan mahasiswa
- [x] Edit data dosen dan mahasiswa
- [x] Tambah akun baru untuk dosen dan mahasiswa
- [x] Keluar <i>dashboard</i>

<b>3. Dosen</b>
- [x] Ubah sandi akun
- [x] Buat dan lihat mata kuliah yang diampu
- [x] Hapus mata kuliah yang diampu
- [x] Tambahkan materi berupa video (.mp4) dan .pdf ke setiap matkul per-pekan/pertemuan
- [x] Tambahkan tugas untuk mahasiswa ke setiap matkul per-pekan
- [x] Hapus mata materi maupun tugas pada setiap matkul per-pekan
- [x] Edit mata materi maupun tugas pada setiap matkul per-pekan
- [x] Mendapatkan email pemberitahuan setelah ada mahasiswa yang mengunggah tugas (telat/tepat waktu)
- [x] Mengunduh tugas yang dikumpulkan oleh mahasiswa pada setiap matkul per-pekan
- [x] Menambah dan mengedit nilai mahasiswa pada setiap matkul per-pekan
- [x] Keluar <i>dashboard</i>

<b>4. Mahasiswa</b>
- [x] Ubah sandi akun
- [x] Lihat/ambil mata kuliah yang tersedia
- [x] Lihat/hapus mata kuliah yang telah diambil
- [x] Belajar onlie melalui video <i>streaming</i> yang disediakan oleh dosen pada setiap matkul per-pekan/pertemuan
- [x] Mengunduh materi berupa .pdf yang telah disediakan dosen pada setiap matkul per-pekan/pertemuan
- [x] Mengunggah tugas yang diberikan oleh dosen dalam bentuk .zip pada setiap matkul per-pekan/pertemuan
- [x] Menghapus tugas yang telah terunggah
- [x] Melihat nilai setiap matkul per-pekan/pertemuan
- [x] Mendapatkan email pemberitahuan setelah mengunggah tugas (telat/tepat waktu)
- [x] Keluar <i>dashboard</i>

## :pushpin: Demo Aplikasi
<a href="http://fik-ocw.herokuapp.com/" target=blank>KLIK!</a>
