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


def send_text(number: str, text: str):
    return send(
        number,
        "text",
        text=text
    )


def send_image(number: str, path: str, caption: str = ""):
    return send(
        number,
        "image",
        path=path,
        caption=caption
    )


def send_video(number: str, path: str, caption: str = ""):
    return send(
        number,
        "video",
        path=path,
        caption=caption
    )


def send_document(number: str, path: str):
    return send(
        number,
        "document",
        path=path
    )