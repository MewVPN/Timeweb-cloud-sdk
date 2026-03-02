from typing import Optional, Literal, Union, Annotated
from pydantic import BaseModel, Field, TypeAdapter


class ARecordData(BaseModel):
    subdomain: Optional[str] = None
    value: str  # IP


class TXTRecordData(BaseModel):
    subdomain: Optional[str] = None
    value: str


class MXRecordData(BaseModel):
    subdomain: Optional[str] = None
    value: str
    priority: int


class _BaseDNSRecord(BaseModel):
    id: int
    ttl: int
    fqdn: str

    def full_name(self) -> str:
        if getattr(self.data, "subdomain", None):
            return f"{self.data.subdomain}.{self.fqdn}"
        return self.fqdn


class ARecord(_BaseDNSRecord):
    type: Literal["A"]
    data: ARecordData

    @property
    def ip(self) -> str:
        return self.data.value


class TXTRecord(_BaseDNSRecord):
    type: Literal["TXT"]
    data: TXTRecordData

    @property
    def content(self) -> str:
        return self.data.value


class MXRecord(_BaseDNSRecord):
    type: Literal["MX"]
    data: MXRecordData

    @property
    def host(self) -> str:
        return self.data.value

    @property
    def priority(self) -> int:
        return self.data.priority


class CNAMERecordData(BaseModel):
    subdomain: Optional[str] = None
    value: str  # target domain


class CNAMERecord(_BaseDNSRecord):
    type: Literal["CNAME"]
    data: CNAMERecordData

    @property
    def target(self) -> str:
        return self.data.value


DNSRecord = Annotated[
    Union[ARecord, TXTRecord, MXRecord, CNAMERecord],
    Field(discriminator="type"),
]

dns_record_adapter = TypeAdapter(DNSRecord)
