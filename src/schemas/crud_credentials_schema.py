from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class Credentials(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    username: str


class CredentialsCreate(Credentials):
    pass

class CredentialsUpdate(Credentials):
    client_id: Optional[str]
    client_secret: Optional[str]
    tenant_id: Optional[str]
    username: Optional[str]

class CredentialsOut(Credentials):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

