const { default: makeWASocket, useMultiFileAuthState } = require("@whiskeysockets/baileys");
const P = require("pino");
const fs = require("fs");
const path = require("path");

// Mengambil argumen pencarian nama jika ada (contoh: node get_wa_ids.js "Nama Grup")
const searchQuery = process.argv[2] ? process.argv[2].toLowerCase() : null;

async function main() {
    // Membaca sesi login yang sudah ada di folder whatsappProd/sessions
    const sessionPath = path.join(__dirname, "../../whatsappProd/sessions");
    
    if (!fs.existsSync(sessionPath)) {
        console.log("❌ Sesi WhatsApp tidak ditemukan! Silakan jalankan 'node server.js' di folder whatsappProd terlebih dahulu untuk scan QR.");
        process.exit(1);
    }

    const { state } = await useMultiFileAuthState(sessionPath);

    const sock = makeWASocket({
        auth: state,
        logger: P({ level: "silent" })
    });

    sock.ev.on("connection.update", async (update) => {
        const { connection } = update;
        
        if (connection === "open") {
            console.log("\n==================================================");
            console.log("        BOTWATEL - WHATSAPP CHAT ID FETCHERS      ");
            console.log("==================================================");
            if (searchQuery) {
                console.log(`🔍 Memfilter grup dengan kata kunci: "${process.argv[2]}"\n`);
            } else {
                console.log("📋 Menampilkan semua daftar grup yang Anda ikuti:\n");
            }

            try {
                // Mengambil seluruh data grup dari memory Baileys
                const groups = await sock.groupFetchAllParticipating();
                let foundCount = 0;

                for (const jid in groups) {
                    const group = groups[jid];
                    const groupName = group.subject;

                    // Fitur pencarian berdasarkan nama
                    if (searchQuery && !groupName.toLowerCase().includes(searchQuery)) {
                        continue;
                    }

                    foundCount++;

                    // Menentukan tipe metadata grup berdasarkan flag Baileys
                    let metadataType = "👥 Group Chat (Grup Biasa)";
                    if (group.isCommunityAnnounce) {
                        metadataType = "📢 Announcement Group (Grup Pengumuman Komunitas)";
                    } else if (group.linkedParent) {
                        metadataType = "🏛️ Community Sub-Group (Grup di dalam Komunitas)";
                    }

                    console.log(`Nama Grup : ${groupName}`);
                    console.log(`Chat ID   : ${jid}`);
                    console.log(`Metadata  : ${metadataType}`);
                    console.log(`Total Member: ${group.participants.length}`);
                    console.log("-" * 50);
                }

                if (foundCount === 0) {
                    console.log("⚠️ Tidak ada grup yang cocok dengan pencarian Anda.");
                }

            } catch (err) {
                console.error("❌ Gagal mengambil data grup:", err.message);
            }

            // Tutup koneksi setelah selesai membaca data
            sock.logout();
            process.exit(0);
        }
    });
}

main();