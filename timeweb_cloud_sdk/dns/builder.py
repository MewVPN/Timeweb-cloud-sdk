from typing import Optional


class DNSBuilder:
    def __init__(self, service, fqdn: str):
        self._service = service
        self._fqdn: str = fqdn
        self._type: Optional[str] = None
        self._value: Optional[str] = None
        self._ttl: int = 600

    def a(self, ip: str):
        self._type = "A"
        self._value = ip
        return self

    def aaaa(self, ip: str):
        self._type = "AAAA"
        self._value = ip
        return self

    def cname(self, target: str):
        self._type = "CNAME"
        self._value = target
        return self

    def ttl(self, ttl: int):
        self._ttl = ttl
        return self

    async def create(self):
        if not self._type or not self._value:
            raise ValueError("Record type and value must be specified")

        return await self._service.create_record(
            fqdn=self._fqdn,
            record_type=self._type,
            value=self._value,
            ttl=self._ttl,
        )
