const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    Browsers
} = require("@whiskeysockets/baileys");

const P = require("pino");
const qrcode = require("qrcode-terminal");

class WhatsAppClient {

    constructor() {

        this.sock = null;

        this.state = null;

        this.saveCreds = null;
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

            logger: P({
                level: "info"
            })

        });

        this.sock.ev.on(
            "creds.update",
            this.saveCreds
        );

        this.sock.ev.on(
            "connection.update",
            this.handleConnection.bind(this)
        );

    }

    async handleConnection(update) {

        const {
            connection,
            qr,
            lastDisconnect
        } = update;

        if (qr) {

            qrcode.generate(qr, {
                small: true
            });

        }

        if (connection === "open") {

            console.log("WhatsApp Connected");

        }

        if (connection === "close") {

            const status =
                lastDisconnect?.error?.output?.statusCode;

            console.log("Disconnected :", status);

            if (
                status === DisconnectReason.restartRequired
            ) {

                console.log("Restarting Socket...");

                await this.createSocket();

            }

        }

    }

    async sendText(number, text) {

        if (!this.sock) {

            throw new Error("WhatsApp belum connect");

        }

        return await this.sock.sendMessage(

            number + "@s.whatsapp.net",

            {
                text
            }

        );

    }

}

module.exports = new WhatsAppClient();