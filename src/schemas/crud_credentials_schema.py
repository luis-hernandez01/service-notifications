from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Credentials(BaseModel):
    identificador: str = Field(..., max_length=255)
    client_id: str
    client_secret: str
    tenant_id: str
    username: str


class CredentialsCreate(Credentials):
    pass

class CredentialsUpdate(Credentials):
    identificador: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    tenant_id: Optional[str]
    username: Optional[str]

class CredentialsOut(Credentials):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

