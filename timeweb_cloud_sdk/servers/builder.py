from .create_models import ServerCreateRequest
from .preset_models import ServerPreset


class ServerBuilder:
    def __init__(self, service, name: str, preset: ServerPreset):
        self._service = service
        self._name = name
        self._preset = preset

        self._os_id: int | None = None
        self._software_id: int | None = None

    def os(self, os_id: int):
        self._os_id = os_id
        return self

    def software(self, software_id: int):
        self._software_id = software_id
        return self

    async def create(self):
        request = ServerCreateRequest(
            name=self._name,
            preset_id=self._preset.id,
            os_id=self._os_id,
            software_id=self._software_id,
        )
        return await self._service.create(request)

    async def create_and_wait(self):
        server = await self.create()
        return await self._service.wait_until_on(server.id)
