from typing import List
from pydantic import BaseModel


class ServerPreset(BaseModel):
    id: int
    location: str
    price: int

    cpu: int
    cpu_frequency: str
    ram: int

    disk: int
    disk_type: str
    bandwidth: int

    description: str | None = None
    description_short: str | None = None

    is_allowed_local_network: bool
    vds_node_configuration_name: str

    tags: List[str] = []

    @property
    def is_nl(self) -> bool:
        return self.location == "nl-1"

    @property
    def is_ru(self) -> bool:
        return self.location.startswith("ru-")

    @property
    def is_kz(self) -> bool:
        return self.location == "kz-1"
