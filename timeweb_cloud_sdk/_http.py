import asyncio
import random
import httpx

from .exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from ._rater import RateLimiter


class HTTPClient:
    def __init__(
        self,
        token: str,
        base_url: str,
        timeout: float = 15,
        rate_limit: int = 20,
        transport=None,
    ):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
            transport=transport,
        )

        self._limiter = RateLimiter(rate=rate_limit)

    async def close(self):
        await self._client.aclose()

    @staticmethod
    async def _sleep_with_jitter(attempt: int):
        base = 1
        max_delay = base * (2**attempt)
        delay = random.uniform(0, max_delay)
        await asyncio.sleep(delay)

    async def request(self, method: str, url: str, retries: int = 3, **kwargs):
        for attempt in range(retries):
            await self._limiter.acquire()

            response = await self._client.request(method, url, **kwargs)

            if response.status_code == 401:
                raise AuthenticationError()

            if response.status_code == 404:
                raise NotFoundError(response.text)

            if response.status_code == 422:
                raise ValidationError(response.text)

            if response.status_code == 429:
                if attempt < retries - 1:
                    await self._sleep_with_jitter(attempt)
                    continue
                raise RateLimitError()

            if 500 <= response.status_code < 600:
                if attempt < retries - 1:
                    await self._sleep_with_jitter(attempt)
                    continue
                raise ServerError(response.text)

            response.raise_for_status()

            if response.content:
                return response.json()

            return None

        raise ServerError("Request failed after retries")
