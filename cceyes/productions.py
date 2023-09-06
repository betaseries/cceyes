import requests
import json
from . import config
from cceyes.models import Production, ProductionDataset, ProductionMeta


def find(dataset=ProductionDataset, meta=ProductionMeta):
    url = config.get_config('api', 'host') + "/productions/find"
    parameters = {"dataset": dataset.dict(), "meta": meta.dict()}

    response = requests.request("GET", url, headers=config.headers, json=parameters)

    if response.status_code == 404:
        return None

    if response:
        production = Production(**response.json())

        return production
    else:
        return None
