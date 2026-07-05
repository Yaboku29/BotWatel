# BotWatel 📨

BotWatel adalah aplikasi bridge (penghubung) otomatis antara **Telegram** dan **WhatsApp** yang memanfaatkan akun pribadi (Userbot). Proyek ini bekerja secara bebas tanpa memerlukan Bot API resmi dari kedua platform tersebut.

Saat ini, sistem diimplementasikan satu arah (**Telegram → WhatsApp**) untuk meneruskan berbagai pesan secara realtime.

---
## 📌 Daftar Isi

1. [✨ Fitur Utama](#-fitur-utama)
2. [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
3. [📂 Struktur Properti & Folder](#-struktur-properti--folder)
4. [🚀 Panduan Instalasi & Penggunaan](#-panduan-instalasi--penggunaan)
   - [Langkah 1: Kloning Repositori](#1-kloning-repositori)
   - [Langkah 2: Inisialisasi Environment Awal](#2-konfigurasi-environment-env)
   - [Langkah 3: Setup & Login WhatsApp (Node.js)](#3-setup-layanan-whatsapp-nodejs)
   - [Langkah 4: Setup & Login Telegram (Python)](#4-setup-layanan-telegram--core-python)
5. [🔍 Cara Mendapatkan ID Target](#-cara-mendapatkan-id-target-telegram-dan-whatsapp)
6. [🔌 REST API Reference (Node.js Service)](#-rest-api-reference-nodejs-service)
7. [🔍 Penanganan Masalah Sesi (Troubleshooting)](#-penanganan-masalah-sesi-troubleshooting)
8. [📊 Cara Membaca Log & Monitoring Sistem](#-cara-membaca-log--monitoring-sistem)
9. [🗺️ Roadmap Pengembangan](#️-roadmap-pengembangan)

---

## ✨ Fitur Utama

- **Userbot Engine:** Berjalan menggunakan akun Telegram pribadi (via Telethon) dan WhatsApp pribadi (via Baileys).
- **Realtime Listener:** Memonitor pesan masuk dari DM (Private Chat), Group, maupun Channel Telegram secara instan.
- **Target Filtering:** Memfilter sumber pesan masuk berdasarkan Chat ID Telegram yang dikonfigurasi pada file `.env`.
- **Auto-Download Media:** Mengunduh media Telegram otomatis (Foto, Video, Dokumen, Voice (*SOON*), Audio (*SOON*), Sticker (*SOON*), GIF (*SOON*)) dan menyimpannya ke folder lokal.
- **Pipeline Architecture:** Menggunakan pola desain modular (*Chain of Responsibility*) sehingga mempermudah penambahan layanan baru (Logger, DB, Translator, Formatter).
- **Realtime Translation:** Mendeteksi bahasa asing otomatis dan menerjemahkannya ke bahasa Inggris via Google Translate sebelum dikirim ke WhatsApp.
- **Media Caption:** Mempertahankan teks caption asli pada media (foto/video) saat diteruskan.
- **Non-Blocking REST API:** Mengirim pesan via HTTP POST ke server Node.js dengan sistem antrean latar belakang (*queued*) agar performa Python tetap responsif.
- **Smart Album Detection:** Mendeteksi pengiriman album media beruntun dari Telegram secara pintar menggunakan SQLite, memastikan hanya gambar/video pertama yang membawa caption laporan panjang, sedangkan media berikutnya masuk sebagai kolase bersih di WhatsApp.
- **Auto-Clean Media Storage:** Menghapus file media fisik lokal dari folder `downloads/` secara instan dan otomatis sesaat setelah berhasil diteruskan ke Node.js untuk menghemat penyimpanan disk.
- **Dynamic Document Mimetype:** Mampu mengenali ekstensi asli dokumen (seperti berkas `.png` atau `.zip` yang dikirim sebagai berkas uncompressed) sehingga tidak rusak saat diunduh di WhatsApp.
- **Isolated Log System:** Mengalihkan seluruh log jaringan dan sistem internal yang ramai (Telethon & Baileys) ke dalam file terpisah di folder `logs/` agar layar terminal tetap bersih dan informatif.
- **GUI Log Dashboard Integration:** Mendukung pelacakan status pesan (SUCCESS/FAILED) beserta alasan error secara visual menggunakan ekstensi SQLite Viewer, mempermudah pemantauan tanpa perlu membaca teks terminal yang menumpuk.

---

## 🏗️ Arsitektur Sistem
```
            Telegram Chat
                  │
                  ▼
          Telethon (Python)
                  │ (HTTP POST JSON)
                  ▼
      Express API + Baileys (Node.js)
                  │
                  ▼
            WhatsApp Chat
```


---

## 📂 Struktur Properti & Folder


```

BotWatel/
├── .env.example            # Template cetakan konfigurasi environment (Salin menjadi .env)
├── app.py                  # Entry point utama aplikasi Python
├── config.py               # Pengelola konfigurasi & pemetaan variabel .env
├── run.bat                 # Skrip otomatisasi peluncur (Launcher) sekali klik
├── requirements.txt        # Daftar dependensi library Python
├── database/               # Folder penyimpanan SQLite database (botwatel.db)
├── downloads/              # Folder penyimpanan media dari Telegram (diatur otomatis)
├── logs/                   # Folder Log Terisolasi (Otomatis dibuat oleh sistem)
│   ├── telegram.log        # Berisi log internal detail jaringan Telethon (Python)
│   └── whatsapp.log        # Berisi log internal detail koneksi Baileys (Node.js)
├── formatter/              # Modul penyusun tampilan teks laporan pesan
│   └── telegram_formatter.py
├── models/                 # Definisi struktur objek data (Dataclasses Python)
│   ├── message.py
│   └── outgoing_message.py
├── pipeline/               # Arsitektur orkestrasi berantai pemrosesan pesan
│   └── pipeline.py
├── services/               # Layanan pipeline (Logger, DB, Translator, WhatsApp Sender)
│   ├── database.py
│   ├── logger.py
│   ├── translator.py
│   └── whatsapp.py
├── telegramProd/           # Modul Telegram Engine (Client, Listener, Downloader, Handler)
│   ├── client.py
│   ├── downloader.py
│   ├── listener.py
│   └── message_handler.py
├── tests/                  # Folder Pengujian Proyek
│   ├── utils/
│   │   └── get_ids.py      # Skrip pembantu untuk mencari ID Telegram (Group/Channel/DM)
│   │   └── get_wa_ids.js   # Skrip pembantu mencari ID WhatsApp & Tipe Metadata (Node.js)
│   ├── test_api.py         # Skrip pengujian REST API
│   └── test_wa.py          # Skrip pengujian fungsionalitas WhatsApp
└── whatsappProd/           # Modul WhatsApp (Server Node.js & REST API Driver)
    ├── client.js
    ├── package.json
    ├── sender.py
    └── server.js

```

### Aturan Penyimpanan Media
Media yang diunduh dari Telegram akan otomatis tersimpan dengan struktur folder absolut berbasis nama chat dan waktu:

```

downloads/
└── [Nama Chat]/
     └── [Tahun]/
          └── [Bulan]/
               └── [Tanggal]/
                    ├── photo.jpg
                    └── video.mp4

```

---

## 🚀 Panduan Instalasi & Penggunaan

Proyek ini membutuhkan pemahaman dasar mengenai penggunaan terminal/command prompt. Pastikan komputer Anda sudah terinstal **Python 3.10+** dan **Node.js 18+**.

### 1. Kloning Repositori
```bash
git clone [https://github.com/username/BotWatel.git](https://github.com/username/BotWatel.git)
cd BotWatel

```

### 2. Konfigurasi Environment (`.env`)

Untuk membuat `.env` cukup menyalin dari `.env.example`.
Bisa dengan duplicate dan rename menjadi `.env` atau dengan Terminal :

- **Linux/macOS**
```bash
cp .env.example .env
```

- **Windows Powershell**
```bash
copy .env.example .env
```

- **VSCode/File Explorer**: klik kanan pada file `env.example`, pilih Duplicate/Copy, lalu ganti namanya *(Rename)* menjadi `.env`.

#### 📌 Tips Tambahan: Pastikan `.env` Masuk `.gitignore`

Karena file `.env` yang asli akan berisi data rahasia akunmu, pastikan di dalam proyekmu sudah ada file bernama **`.gitignore`** di root folder yang berisi baris berikut:

```text
.env
database/botwatel.db
downloads/
whatsappProd/sessions/
__pycache__/
```

*Note: Jangan ubah isi `.env.example` dengan isi data yang krusial seperti API ataupun sejenisnya.

#### 🔑 Cara Mendapatkan API ID & API Hash Telegram

Untuk menghubungkan Userbot Python (Telethon) ke server Telegram, Anda memerlukan kredensial aplikasi resmi dari Telegram. Ikuti langkah mudah berikut:

1. Buka browser dan masuk ke situs resmi: **[https://my.telegram.org](https://my.telegram.org)**.
2. Masukkan nomor HP akun Telegram Anda (gunakan format internasional, misal: `+628xxxxxxxx`).
3. Telegram akan mengirimkan **kode verifikasi/OTP** langsung ke aplikasi Telegram Anda (bukan via SMS). Masukkan kode tersebut untuk login.
4. Setelah berhasil masuk, klik menu **"API development tools"**.
5. Isi formulir pembuatan aplikasi baru:
   - **App title:** Bebas (misal: `BotWatel Engine`)
   - **Short name:** Bebas (misal: `botwatel`)
   - Bagian URL atau deskripsi bisa Anda kosongi atau isi seadanya.
6. Klik **"Create application"**.
7. Anda akan melihat data **`App api_id`** (berupa angka) dan **`App api_hash`** (berupa kombinasi huruf & angka acak).
8. Salin kedua nilai tersebut, lalu tempelkan ke file `.env` Anda:
```env
   API_ID=12345678          # Ganti dengan api_id Anda
   API_HASH=abcdef123456... # Ganti dengan api_hash Anda
```

### 3. Setup Layanan WhatsApp (Node.js)

Buka terminal baru, masuk ke folder modul WhatsApp, pasang dependensi, lalu jalankan servernya:

```bash
cd whatsappProd
npm install
node server.js

```

*Catatan: Saat pertama kali dijalankan, terminal akan merender QR Code kecil. Buka WhatsApp HP Anda -> Perangkat Tertaut -> Scan QR tersebut. Sesi login akan disimpan secara permanen di dalam folder `sessions/`.*

### 4. Setup Layanan Telegram & Core (Python)

Buka terminal baru satu lagi (kembali ke root folder utama `BotWatel`), instal dependensi melalui file `requirements.txt`, lalu jalankan aplikasi utamanya:

```bash
pip install -r requirements.txt
python app.py

```

*Catatan: Pada peluncuran pertama, Telethon di terminal akan meminta Anda memasukkan nomor HP (gunakan format internasional, misal: +628xxx) dan memasukkan kode OTP resmi yang dikirimkan oleh sistem Telegram.*

## 🚀 Cara Menjalankan BotWatel (Windows OS)

Proyek ini telah dilengkapi dengan berkas otomatisasi peluncur (*launcher*) bernama `run.bat` di root folder. Fitur ini dirancang untuk mempermudah eksekusi ekosistem BotWatel tanpa perlu membuka banyak tab atau mengetik perintah terminal yang panjang secara manual.

### Langkah Cepat Menjalankan Aplikasi:

1. Buka Proyek BotWatel di VSCode atau juga bisa langsung di terminal:
```bash
[drive]:\...\BotWatel>
```
2. Jika sudah di VSCode bisa jalankan perintah berdasarkan OS Device Anda:
- Windows Powershell

```powershell
./run
```

- Terminal (macOS dan Linux)

```bash
cmod +x run.sh # Lakukan saat pertama kali menjalankan
/run.sh # untuk sehari-hari
```

#### 🧠 Apa yang Terjadi di Latar Belakang?

Begitu perintah peluncur (`./run` atau `./run.sh`) dieksekusi, skrip akan secara otomatis memeriksa kesiapan sistem, memecah proses, dan membuka **dua jendela terminal baru** di luar VSCode secara instan:

1. **Jendela 1 (`BotWatel - WhatsApp Service`):** 
   - **Windows:** Membuka jendela PowerShell baru.
   - **macOS/Linux:** Membuka jendela aplikasi Terminal bawaan sistem.
   - **Tugas:** Otomatis masuk ke folder `whatsappProd`, memeriksa folder `node_modules` (melakukan `npm install` jika belum ada), lalu menyalakan server Express API dan mengaktifkan REST API Node.js/Baileys.

2. **Jendela 2 (`BotWatel - Telegram Service`):** 
   - **Windows:** Membuka jendela PowerShell baru kedua.
   - **macOS/Linux:** Membuka jendela aplikasi Terminal bawaan sistem kedua.
   - **Tugas:** Otomatis memeriksa lingkungan Virtual Environment (membuat `venv` baru & menginstal library dari `requirements.txt` jika belum ada), mengaktifkan lingkungan `venv` tersebut, lalu mengeksekusi Core Engine Python/Telethon (`python app.py`).

---

## 🔍 Cara Mendapatkan ID Target (Telegram dan Whatsapp)

Aplikasi ini memfilter pesan berdasarkan Chat ID yang didaftarkan pada file `.env`. Jika Anda bingung atau belum tahu berapa ID dari Group atau Channel target Anda, proyek ini menyediakan skrip pembantu di dalam folder `tests/utils/`.

### Langkah Mencari ID Telegram & Whatsapp:

1. Pastikan Anda sudah melakukan setup dasar dan berhasil login Telegram pada pengujian pertama.

2. Jalankan perintah berikut di terminal root proyek Anda:

   ```bash
   python tests/utils/get_tele_ids.py
   ```

3. Skrip akan membaca 20 riwayat obrolan terbaru akun Anda dan mencetaknya dengan format

```
Nama Chat : Kelompok Belajar C#
Chat ID   : -100123456789
Jenis     : 👥 Group
```

4. Salin angka Chat ID tersebut(termasuk tanda minus `-` jika ada grup/channel) lalu tempelkan ke variabel `TELEGRAM_TARGET_CHATS` di file `.env` Anda. 

5. Untuk mencari atau mendapatkan ID Whatsapp (Group/Community Announcement), pastikan Anda sudah sukses melakukan scan QR Code pada server Node.js sebelumnya. Lalu jalankan salah satu perintah berikut:

- Melihat seluruh grup Anda
```bash
node tests/utils/get_wa_ids.js
```

- Mencari berdasarkan nama grup tertentu (*Case-Sensitive*)

```bash
node tests/utils/get_wa_ids.js "Nama Komunitas Anda"
```

6. Skrip akan menampilkan metadata tipe grup secara jelas seperti berikut

```
Nama Grup : Karyawan Sentosa
Chat ID   : 12036321234567890@g.us
Metadata  : 📢 Announcement Group (Grup Pengumuman Komunitas)
Total Member: 150
--------------------------------------------------
Nama Grup : Karyawan Sentosa
Chat ID   : 628123456789-160000000@g.us
Metadata  : 👥 Group Chat (Grup Biasa)
Total Member: 45
```

7. Jika Anda menginginkan pesan dikirimkan ke **ANNOUNCEMENT GROUP**, salin Chat ID yang memiliki `Metadata: 📢 Announcement Group (Grup Pengumuman Komunitas)` (biasanya yang berakhiran @g.us).
8. Tempelkan ID tersebut ke variabel `WA_COMMUNITY_ANNOUNCEMENT_NUMBER` pada file `.env` Anda agar bot bisa mengirim pesan tepat ke ruang pengumuman utama komunitas, bukan ke grup obrolan anggotanya. *Note : Pastikan Anda adalah Admin di Group Pengumumannya jika ingin Bot bisa mengirim pesan

## 🔌 REST API Reference (Node.js Service)

Server Node.js secara default berjalan di `http://localhost:3000` dan mengekspos endpoint HTTP yang ditembak oleh `sender.py` di sisi Python.

### Mengirim Pesan

* **Endpoint:** `POST /send`
* **Headers:** `Content-Type: application/json`

#### Contoh Payload Pesan Teks:

```json
{
  "number": "628123456789",
  "type": "text",
  "text": "Halo dari BotWatel!"
}

```

#### Contoh Payload Pesan Gambar (File Lokal Absolut):

```json
{
  "number": "628123456789",
  "type": "image",
  "path": "C:/BotWatel/downloads/Group_A/2026/07/03/photo.jpg",
  "caption": "Pesan gambar yang diteruskan dari Telegram"
}

```

#### Response (Non-blocking):

```json
{
  "success": true,
  "status": "queued"
}

```

---


### 🔍 Penanganan Masalah Sesi (Troubleshooting)
Jika saat menjalankan `node server.js` Anda mendapati pesan error koneksi terputus mendadak atau sesi kedaluwarsa (Error 428 / 401), Anda dapat memicu ulang pemuatan QR Code baru dengan cara:
1. Matikan proses terminal Node.js (`Ctrl + C`).
2. Hapus folder `sessions/` yang berada di dalam folder proyek Anda.
3. Jalankan kembali `node server.js`.

---

## 📊 Cara Membaca Log & Monitoring Sistem

Aplikasi ini dirancang dengan prinsip **Clean Terminal Output**. Seluruh log teknis yang berisik dari Telegram dan WhatsApp secara otomatis diisolasi ke latar belakang, sehingga terminal Anda hanya akan menampilkan status konfirmasi ringkas saat ada pesan yang berhasil diteruskan.

Jika Anda ingin melihat riwayat status pengiriman atau melacak error tertentu, Anda dapat melihatnya secara visual tanpa menggunakan terminal:

### 1. Monitoring via GUI SQLite (Sangat Direkomendasikan)
1. Instal ekstensi **SQLite Viewer** di VSCode Anda.
2. Buka folder proyek ini di VSCode, lalu klik berkas database `database/botwatel.db`.
3. Anda akan melihat tabel visual layaknya Excel yang memuat metadata pesan.
4. Perhatikan kolom `status` (`SUCCESS` / `FAILED`). Jika ada pesan yang gagal, detail penyebab masalahnya akan tertulis secara lengkap pada kolom `error_message`.

### 2. Melacak Error Teknis Koneksi (File Log)
Jika bot tidak merespons atau koneksi terputus, Anda bisa langsung membuka folder `logs/` untuk membaca jejak masalahnya secara mendalam:
* Lihat `logs/telegram.log` untuk masalah internal Telegram (misal: sesi habis atau pembatasan rate-limit).
* Lihat `logs/whatsapp.log` untuk masalah internal WhatsApp (misal: kegagalan *handshake* jaringan Baileys atau masalah autentikasi QR).

---

## 🗺️ Roadmap Pengembangan

* [x] Login Telegram Userbot (Telethon)
* [x] Listener & Filter Chat ID Telegram
* [x] Auto-Download Media Telegram (Absolute Path & Sanitized Folder)
* [x] Login WhatsApp Userbot (Baileys dengan Auth File State)
* [x] Node.js REST API Server & Integrasi Multi-language (Python ↔ Node.js)
* [x] Modular Message Pipeline Arsitektur
* [x] Realtime Auto Translation (deep-translator)
* [x] Implementasi Database SQLite nyata pada `database_service`
- [x] Sistem Logging Terisolasi (`logs/`) untuk Python & Node.js
- [x] Pencatatan detail error pengiriman ke dalam database SQLite (`error_message`)
- [x] Otomatisasi instalasi dependensi via Skrip Launcher Sekali Klik(`run.bat`)
- [ ] Pengaktifan Modul `telegram_formatter` secara menyeluruh pada alur WhatsApp
- [ ] Sinkronisasi Dua Arah Penuh (WhatsApp ↔ Telegram Bridge)