import requests
import json
from . import config


def me():
    url = "https://api.cceyes.eu/providers/me"
    response = requests.request("GET", url, headers=config.headers)

    return response


def upsert(productions):
    url = "https://api.cceyes.eu/productions"
    response = requests.request("POST", url, headers=config.headers, json=productions)

    return response
