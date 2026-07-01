import requests

BASE_URL = "http://localhost:3000"


def send_text(number: str, text: str):

    response = requests.post(
        f"{BASE_URL}/send",
        json={
            "number": number,
            "text": text
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()