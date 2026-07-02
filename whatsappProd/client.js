const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    Browsers
} = require("@whiskeysockets/baileys");

const P = require("pino");
const qrcode = require("qrcode-terminal");
const fs = require("fs");

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
        this.sock = makeWASocket({
            auth: this.state,
            browser: Browsers.ubuntu("BotWatel"),
            logger: P({ level: "silent" })
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

            await this.listGroups();
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
        community,
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

            case "image":

                if (!fs.existsSync(path)) {
                    throw new Error("File tidak ditemukan: " + path);
                }

                const buffer = fs.readFileSync(path);

                return await this.sock.sendMessage(jid, {
                    image: buffer,
                    caption: caption || ""
                });

            default:
                throw new Error("Unsupported type: " + type);
        }
    }
    async getAnnouncementGroup(subject) {

        const groups = await this.sock.groupFetchAllParticipating();

        for (const jid in groups) {

            const group = groups[jid];

            if (
                group.subject === subject &&
                group.isCommunityAnnounce === true
            ) {
                return jid;
            }
        }

        return null;
    }
    
}

module.exports = new WhatsAppClient();