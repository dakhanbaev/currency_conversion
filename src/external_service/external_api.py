import abc
import logging
from aiohttp import ClientSession, ClientResponse, client_exceptions
from fastapi import status, HTTPException

from src.config import get_exchangerate_api_url


logger = logging.getLogger(__name__)


async def get_client_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


class ExternalApi(abc.ABC):

    API_URL: str
    client_session: ClientSession

    @abc.abstractmethod
    async def get_all_rates(self, code: str):
        raise NotImplementedError


class ExchangeRateApi:

    API_URL = get_exchangerate_api_url()
    client_session = ClientSession

    async def _get_exchange_rates(self, url: str) -> dict:
        async with self.client_session() as session:
            async with session.get(url) as response:
                return await self._parse_response(response)

    @staticmethod
    async def _parse_response(response: ClientResponse) -> dict:
        try:
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=response.status, detail=str(e))

        try:
            content = await response.json()
        except client_exceptions.ContentTypeError:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"Invalid JSON response from api for url : {response.url}",
            )

        return content

    async def get_all_rates(self, code: str) -> dict:
        url = f"{self.API_URL}{code}"
        result = await self._get_exchange_rates(url)
        if rates := result.get("conversion_rates"):
            return rates
        return {}
