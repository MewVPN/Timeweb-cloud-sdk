from typing import List

from .._http import HTTPClient
from .._polling import wait_for_condition

from .models import Server
from .create_models import ServerCreateRequest
from .preset_models import ServerPreset
from .preset_selector import PresetSelector
from .fsm import ensure_not_terminal, is_power_on, is_power_off
from .builder import ServerBuilder


class ServersService:
    def __init__(self, http: HTTPClient):
        self._http = http

    def builder(self, name: str, preset: ServerPreset) -> ServerBuilder:
        return ServerBuilder(self, name, preset)

    async def list(self) -> List[Server]:
        data = await self._http.request("GET", "/servers")
        return [Server(**s) for s in data.get("servers", [])]

    async def get(self, server_id: int) -> Server:
        data = await self._http.request("GET", f"/servers/{server_id}")
        return Server(**data["server"])

    async def create(self, request: ServerCreateRequest) -> Server:
        data = await self._http.request(
            "POST",
            "/servers",
            json=request.model_dump(exclude_none=True),
        )
        return Server(**data["server"])

    async def presets(self) -> List[ServerPreset]:
        data = await self._http.request("GET", "/presets/servers")
        return [ServerPreset(**p) for p in data.get("server_presets", [])]

    async def presets_selector(self) -> PresetSelector:
        presets = await self.presets()
        return PresetSelector(presets)

    async def reboot(self, server_id: int):
        await self._http.request("POST", f"/servers/{server_id}/reboot")

    async def power_off(self, server_id: int):
        await self._http.request("POST", f"/servers/{server_id}/shutdown")

    async def hard_power_off(self, server_id: int):
        await self._http.request("POST", f"/servers/{server_id}/hard-shutdown")

    async def power_on(self, server_id: int):
        await self._http.request("POST", f"/servers/{server_id}/start")

    async def wait_until_on(
        self,
        server_id: int,
        interval: float = 3,
        timeout: float = 600,
    ) -> Server:
        async def fetch():
            return await self.get(server_id)

        def check(server: Server):
            ensure_not_terminal(server.status)
            return is_power_on(server.status)

        return await wait_for_condition(fetch, check, interval=interval, timeout=timeout)

    async def wait_until_off(
        self,
        server_id: int,
        interval: float = 3,
        timeout: float = 600,
    ) -> Server:
        async def fetch():
            return await self.get(server_id)

        def check(server: Server):
            ensure_not_terminal(server.status)
            return is_power_off(server.status)

        return await wait_for_condition(fetch, check, interval=interval, timeout=timeout)

    async def power_on_and_wait(self, server_id: int) -> Server:
        await self.power_on(server_id)
        return await self.wait_until_on(server_id)

    async def power_off_and_wait(self, server_id: int) -> Server:
        await self.power_off(server_id)
        return await self.wait_until_off(server_id)

    async def reboot_and_wait(self, server_id: int) -> Server:
        await self.reboot(server_id)
        return await self.wait_until_on(server_id)
