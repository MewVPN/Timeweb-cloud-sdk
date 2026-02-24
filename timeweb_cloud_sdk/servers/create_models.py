from pydantic import BaseModel, model_validator
from typing import Optional, List


class ServerDiskCreate(BaseModel):
    size: int
    type: str


class ServerNetworkCreate(BaseModel):
    type: str
    bandwidth: Optional[int] = None
    is_ddos_guard: Optional[bool] = None


class ServerCreateRequest(BaseModel):
    name: str
    preset_id: int

    os_id: Optional[int] = None
    image_id: Optional[str] = None

    configurator_id: Optional[int] = None
    software_id: Optional[int] = None
    boot_mode: Optional[str] = None

    is_ddos_guard: Optional[bool] = None
    is_master_ssh: Optional[bool] = None
    is_dedicated_cpu: Optional[bool] = None

    cpu: Optional[int] = None
    ram: Optional[int] = None
    gpu: Optional[int] = None

    cloud_init: Optional[str] = None

    disks: Optional[List[ServerDiskCreate]] = None
    networks: Optional[List[ServerNetworkCreate]] = None

    @model_validator(mode="after")
    def validate_os_or_image(self):
        if self.os_id and self.image_id:
            raise ValueError("Cannot specify both os_id and image_id")

        if not self.os_id and not self.image_id:
            raise ValueError("Either os_id or image_id must be specified")

        return self
