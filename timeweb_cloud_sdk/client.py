from ._http import HTTPClient
from .dns.service import DNSService
from .servers.service import ServersService


class TimewebCloud:
    BASE_URL = "https://api.timeweb.cloud/api/v1"

    def __init__(self, token: str):
        self._http = HTTPClient(
            token=token,
            base_url=self.BASE_URL,
        )

        self.dns = DNSService(self._http)
        self.servers = ServersService(self._http)

    async def close(self):
        await self._http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
