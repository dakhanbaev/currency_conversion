from functools import partial

import pytest
from aiohttp import client_exceptions
from src.external_service.external_api import ExchangeRateApi
import src.config as _config


class FakeClientSession:
    response = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, url):
        return self.response(url=url)

    async def close(self):
        pass


class FakeClientResponse:
    def __init__(self, status, content, url, raise_exception=False, raise_json=False):
        self.status = status
        self.content = content
        self.url = url
        self.raise_exception = raise_exception
        self.raise_json = raise_json
        self.request_info = "INFO"
        self.history = "HISTORY"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        if self.raise_json:
            raise client_exceptions.ContentTypeError("This is a ContentTypeError", history=())
        return self.content

    def raise_for_status(self):
        if self.raise_exception:
            raise Exception("TEST Exception")


@pytest.fixture
def get_response():
    content = {
            "result": "success",
            "conversion_rates":
                {
                    "USD": 1,
                    "AED": 3.6725,
                    "AFN": 73.7913,
                    "ALL": 95.7917,
                    "AMD": 405.2462
                }
        }
    return partial(
        FakeClientResponse,
        status=200,
        content=content)


@pytest.fixture
def get_session(get_response):
    FakeClientSession.response = get_response
    return FakeClientSession


@pytest.fixture
def exchange_rate_api(get_session):
    ExchangeRateApi.client_session = get_session
    ExchangeRateApi.API_URL = _config.get_exchangerate_api_url()
    return ExchangeRateApi()


class TestExchangeRateApi:

    @pytest.mark.asyncio
    async def test_get_all_rates(self, exchange_rate_api):
        name = "USD"
        result = await exchange_rate_api.get_all_rates(name)
        assert result is not None
        assert len(result) == 5

