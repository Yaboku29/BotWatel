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
5. [🔍 Cara Mendapatkan ID Target](#-cara-mendapatkan-id-target-telegram--whatsapp)
   - [1. Mencari ID Chat Telegram](#1-mendapatkan-id-telegram-dm-group-channel)
   - [2. Mencari ID Chat & Jenis Metadata WhatsApp](#2-mendapatkan-id-whatsapp-group--community-announcement)
6. [🔌 REST API Reference (Node.js Service)](#-rest-api-reference-nodejs-service)
7. [🔍 Penanganan Masalah Sesi (Troubleshooting)](#-penanganan-masalah-sesi-troubleshooting)
8. [🗺️ Roadmap Pengembangan](#️-roadmap-pengembangan)

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
├── .env                    # File konfigurasi kredensial & environment variable
├── app.py                  # Entry point utama aplikasi Python
├── config.py               # Pengelola konfigurasi & pemetaan variabel .env
├── requirements.txt        # Daftar dependensi library Python
├── database/               # Folder penyimpanan SQLite database (botwatel.db)
├── downloads/              # Folder penyimpanan media dari Telegram (diatur otomatis)
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

Buat sebuah file baru bernama `.env` di root folder utama proyek `BotWatel/`, lalu sesuaikan nilainya:

```env
# ==========================================
# TELEGRAM CREDENTIALS (my.telegram.org)
# ==========================================
API_ID=12345678
API_HASH=abcdef0123456789abcdef0123456789

# TARGET CHATS (Pisahkan dengan koma jika multi-chat, kosongkan/DM otomatis masuk)
TELEGRAM_TARGET_CHATS=123456789,-100123456789

# ==========================================
# WHATSAPP API & TARGET
# ==========================================
WA_API_URL=http://localhost:3000
WA_TARGET_NUMBER=628123456789
WA_COMMUNITY_ANNOUNCEMENT_NUMBER=628123456789-1600000000@g.us

# ==========================================
# DATABASE & SYSTEM LOG
# ==========================================
DATABASE_PATH=database/botwatel.db
LOG_LEVEL=INFO

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

---

## 🔍 Cara Mendapatkan ID Target (Telegram dan Whatsapp)

Aplikasi ini memfilter pesan berdasarkan Chat ID yang didaftarkan pada file `.env`. Jika Anda bingung atau belum tahu berapa ID dari Group atau Channel target Anda, proyek ini menyediakan skrip pembantu di dalam folder `tests/utils/`.

### Langkah Mencari ID Telegram:
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

## 🗺️ Roadmap Pengembangan

* [x] Login Telegram Userbot (Telethon)
* [x] Listener & Filter Chat ID Telegram
* [x] Auto-Download Media Telegram (Absolute Path & Sanitized Folder)
* [x] Login WhatsApp Userbot (Baileys dengan Auth File State)
* [x] Node.js REST API Server & Integrasi Multi-language (Python ↔ Node.js)
* [x] Modular Message Pipeline Arsitektur
* [x] Realtime Auto Translation (deep-translator)
* [x] Implementasi Database SQLite nyata pada `database_service`
* [ ] Pengaktifan Modul `telegram_formatter` secara menyeluruh pada alur WhatsApp
* [ ] Sinkronisasi Dua Arah Penuh (WhatsApp ↔ Telegram Bridge)

### 🔍 Penanganan Masalah Sesi (Troubleshooting)
Jika saat menjalankan `node server.js` Anda mendapati pesan error koneksi terputus mendadak atau sesi kedaluwarsa (Error 428 / 401), Anda dapat memicu ulang pemuatan QR Code baru dengan cara:
1. Matikan proses terminal Node.js (`Ctrl + C`).
2. Hapus folder `sessions/` yang berada di dalam folder proyek Anda.
3. Jalankan kembali `node server.js`.