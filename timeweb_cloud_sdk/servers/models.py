from pydantic import BaseModel
from typing import List, Optional


class ServerOS(BaseModel):
    id: int
    name: str
    version: Optional[str] = None


class ServerSoftware(BaseModel):
    id: int
    name: str


class ServerImage(BaseModel):
    id: str
    name: str
    is_custom: bool


class ServerIP(BaseModel):
    ip: str
    type: str
    is_main: bool
    ptr: Optional[str] = None
    id: Optional[str] = None


class ServerNetwork(BaseModel):
    type: str
    bandwidth: Optional[int] = None
    nat_mode: Optional[str] = None
    ips: List[ServerIP] = []
    blocked_ports: List[int] = []
    is_ddos_guard: Optional[bool] = None
    is_image_mounted: Optional[bool] = None


class ServerDisk(BaseModel):
    id: int
    size: int
    used: int
    type: str
    is_mounted: bool
    is_system: bool
    status: str
    system_name: Optional[str] = None
    is_auto_backup: Optional[bool] = None
    comment: Optional[str] = None


class Server(BaseModel):
    id: int
    name: str
    status: str

    comment: Optional[str] = None
    created_at: Optional[str] = None
    start_at: Optional[str] = None
    status_changed_at: Optional[str] = None

    os: Optional[ServerOS] = None
    software: Optional[ServerSoftware] = None
    image: Optional[ServerImage] = None

    preset_id: Optional[int] = None
    configurator_id: Optional[int] = None
    location: Optional[str] = None
    availability_zone: Optional[str] = None
    boot_mode: Optional[str] = None

    cpu: Optional[int] = None
    gpu: Optional[int] = None
    cpu_frequency: Optional[str] = None
    ram: Optional[int] = None
    is_dedicated_cpu: Optional[bool] = None

    is_ddos_guard: Optional[bool] = None
    is_master_ssh: Optional[bool] = None
    is_qemu_agent: Optional[bool] = None
    is_allow_root_ssh_pass: Optional[bool] = None
    is_available_additional_ip: Optional[bool] = None

    avatar_id: Optional[str] = None
    avatar_link: Optional[str] = None
    vnc_pass: Optional[str] = None
    root_pass: Optional[str] = None

    project_id: Optional[int] = None

    networks: List[ServerNetwork] = []
    disks: List[ServerDisk] = []

    cloud_init: Optional[str] = None
