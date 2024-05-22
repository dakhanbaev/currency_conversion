from functools import partial

import pytest
from aiohttp import client_exceptions, ClientSession
from fastapi import status, HTTPException
from external_service.external_api import ExchangeRateApi, get_client_session
import api_gateway as _config


class FakeClientSession:
    response = None

    def __init__(self, timeout):
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, url):
        return self.response(url=url)


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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@pytest.fixture
def get_response():
    content = {
        "result": "success",
        "conversion_rates": {
            "USD": 1,
            "AED": 3.6725,
            "AFN": 73.7913,
            "ALL": 95.7917,
            "AMD": 405.2462,
        },
    }
    return partial(FakeClientResponse, status=200, content=content)


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

    @pytest.mark.asyncio
    async def test_get_all_rates_unhappy(self, exchange_rate_api, get_session):
        get_session.response = partial(
            FakeClientResponse,
            status=status.HTTP_200_OK,
            content={},
            url="",
        )
        name = "USD"
        result = await exchange_rate_api.get_all_rates(name)
        assert result is not None
        assert result == {}
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_request_handler_raise_for_status(self, exchange_rate_api, get_session):
        get_session.response = partial(
            FakeClientResponse,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={},
            url="",
            raise_exception=True,
        )
        name = "BTS"
        with pytest.raises(HTTPException) as exc:
            await exchange_rate_api.get_all_rates(name)

        assert isinstance(exc.value, HTTPException)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.asyncio
    async def test_request_handler_not_implemented(self, exchange_rate_api, get_session):
        get_session.response = partial(
            FakeClientResponse,
            status=status.HTTP_501_NOT_IMPLEMENTED,
            content={},
            url="",
            raise_json=True,
        )
        name = "BTS"

        with pytest.raises(HTTPException) as exc:
            await exchange_rate_api.get_all_rates(name)

        assert isinstance(exc.value, HTTPException)
        assert exc.value.status_code == status.HTTP_501_NOT_IMPLEMENTED


@pytest.mark.asyncio
async def test_get_client_session():
    async for session in get_client_session():
        assert isinstance(session, ClientSession)
        assert session is not None
        async with session.get("https://www.exchangerate-api.com/") as response:
            assert response.status == status.HTTP_200_OK
    assert session.closed is True
