from .create_models import ServerCreateRequest


class ServerBuilder:
    def __init__(self, service, name: str, preset_id: int):
        self._service = service
        self._data = ServerCreateRequest(name=name, preset_id=preset_id, os_id=99)
        self._os_set = False
        self._image_set = False

    def os(self, os_id: int):
        self._data.os_id = os_id
        self._data.image_id = None
        self._os_set = True
        self._image_set = False
        return self

    def image(self, image_id: str):
        self._data.image_id = image_id
        self._data.os_id = None
        self._image_set = True
        self._os_set = False
        return self

    def location(self, location: str):
        self._data.location = location
        return self

    def availability_zone(self, zone: str):
        self._data.availability_zone = zone
        return self

    def cloud_init(self, data: str):
        self._data.cloud_init = data
        return self

    async def create(self):
        if not self._os_set and not self._image_set:
            raise ValueError("You must specify either os() or image()")

        request = ServerCreateRequest(**self._data.model_dump(exclude_none=True))

        return await self._service.create(request)

    async def create_and_wait(self):
        server = await self.create()
        return await self._service.wait_until_on(server.id)
