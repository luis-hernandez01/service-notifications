from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Credentials(BaseModel):
    id: int
    client_id: str
    client_secret: str
    tenant_id: str
    username: str


class CredentialsCreate(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    username: str


class CredentialsUpdate(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]
    tenant_id: Optional[str]
    username: Optional[str]


class CredentialsOut(Credentials):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    items: List[Credentials]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
