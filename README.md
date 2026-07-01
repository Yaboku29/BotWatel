# BotWatel

BotWatel adalah aplikasi Python yang menggunakan **Telethon** untuk memonitor pesan Telegram menggunakan akun pribadi, kemudian menyimpan media yang diterima ke dalam folder lokal. Proyek ini dirancang agar nantinya dapat dikembangkan menjadi **Telegram → WhatsApp Bridge**.

---

## Fitur

- Login menggunakan akun Telegram pribadi
- Menerima seluruh pesan baru secara realtime
- Menampilkan informasi pesan
  - Nama chat
  - Chat ID
  - Pengirim
  - Username
  - Message ID
  - Waktu
  - Jenis pesan
  - Isi pesan
- Mengunduh media secara otomatis
- Menyimpan media berdasarkan:
  - Nama chat
  - Tahun
  - Bulan
  - Tanggal

Contoh struktur folder hasil download:

downloads/
```
Nama Grup/
└── 2026/
└── 07/
└── 01/
├── photo.jpg
├── document.pdf
└── video.mp4
```

---

## Requirement

- Python 3.11+
- Telegram API ID
- Telegram API Hash

---

## Instalasi

### Clone repository

```bash
git clone https://github.com/username/BotWatel.git

cd BotWatel
```

---

### Buat Virtual Environment

Windows

```bash
python -m venv .venv
```

Aktifkan

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### Install dependency

```bash
pip install -r requirements.txt
```

---

## Membuat API Telegram

Masuk ke

https://my.telegram.org

Login menggunakan nomor Telegram.

Pilih

```
API Development Tools
```

Kemudian buat aplikasi baru.

Catat:

- API ID
- API Hash

---

## Konfigurasi

Buat file

```
.env
```

Isi dengan

```env
API_ID=12345678
API_HASH=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Menjalankan Program

```bash
python app.py
```

Saat pertama kali dijalankan akan diminta:

```
Phone Number
```

Masukkan nomor Telegram.

Setelah itu masukkan:

```
Login Code
```

Jika menggunakan Two-Step Verification:

```
Password
```

Setelah berhasil login akan muncul file:

```
watel.session
```

File ini digunakan agar tidak perlu login ulang setiap menjalankan program.

---

## Struktur Project

```
BotWatel/
│
├── app.py
├── .env
├── README.md
├── downloads/
│
└── telegramProd/
    ├── client.py
    ├── downloader.py
    ├── listener.py
```

---

## Output Contoh

```
============================================================

Chat Name : Belajar Python
Chat ID   : -1001234567890

Sender    : Rizky

Username  : @rizky

Message ID : 1234

Time       : 2026-07-01 20:30

Type       : Photo

TEXT

Halo semua

Saved File

downloads/
Belajar Python/
2026/
07/
01/
photo.jpg

============================================================
```

---

## Dependency

```
Telethon
python-dotenv
```

atau install menggunakan

```bash
pip install telethon python-dotenv
```

---

## Roadmap

- [x] Login menggunakan akun Telegram
- [x] Menerima pesan realtime
- [x] Download media
- [ ] Forward pesan ke WhatsApp
- [ ] Auto Reply WhatsApp
- [ ] Database SQLite
- [ ] Logging
- [ ] GUI Dashboard
- [ ] Docker Support