require("dotenv").config();
const express = require("express");
const whatsapp = require("./client");

const app = express();
app.use(express.json());

(async () => {

    await whatsapp.start();

    app.post("/send", (req, res) => {

        res.json({ success: true, status: "queued" });

        whatsapp.sendMessage(req.body)
            .then(result => {
                console.log("SEND OK");
            })
            .catch(err => {
                console.error("SEND ERROR:", err.message);
            });

    });

    const PORT = process.env.PORT || 3000;

    app.listen(PORT, () => {
        console.log("API Running on port", PORT);
    });

})();