import requests
import json
from . import config
from cceyes.models import Production


def datasets():
    url = config.get_config('api', 'host') + "/providers/datasets"
    response = requests.request("GET", url, headers=config.headers)

    return response


def stats():
    url = config.get_config('api', 'host') + "/providers/stats"
    response = requests.request("GET", url, headers=config.headers)

    return response


def upsert(productions: list[Production]):
    url = config.get_config('api', 'host') + "/productions"

    # go through every item in the list and convert to JSON
    for i, production in enumerate(productions):
        productions[i] = production.dict()

    response = requests.request("POST", url, headers=config.headers, json=productions)

    return response
