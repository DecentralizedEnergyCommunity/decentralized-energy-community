import urllib
import requests

from utils.config import Config

config = Config.load()


def refresh_token():
    url = "https://login.fluvius.be/klanten.onmicrosoft.com/B2C_1A_customer_signup_signin/SelfAsserted?tx=StateProperties=eyJUSUQiOiJlNTQ2ZjYyZi0xNmZmLTRmNWItYWVhZS04OGE4OTA2ZGQyMmUifQ&p=B2C_1A_customer_signup_signin"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Authorization": config["fluvius"]["token"],
        "Cookie": "_ga=GA1.1.160734925.1710452704; _upscope__region=ImV1LWNlbnRyYWwi; cookie-agreed-categories=%5B%22statistical%22%2C%22marketing%22%2C%22social%22%2C%22functional%22%5D; cookie-agreed=2; _ga_LMBLD784VJ=GS1.1.1720908225.13.1.1720910511.40.0.0; _gcl_au=1.1.578237979.1720645981; Cookie_SAC=7700808497; _ga_TMLE47NLNF=GS1.1.1720645980.1.1.1720648197.60.0.0; _hjSessionUser_1098786=eyJpZCI6IjRjYjJjMTliLWJmMmYtNTRiMy05ZTNhLThiYTBlMjdhMzZkNCIsImNyZWF0ZWQiOjE3MjA4MDA2Mjk0MTYsImV4aXN0aW5nIjp0cnVlfQ==; x-ms-cpim-csrf=bFh3Ni9zclNVWGdEa1dQYnprVzBsU0psQ0NVUzdOOGZDMjFzSVlKQ1NiMWZ0dEo0NXRrZzV2OXVOcVRBclljclBDU1duWE1xOVJNTDhQd3hzekZDclE9PTsyMDI0LTA3LTEzVDIyOjQxOjUxLjg5NjEzMjVaO3ZPZGdhQVIxQnZ4RFdrWWVFUWF3OWc9PTt7Ik9yY2hlc3RyYXRpb25TdGVwIjo1fQ==; _hjSession_1098786=eyJpZCI6ImU0YjQwYTM2LWQwNmMtNGJlOC1hOTNkLWZmNDYyZDk1MmM3ZSIsImMiOjE3MjA5MDgyMjczOTMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; x-ms-cpim-sso:klanten.onmicrosoft.com/b2c_1a_customer_signup_signin_0=m1.FEUuSiXSaE4F6Pr5.WA79TCOTlZbvkvl6iFBEGA==.0.Z1s9B6XULhAPd1xMkK82SqBGxGFG4RM6du6bZCeFcM0oACuqMr122qHQHFXHbxGp0MiwA95mm0fD12h0UmdliHxha/ju/1rPOiNsLSiZJmvmW43MtPPf+EdJCnpC+/Cy9zAj9ufgsjoMh0d3pJWSmsA6zHibMB62S6cvSvXrKbT1Fwdpw+LC4CuWbxFFHfFniSibTNDmyCyCQoAAU+BR44uEiLssDSRtx6KDJjrxLax2+TnLqXqsIE2MknqKc/EqBT5cbpTcm4jhaPULpZgucJKToTCAVj9yNpNA9Ap3HnrZyJ9KOQ1j3SzNymqYmjvue2tsXHjm6TqXZ55D2SqXJLZGGmRd+aYFs8Qy7IC0xFEFLJqaXGcjH3RVqqq8Q6bowXwDmxscPg6jvLoe5RCHztDsDYhTEWDnw+JeZ1rWeTrxhCttlmoUyAWm6RmAxsHUI8a8bR4=; x-ms-cpim-cache|p_ay_owek0-yirpw8k4qkq_0=m1.ibfCA64HQIMLZAe2.agD87/euQB7yuRAmTSABnA==.0.1rMvWY0yUu9CmvDpl3gUX+jWoqSu6VuvcG+iFUNbQ49xO15Ee5iOHsRdsg/MEKMMs8m3LHvvZ6YwUwX2x2OxsoXtkVZfP7GMiXL0uhPnGXB5aSWI2PZzjhna+naEqe8fcfpwSKVjezpR7+f3PHQiNPxMC2aC/Lx103vDMsxYt9S8JpCjcB4r8JMFw8GWsUY02uh5/rids92zWcNpia1zJ3xQI/hMOptKiugCugDI5awqeNyRIm5e27kMBM4u2N2uCdm8kscR6roxWJx14PmJlOoYPkLot6kNDLVW2FqWWO7aGEDiv+MPAVlG3rXqTk2hM9E7+DGGBXK4U2JkT9KsMjqVsdeSr4E5OM51yonRTZ41RRFd1hwthl12Zae45/3t0uFkubU7xueMogQP39Noh6ZDCQnWOe3qGnDczDare+VwExCQeekemIIZ3NCoGlMiQlZAvQfbV0Xn/jM3GECxHVW9zo60EgCf4BTLdZiCCVIjQbThFnQb+0mu14ftkrmXUq4CClobwu709f52G+Z2MKPHdLf7mPsN1Xk5Ki1bp0FhL65HxxUoym0e9iKMfxwGt1FTRYXwcAxL5W2VS9FLwe7VfKnTqBLtxKJ3xSzlYft233zF2thYB+fE093cWKrpqWn0KqOjQj6zLB76Wxv8Wv8KCw2p8h2vYOe6Pp8XOzTb8RRu/Fw//8QBCvINTNt13aOJ5DL95+Ys4r/p8W0dfdhkvAP7YdQQv3/79crWeHFv3ESMt6jNou6x6ryuLRA/9YX47ixZg9wIQV9VLnHwER2wWkFl7dmhjZ55mZ3TRivZBfVCQ9YtKMCnSLoE4tpw8l8xoKrNnf4qK9XMoJ2mNZ3RsB5iMNJCrg3amasZB04rSIyCifZrMpAKu+0I+MGZHnMHy89Y0sZpYqKT4OiKFLVIpHu7w2o+KR9pFVR/esRPlWx2J8gFA0I7zidVtpVoCb/qG1YZQw6fCUvSr3+tYPEVOsKAIM5ELX+1nZpbgtwg/In00Cln4zoLAPAttBODpUN/Db4tuQqXNqANTv6fYyElooqFsdY5uxdQKd9l99SZh5E="
    }

    payload = {
        "signInName": urllib.parse.quote(config["fluvius"]["username"]),
        "password": urllib.parse.quote(config["fluvius"]["password"]),
        "request_type": "RESPONSE",
    }

    response = requests.post(url, data=payload, headers=headers)
    response.text
    return response.headers.get("Authorization")


if __name__ == "__main__":
    token = refresh_token()
    print(token)
