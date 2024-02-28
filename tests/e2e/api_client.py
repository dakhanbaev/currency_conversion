import requests
from fastapi import status
from src import config as _config


def get_update(name):
    url = _config.get_api_url()
    r = requests.get(f"{url}/update/{name}")
    r.raise_for_status()
    assert r.status_code == status.HTTP_200_OK
    assert r.json() == {"result": "Updated successfully"}


def post_to_convert(source_currency, target_currency, amount):
    url = _config.get_api_url()
    r = requests.post(
        f"{url}/convert",
        json={
            "source_currency": source_currency,
            "target_currency": target_currency,
            "amount": amount,
        },
    )
    r.raise_for_status()

    assert r.status_code == status.HTTP_200_OK
    return r.json()


def get_last_update(name):
    url = _config.get_api_url()
    return requests.get(f"{url}/last_update/{name}")
