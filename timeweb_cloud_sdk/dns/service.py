from typing import List
from .._http import HTTPClient
from .models import DNSRecord
from .builder import DNSBuilder


class DNSService:
    def __init__(self, http: HTTPClient):
        self._http = http

    def builder(self, fqdn: str) -> DNSBuilder:
        return DNSBuilder(self, fqdn)

    async def list(self) -> List[str]:
        data = await self._http.request(
            "GET",
            "/domains",
        )
        return [d["fqdn"] for d in data.get("domains", [])]

    async def list_records(self, fqdn: str) -> List[DNSRecord]:
        data = await self._http.request(
            "GET",
            f"/domains/{fqdn}/dns-records",
        )
        return [DNSRecord(**r) for r in data.get("dns_records", [])]

    async def create_record(
        self,
        fqdn: str,
        record_type: str,
        value: str,
        ttl: int = 600,
    ) -> DNSRecord:
        payload = {
            "type": record_type,
            "content": value,
            "ttl": ttl,
        }

        data = await self._http.request(
            "POST",
            f"/domains/{fqdn}/dns-records",
            json=payload,
        )

        return DNSRecord(**data["dns_record"])

    async def update_record(
        self,
        fqdn: str,
        record_id: int,
        record_type: str,
        value: str,
        ttl: int = 600,
    ) -> DNSRecord:
        payload = {
            "type": record_type,
            "content": value,
            "ttl": ttl,
        }

        data = await self._http.request(
            "PATCH",
            f"/domains/{fqdn}/dns-records/{record_id}",
            json=payload,
        )

        return DNSRecord(**data["dns_record"])

    async def delete_record(
        self,
        fqdn: str,
        record_id: int,
    ):
        await self._http.request(
            "DELETE",
            f"/domains/{fqdn}/dns-records/{record_id}",
        )
