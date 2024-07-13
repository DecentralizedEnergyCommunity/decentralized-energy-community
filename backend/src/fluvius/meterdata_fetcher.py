import pandas as pd
import requests
import datetime
import urllib.parse
import io

from backend.src.domain.meterdata import Granularity, MeterData


class MeterDataFetcher:

    @staticmethod
    def refresh_token():

        url = "https://mijn.fluvius.be/verbruik/api/login"
        payload = {
            "username": "",
            "password": ""
        }

        response = requests.post(url, data=payload)
        return response.headers.get("Authorization")

    def fetch_meter_data(self, ean: str, start: datetime, end: datetime, granularity: Granularity) -> MeterData:
        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InBwZkp3N0c0SGpNeHJkb0syMXJ6dUVha0M4dlRPTDJONzIzLUpfUlB1X0EiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiI5MWJiOWEwYS1mNDVkLTQ5MWEtYWUwYi00MzMyNGZiYzM0M2EiLCJpc3MiOiJodHRwczovL2xvZ2luLmZsdXZpdXMuYmUvNmUyMDI1ZDItMWZkMC00MGZiLWE3OGUtMmQ4YWQ5ODVmMDYxL3YyLjAvIiwiZXhwIjoxNzIwODYwNTMyLCJuYmYiOjE3MjA4NTY5MzIsImlkZW50aXR5X3Byb3ZpZGVyIjoiaWRwLmlhbWZhcy5iZWxnaXVtLmJlIiwiZ2l2ZW5fbmFtZSI6Ikplcm9lbiIsInN1cl9uYW1lIjoiUGVlbGFlcnRzIiwiZW1haWwiOiJwbGFjZWhvbGRlckBuby5lbWFpbC5hdmFpbGFibGUiLCJzdWIiOiI0N2I5ZGQ3OS0xZTE1LTQ1MjItYWE4MS1jMTEwOWQzZGIwMTEiLCJidXNpbmVzc3BhcnRuZXJfaWQiOiI3NzAwODA4NDk3IiwidGlkIjoiNmUyMDI1ZDItMWZkMC00MGZiLWE3OGUtMmQ4YWQ5ODVmMDYxIiwibm9uY2UiOiIwMTkwYTYyMi0xMmRkLTcyYWQtOGQxMi1hNjdmMzkwMWI2MmIiLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJhenAiOiI5MWJiOWEwYS1mNDVkLTQ5MWEtYWUwYi00MzMyNGZiYzM0M2EiLCJ2ZXIiOiIxLjAiLCJpYXQiOjE3MjA4NTY5MzJ9.Is5IzmSc4AvYtqhgrbzEWg8_92w56Jg4cqa1zYlVK6m-frs8I6fKsoK_v6ozEWxMUu2xeRihHwaVjrCmlzFlvvx0Yl10wjK2WjxVSCk_Bz-T0ZsER1XPfXNASLcjFklY4_2xEsXMJLo9BkhVeK7xCjGCYMUVrqpx0cXH9XShaYz4TLR923aubFlB3ZJ1INgHRlGVf0uhWHikzEPQlE0A25qgqIWMqaZGOznl3kxvRKtfSu2yeZupSlBwTDcKPgIiid0XOr-2rAXEzu-D6fP4Jb7kLWbxv0J_SY3hAqDSJz6faFhqFb9Ok16qWdwVPUo0jWQfpT8mb0iwUKRnmLNnJw",
        }

        start_str = urllib.parse.quote(start.strftime("%Y-%m-%dT%H:%M:%S%z"))
        end_str = urllib.parse.quote(end.strftime("%Y-%m-%dT%H:%M:%S%z"))
        endpoint = f"https://mijn.fluvius.be/verbruik/api/consumption-histories/{ean}/report?historyFrom={start_str}&historyUntil={end_str}&granularity={granularity}&asServiceProvider=false"
        response = requests.get(endpoint, headers=headers)
        print(response.text)

        df = pd.read_csv(io.StringIO(response.text), index_col=0)
        return MeterData(ean, df)


if __name__ == '__main__':
    token = MeterDataFetcher().refresh_token()
    print(token)
