from pydantic import BaseModel
from typing import Optional


class DNSRecord(BaseModel):
    id: int
    type: str
    name: str
    content: str
    ttl: int

    priority: Optional[int] = None
    weight: Optional[int] = None
    port: Optional[int] = None
