import pytest
import httpx
from timeweb_cloud_sdk import TimewebCloud


@pytest.mark.asyncio
async def test_servers_list():
    def handler(request):
        return httpx.Response(
            200,
            json={"servers": [{"id": 1, "name": "srv", "status": "on"}]},
        )

    transport = httpx.MockTransport(handler)

    async with TimewebCloud("x", transport=transport) as client:
        servers = await client.servers.list()

    assert len(servers) == 1
    assert servers[0].id == 1
    assert servers[0].status == "on"


@pytest.mark.asyncio
async def test_server_actions():
    calls = []

    def handler(request):
        calls.append((request.method, request.url.path))
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)

    async with TimewebCloud("x", transport=transport) as client:
        await client.servers.power_on(1)
        await client.servers.power_off(1)
        await client.servers.hard_power_off(1)
        await client.servers.reboot(1)

    assert len(calls) == 4
