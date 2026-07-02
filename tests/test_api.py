import requests

response = requests.post(
    "http://localhost:3000/send",
    json={
        "number": "6285877507211",
        "text": "Halo dari Python!"
    }
)

print(response.status_code)
print(response.text)