import requests
import json
from . import config
from cceyes.models import Production


def datasets():
    url = config.get_config('api', 'host') + "/providers/datasets"
    response = requests.request("GET", url, headers=config.headers)

    return response


def upsert(productions: list[Production]):
    url = config.get_config('api', 'host') + "/productions"
    response = requests.request("POST", url, headers=config.headers, json=productions)

    return response
