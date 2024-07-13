import requests


def refresh_token():
    """
    Get the Authorization token from the Fluvius API. POST request yields status 200, but not Authorization header in the response.
    """
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
