#!/build/bin/bash

clear
echo "=================================================="
echo "           BOTWATEL AUTOMATED LAUNCHER            "
echo "=================================================="
echo ""

# 1. PENGECEKAN DEPENDENSI NODE.JS
echo "[Check] Memeriksa modul WhatsApp (Node.js)..."
if [ ! -d "whatsappProd/node_modules" ]; then
    echo "[!] Folder node_modules tidak ditemukan."
    echo "[⚙️] Menjalankan 'npm install' otomatis untuk layanan WhatsApp..."
    cd whatsappProd && npm install && cd ..
    echo "[✓] Instalasi dependensi Node.js selesai!"
else
    echo "[✓] Modul WhatsApp sudah siap."
fi
echo ""

# 2. PENGECEKAN VIRTUAL ENVIRONMENT (VENV) PYTHON
echo "[Check] Memeriksa Virtual Environment Python (venv)..."
if [ ! -d "venv" ]; then
    echo "[!] Folder venv tidak ditemukan."
    echo "[⚙️] Membuat virtual environment baru..."
    python3 -m venv venv
    echo "[⚙️] Mengaktifkan venv dan menginstal library dari requirements.txt..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "[✓] Pembuatan venv dan instalasi library Python selesai!"
else
    echo "[✓] Virtual environment Python sudah siap."
fi

echo ""
echo "=================================================="
echo "              MENYALAKAN BOTWATEL                 "
echo "=================================================="
echo ""

# 3. MENYALAKAN KEDUA TERMINAL SECARA TERPISAH
# Menggunakan AppleScript jika di Mac, atau terminal bawaan jika di Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Khusus macOS: Membuka 2 jendela Terminal baru
    echo "[1/2] Menyalakan WhatsApp Server di jendela baru..."
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/whatsappProd && node server.js"'
    
    echo "[2/2] Mengaktifkan Venv dan Telegram Engine di jendela baru..."
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && python3 app.py"'
else
    # Khusus Linux (Menggunakan x-terminal-emulator atau gnome-terminal)
    echo "[1/2] Menyalakan WhatsApp Server di jendela baru..."
    x-terminal-emulator -e "bash -c 'cd whatsappProd && node server.js; exec bash'" &
    
    echo "[2/2] Mengaktifkan Venv dan Telegram Engine di jendela baru..."
    x-terminal-emulator -e "bash -c 'source venv/bin/activate && python3 app.py; exec bash'" &
fi

echo ""
echo "=================================================="
echo "🎉 Sukses! Kedua layanan telah berjalan di luar."
echo "Anda bisa menutup atau memakai terminal VSCode ini."
echo "=================================================="