import requests


def refresh_token():
    url = "https://mijn.fluvius.be/verbruik/api/login"
    payload = {
        "username": "",
        "password": ""
    }

    response = requests.post(url, data=payload)
    return response.headers.get("Authorization")


if __name__ == '__main__':
    token = refresh_token()
    print(token)
