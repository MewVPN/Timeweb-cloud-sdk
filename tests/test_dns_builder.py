import pytest
from timeweb_cloud_sdk.dns.builder import DNSBuilder


class DummyService:
    def __init__(self):
        self.called = None

    async def create_record(self, **kwargs):
        self.called = kwargs
        return {"ok": True}


@pytest.mark.asyncio
async def test_dns_builder_a():
    service = DummyService()

    builder = DNSBuilder(service, "example.com")
    await builder.a("1.2.3.4").ttl(300).create()

    assert service.called["record_type"] == "A"
    assert service.called["value"] == "1.2.3.4"
    assert service.called["ttl"] == 300
