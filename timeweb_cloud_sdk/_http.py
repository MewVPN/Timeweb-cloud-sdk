import asyncio

import httpx
from .exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)


class HTTPClient:
    def __init__(self, token: str, base_url: str, timeout: float = 15):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    async def close(self):
        await self._client.aclose()

    async def request(self, method: str, url: str, retries: int = 3, **kwargs):
        for attempt in range(retries):
            response = await self._client.request(method, url, **kwargs)

            if response.status_code == 401:
                raise AuthenticationError()
            if response.status_code == 404:
                raise NotFoundError(response.text)
            if response.status_code == 422:
                raise ValidationError(response.text)
            if response.status_code == 429:
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise RateLimitError()
            if 500 <= response.status_code < 600:
                if attempt < retries - 1:
                    await asyncio.sleep(2**attempt)
                    continue
                raise ServerError(response.text)
            response.raise_for_status()
            if response.content:
                return response.json()
            return None

        raise ServerError("Request failed")
