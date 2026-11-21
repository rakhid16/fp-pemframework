# FIK Open Courseware

FIK Open Courseware (FIK-OCW) adalah platform pembelajaran daring untuk mahasiswa Fakultas Ilmu Komputer, Universitas Pembangunan Nasional "Veteran" Jawa Timur.

Platform ini menyediakan materi dalam bentuk PDF dan video, pengumpulan tugas, pemberitahuan melalui email, serta pencatatan nilai.

## Teknologi

- Flask sebagai framework backend
- MongoDB dan PyMongo sebagai database
- Firebase Storage dan Pyrebase sebagai penyimpanan file
- Flask-Mail untuk pengiriman email
- Bootstrap untuk antarmuka
- Gunicorn untuk deployment

## Peran Pengguna

### Pengunjung

- Melihat landing page
- Masuk ke aplikasi
- Mengakses halaman lupa sandi
- Mengirim pesan kepada tim pengembang

### Admin

- Mengelola akun dosen dan mahasiswa
- Melihat, menambah, mengubah, dan menghapus data akun

### Dosen

- Mengelola mata kuliah
- Menambah, mengubah, dan menghapus materi serta tugas
- Melihat tugas yang dikumpulkan mahasiswa
- Mengelola nilai mahasiswa

### Mahasiswa

- Melihat dan mengambil mata kuliah
- Mengakses materi per pertemuan
- Mengumpulkan dan menghapus tugas
- Melihat nilai mata kuliah

## Menjalankan Secara Lokal

1. Kloning repositori dan masuk ke direktori proyek:

   ```bash
   git clone https://github.com/rakhid16/fp-pemframework.git
   cd fp-pemframework
   ```

2. Instal dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:

   ```bash
   python main.py
   ```

4. Buka `http://127.0.0.1:5000/` pada browser.

Hentikan server dengan menekan `Ctrl+C`.

## Konfigurasi

Konfigurasi MongoDB, Firebase, dan Flask-Mail perlu disediakan sendiri pada `main.py` serta `firebase_key.json`. Kredensial tidak disertakan dalam repositori demi keamanan.

Tanpa konfigurasi yang valid, koneksi database, penyimpanan file, dan pengiriman email tidak dapat digunakan.

## Kontribusi

Fork repositori ini, buat perubahan pada cabang terpisah, lalu ajukan pull request.

## Lisensi

[Creative Commons Zero v1.0 Universal](LICENSE)

## Pengembang

- [Maulana Idris](https://github.com/maulidr)
- [Fitri Aulia Y P](https://github.com/fitriaulia)
- [Rakhman Wahid](https://github.com/rakhid16)
- [Amir Fanani](https://github.com/amirfanani)
