import pytest
import httpx
from timeweb_cloud_sdk import TimewebCloud


@pytest.mark.asyncio
async def test_wait_until_on():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1

        status = "off" if calls < 2 else "on"

        return httpx.Response(
            200,
            json={
                "server": {
                    "id": 1,
                    "name": "srv",
                    "status": status,
                }
            },
        )

    transport = httpx.MockTransport(handler)

    async with TimewebCloud("x", transport=transport) as client:
        server = await client.servers.wait_until_on(1, interval=0.01, timeout=1)

    assert server.status == "on"
    assert calls >= 2
