import requests
from config import WA_API_URL

BASE_URL = WA_API_URL


def send(
    number: str,
    message_type: str,
    text: str = "",
    path: str = "",
    caption: str = ""
):

    try:
        response = requests.post(
            f"{BASE_URL}/send",
            json={
                "number": number,
                "type": message_type,
                "text": text,
                "path": path,
                "caption": caption
            },
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("❌ WA API timeout")
        return {"success": False, "error": "timeout"}

    except requests.exceptions.RequestException as e:
        print("❌ WA API error:", str(e))
        return {"success": False, "error": str(e)}


# ======================
# TEXT
# ======================
def send_text(number: str, text: str):
    if not text:
        text = ""

    return send(
        number,
        "text",
        text=text
    )


# ======================
# IMAGE
# ======================
def send_image(number: str, path: str, caption: str = ""):

    if not path:
        raise ValueError("path wajib untuk image")

    return send(
        number,
        "image",
        path=path,
        caption=caption
    )


# ======================
# VIDEO
# ======================
def send_video(number: str, path: str, caption: str = ""):

    if not path:
        raise ValueError("path wajib untuk video")

    return send(
        number,
        "video",
        path=path,
        caption=caption
    )


# ======================
# DOCUMENT
# ======================
def send_document(number: str, path: str):

    if not path:
        raise ValueError("path wajib untuk document")

    return send(
        number,
        "document",
        path=path
    )