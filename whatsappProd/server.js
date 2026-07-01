const express = require("express");

const whatsapp = require("./client");

const app = express();

app.use(express.json());

(async () => {

    await whatsapp.start();

    app.post("/send", async (req, res) => {

        const {
            number,
            text
        } = req.body;

        try {

            await whatsapp.sendText(
                number,
                text
            );

            res.json({
                success: true
            });

        }

        catch (err) {

            console.error(err);

            res.status(500).json({
                success: false
            });

        }

    });

    app.get("/", (req, res) => {
        res.send("BotWatel API is running");
    });

    app.get("/status", (req, res) => {
        res.json({
            connected: whatsapp.sock !== null
        });
    });

    app.listen(3000, () => {

        console.log("API Running");

    });

})();