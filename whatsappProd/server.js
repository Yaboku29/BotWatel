require("dotenv").config();
const express = require("express");
const whatsapp = require("./client");

const app = express();
app.use(express.json());

(async () => {

    await whatsapp.start();

    app.post("/send", (req, res) => {

        res.json({ success: true, status: "queued" });

        // Mengambil target dan tipe dari body request untuk memperjelas info di terminal
        const { number, type } = req.body;

        whatsapp.sendMessage(req.body)
            .then(result => {
                // Cetak ringkas saja di terminal agar tidak mengotori layar
                console.log(`🚀 [Node API] Berhasil mengirim pesan (${type}) ke -> ${number}`);
            })
            .catch(err => {
                // Log error ringkas untuk terminal
                console.error(`❌ [Node API Error] Gagal kirim ke ${number}:`, err.message);
            });

    });

    const PORT = process.env.PORT || 3000;

    app.listen(PORT, () => {
        console.log("API Running on port", PORT);
    });

})();