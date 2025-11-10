from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class Notification(BaseModel):
    id: int
    identifying_name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=255)
    content_html: str = Field(..., min_length=2)
    credenciales_id: int


class CreateNotification(BaseModel):
    identifying_name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=255)
    content_html: str
    credenciales_id: int


class UpdateNotification(BaseModel):
    identifying_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=255)
    content_html: str
    credenciales_id: int


class NotificationOut(Notification):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    items: List[Notification]
    per_page: int
    size: int
    total: int
    page: int
    pages: int
    last_page:int
