import pytest
import httpx

from timeweb_cloud_sdk import TimewebCloud
from timeweb_cloud_sdk.servers.builder import ServerBuilder
from timeweb_cloud_sdk.servers.preset_models import ServerPreset


class DummyService:
    def __init__(self):
        self.request = None

    async def create(self, request):
        self.request = request

        class S:
            id = 1

        return S()

    async def wait_until_on(self, server_id):
        return {"id": server_id, "status": "on"}


@pytest.mark.asyncio
async def test_server_builder_create():
    preset = ServerPreset(
        id=10,
        price=100,
        cpu=2,
        cpu_frequency="3.0",
        ram=2048,
        disk=20,
        disk_type="ssd",
        bandwidth=100,
        is_allowed_local_network=True,
        vds_node_configuration_name="basic",
        tags=[],
    )

    service = DummyService()

    builder = ServerBuilder(service, "test-server", preset)
    await builder.os(1).software(2).create()

    assert service.request.name == "test-server"
    assert service.request.preset_id == 10
    assert service.request.os_id == 1
    assert service.request.software_id == 2


@pytest.mark.asyncio
async def test_delete_and_wait():
    calls = 0

    def handler(request: httpx.Request):
        nonlocal calls
        calls += 1

        if request.method == "DELETE":
            return httpx.Response(204)

        return httpx.Response(404)

    transport = httpx.MockTransport(handler)

    async with TimewebCloud("x", transport=transport) as client:
        await client.servers.delete_and_wait(1, interval=0.01, timeout=1)

    assert calls >= 1
