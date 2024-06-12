import requests
from fastapi import status
from src import config as _config


def post_user(name):
    url = _config.get_api_url()
    payload = {
        "name": name
    }
    r = requests.post(f'{url}/user', json=payload)
    r.raise_for_status()

    assert r.status_code == status.HTTP_201_CREATED
    return r.json()


def post_transaction(user_id, transaction_type, amount):
    url = _config.get_api_url()
    payload = {
        "user_id": user_id,
        "transaction_type": transaction_type,
        "amount": amount
    }
    r = requests.post(f'{url}/transaction', json=payload)
    r.raise_for_status()

    assert r.status_code == status.HTTP_201_CREATED
    return r.json()


def get_balance(user_id, timestamp):
    url = _config.get_api_url()
    payload = {
        "timestamp": timestamp
    }
    r = requests.patch(f"{url}/user/{user_id}/balance", json=payload)
    r.raise_for_status()
    assert r.status_code == status.HTTP_200_OK
    return r.json()


def get_transaction(transaction_id):
    url = _config.get_api_url()
    r = requests.get(f"{url}/transaction/{transaction_id}")
    r.raise_for_status()
    assert r.status_code == status.HTTP_200_OK
    return r.json()


