const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    Browsers
} = require("@whiskeysockets/baileys");

const P = require("pino");
const qrcode = require("qrcode-terminal");
const fs = require("fs");
const pathModule = require("path");

class WhatsAppClient {
    constructor() {
        this.sock = null;
        this.state = null;
        this.saveCreds = null;
        this.isReady = false;
    }

    async start() {
        const { state, saveCreds } =
            await useMultiFileAuthState("sessions");

        this.state = state;
        this.saveCreds = saveCreds;

        await this.createSocket();
    }

    async createSocket() {
        // 1️⃣ Tentukan path folder logs (naik 1 tingkat ke root project, lalu masuk folder logs)
        const logDir = pathModule.join(__dirname, "../logs");
        
        // 2️⃣ Pastikan folder logs sudah terbuat secara fisik
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 3️⃣ Buat stream write khusus pino untuk menulis seluruh log detail Baileys ke file whatsapp.log
        const fileLogger = P(
            { level: "debug" }, // Mengubah dari "silent" ke "debug" agar semua histori internal tercatat di file log
            fs.createWriteStream(pathModule.join(logDir, "whatsapp.log"), { flags: "a" }) // 'a' artinya append/menambah baris terus
        );

        this.sock = makeWASocket({
            auth: this.state,
            browser: Browsers.ubuntu("BotWatel"),
            logger: fileLogger // 4️⃣ Ganti pino bawaan dengan fileLogger kita
        });

        this.sock.ev.on("creds.update", this.saveCreds);
        this.sock.ev.on("connection.update", this.handleConnection.bind(this));
    }

    async handleConnection(update) {
        const { connection, qr, lastDisconnect } = update;

        if (qr) {
            qrcode.generate(qr, { small: true });
        }

        if (connection === "open") {
            console.log("WhatsApp Connected");
            this.isReady = true;
        }

        if (connection === "close") {
            this.isReady = false;

            const status =
                lastDisconnect?.error?.output?.statusCode;

            console.log("Disconnected:", status);

            if (status === DisconnectReason.restartRequired) {
                await this.createSocket();
            }
        }
    }

    async sendMessage({
        number,
        type = "text",
        text,
        path,
        caption
    }) {

        if (!this.sock || !this.isReady) {
            throw new Error("WhatsApp belum siap");
        }

        let jid;

        if (number.endsWith("@g.us")) {
            jid = number;
        } else {
            jid = `${number}@s.whatsapp.net`;
        }
        switch (type) {

            case "text":
                return await this.sock.sendMessage(jid, {
                    text: text || ""
                });

            case "image": {

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    image: buffer,
                    caption: caption || ""
                });
            }

            case "video": {

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    video: buffer,
                    caption: caption || ""
                });
            }

            case "document": {
                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);
                const filename = pathModule.basename(path);
                
                // Deteksi mimetype sederhana berdasarkan ekstensi file asli
                let ext = pathModule.extname(path).toLowerCase();
                let mimetype = "application/octet-stream"; // default jika tidak dikenal

                if (ext === ".pdf") mimetype = "application/pdf";
                else if (ext === ".png") mimetype = "image/png";
                else if (ext === ".jpg" || ext === ".jpeg") mimetype = "image/jpeg";
                else if (ext === ".zip") mimetype = "application/zip";
                else if (ext === ".txt") mimetype = "text/plain";
                else if (ext === ".docx") mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";

                return await this.sock.sendMessage(jid, {
                    document: buffer,
                    mimetype: mimetype,
                    fileName: filename // Menjaga nama file asli (misal: gambar.png) tetap utuh di WA
                });
            }

            case "audio": {

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    audio: buffer,
                    mimetype: "audio/mpeg"
                });
            }

            case "voice": {

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    audio: buffer,
                    ptt: true
                });
            }

            case "sticker": {

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    sticker: buffer
                });
            }

            default:
                throw new Error("Unsupported type: " + type);
        }
    }
    // async getAnnouncementGroup(subject) {

    //     const groups = await this.sock.groupFetchAllParticipating();

    //     for (const jid in groups) {

    //         const group = groups[jid];

    //         if (
    //             group.subject === subject &&
    //             group.isCommunityAnnounce === true
    //         ) {
    //             return jid;
    //         }
    //     }

    //     return null;
    // }
    
}

module.exports = new WhatsAppClient();