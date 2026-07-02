const express = require("express");

const startWhatsapp = require("./client");

const app = express();

app.use(express.json());

(async () => {

    const sock = await startWhatsapp();

    app.post("/send", async (req, res) => {

        const {
            number,
            type,
            text,
            path,
            caption
        } = req.body;

        const jid = number + "@s.whatsapp.net";

        try {

            switch (type) {

                case "text":

                    await sock.sendMessage(
                        jid,
                        {
                            text
                        }
                    );

                    break;

                case "image":

                    await sock.sendMessage(
                        jid,
                        {
                            image: {
                                url: path
                            },
                            caption: caption || ""
                        }
                    );

                    break;

                case "video":

                    await sock.sendMessage(
                        jid,
                        {
                            video: {
                                url: path
                            },
                            caption: caption || ""
                        }
                    );

                    break;

                case "document":

                    await sock.sendMessage(
                        jid,
                        {
                            document: {
                                url: path
                            },
                            fileName: path.split(/[\\/]/).pop()
                        }
                    );

                    break;

                default:

                    return res.status(400).json({
                        success: false,
                        message: "Unknown message type"
                    });

            }

            res.json({
                success: true
            });

        }
        catch (err) {

            console.error(err);

            res.status(500).json({
                success: false,
                message: err.message
            });

        }

    });

    app.listen(3000, () => {

        console.log("API Running");

    });

})();