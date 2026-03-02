import pytest
import httpx

from timeweb_cloud_sdk._http import HTTPClient
from timeweb_cloud_sdk.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
)


@pytest.mark.asyncio
async def test_http_empty_response():
    def handler(request):
        return httpx.Response(204)

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    result = await client.request("GET", "/test")
    assert result is None


@pytest.mark.asyncio
async def test_http_success():
    def handler(request):
        return httpx.Response(200, json={"ok": True})

    client = HTTPClient(
        token="x",
        base_url="https://api.test",
        transport=httpx.MockTransport(handler),
    )

    result = await client.request("GET", "/test")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_http_401():
    def handler(request):
        return httpx.Response(401)

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    with pytest.raises(AuthenticationError):
        await client.request("GET", "/test")


@pytest.mark.asyncio
async def test_http_retry_on_429():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls < 2:
            return httpx.Response(429)
        return httpx.Response(200, json={"ok": True})

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    result = await client.request("GET", "/test")

    assert result == {"ok": True}
    assert calls == 2


@pytest.mark.asyncio
async def test_http_404():
    def handler(request):
        return httpx.Response(404, text="not found")

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    with pytest.raises(NotFoundError):
        await client.request("GET", "/test")


@pytest.mark.asyncio
async def test_http_422():
    def handler(request):
        return httpx.Response(422, text="validation error")

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    with pytest.raises(ValidationError):
        await client.request("GET", "/test")


@pytest.mark.asyncio
async def test_http_500_retry_fail():
    def handler(request):
        return httpx.Response(500, text="boom")

    client = HTTPClient("x", "https://api.test", transport=httpx.MockTransport(handler))

    with pytest.raises(ServerError):
        await client.request("GET", "/test", retries=1)
