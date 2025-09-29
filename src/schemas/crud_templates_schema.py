
from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import Optional


class Notification(BaseModel):
    identifying_name: str = Field(...,min_length=1, max_length=100) 
    description: str = Field(...,min_length=1, max_length=255)
    content_html: str = Field(...,min_length=2)
    credenciales_id : int

class CreateNotification(Notification):
    pass

class UpdateNotification(Notification):
    identifying_name: Optional[str] = Field(default=None,min_length=1, max_length=100)
    description: Optional[str] = Field(default=None,min_length=1, max_length=255)
    content_html:  Optional[str] = Field(default=None)

class NotificationOut(Notification):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

