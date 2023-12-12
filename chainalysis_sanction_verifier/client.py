import os
import asyncio
import time
import json
from typing import Optional, List, Dict, TypedDict

from httpx import AsyncClient, Response


__all__ = [
    "ChainalysisApiException",
    "Identification",
    "Client",
]


class ChainalysisApiException(Exception):
    pass


class Identification(TypedDict):
    """
    Information regarding a sanctioned address.
    """

    category: str
    """
    The Chainalysis Entity category. For sanctioned addresses, the value will be 'sanctions'.
    """

    name: Optional[str]
    """
    The OFAC name associated with the sanctioned address.
    """

    description: Optional[str]
    """
    The OFAC description of the sanctioned address.
    """

    url: Optional[str]
    """
    The OFAC URL for more information about the sanctioned address.
    """


class Client:
    """
    Chainalysis address screening client.
    """

    BASE_URL = "https://public.chainalysis.com/api/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        rate_limit_delay: int | float = 0.06,
    ) -> None:
        self.api_key = os.getenv("CHAINALYSIS_API_KEY", api_key)
        if self.api_key is None:
            raise ValueError(
                "No API key provided. Either provide an API key or set "
                "a 'CHAINALYSIS_API_KEY' environment variable."
            )

        self.rate_limit_delay = rate_limit_delay
        self._client = AsyncClient()

        # rate limiting stuff:
        self._last_request_time = 0.0
        self._rl_lock = asyncio.Lock()

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _to_dict(self) -> dict:
        return {
            "api_key": self.api_key,
            "rate_limit_delay": self.rate_limit_delay,
        }

    def __str__(self) -> str:
        return f"ChainalysisSanctionClient({self._to_dict()})"

    def __repr__(self) -> str:
        return str(self)

    def display(self) -> str:
        return f"ChainalysisSanctionClient({json.dumps(self._to_dict(), indent=4)})"

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, endpoint: str, headers: Dict[str, str]) -> Response:
        async with self._rl_lock:
            time_since_request = time.time() - self._last_request_time
            wait_time = self.rate_limit_delay - time_since_request
            if wait_time > 0:
                await asyncio.sleep(wait_time)

            task = asyncio.Task(
                coro=self._client.get(
                    url=f"{self.BASE_URL}/{endpoint.lstrip('/')}",
                    headers=headers,
                ),
            )
            self._last_request_time = time.time()

        response = await task
        if response.status_code > 200:
            raise ChainalysisApiException(
                {
                    "code": response.status_code,
                    "type": _error_types.get(response.status_code),
                    "text": response.text,
                }
            )

        return response

    async def check_address_sanction_identifications(
        self,
        address: str,
    ) -> List[Identification]:
        """
        Checks whether an address is sanctioned and returns an identifications array with any available
        sanctions data.

        :param address: Cryptocurrency address to check sanction status for. Note: the string is case-sensitive.
        :returns: An array that contains any available identification information for the provided address.
        Note: If the array is empty, the address has not been sanctioned
        """
        response = await self._get(
            endpoint=f"address/{address}",
            headers={
                "X-API-KEY": self.api_key,
                "Accept": "application/json",
            },
        )
        return response.json()["identifications"]


_error_types = {
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    406: "Not Acceptable",
    500: "Internal Server Error",
    503: "Service Unavailable Error",
    504: "Request Timeout",
}
