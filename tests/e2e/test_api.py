import pytest
import requests
from fastapi import status
from tests.e2e import api_client


@pytest.mark.parametrize(
    "name, response",
    [("USD", "USD"), ("EUR", "EUR")],
)
def test_get_last_update(name, response):
    r = api_client.get_last_update(name)
    r.raise_for_status()
    assert r.status_code == 200
    assert r.ok
    result = r.json()
    assert result.get("last_update", None)
    assert result["name"] == name


def test_get_update():
    name = "USD"
    r = api_client.get_last_update(name)
    first_last_update = r.json()["last_update"]
    api_client.get_update(name)
    r = api_client.get_last_update(name)
    second_last_update = r.json()["last_update"]

    assert first_last_update != second_last_update


def test_post_to_convert():
    result = api_client.post_to_convert("USD", "EUR", 100)
    assert result.get("result")
    with pytest.raises(requests.exceptions.HTTPError) as exc:
        api_client.post_to_convert("", "", 0)
    assert exc.value.response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
