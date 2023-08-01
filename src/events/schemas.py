from datetime import date
from typing import Optional, List
from pydantic import BaseModel, UUID4, Field
import uuid

from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from src.auth.schemas import User


class BaseEvent(BaseModel):
    date: date
    name: str
    description: Optional[str]


class Event(BaseEvent):
    uuid: UUID4 = Field(default_factory=uuid.uuid4)

    class Config:
        from_attributes = True


class EventOut(Event):
    users: List[User] = []

    class Config:
        from_attributes = True


class EventList(Event):
    members_count: int = 0

    class Config:
        from_attributes = True


class EventCreate(BaseEvent):
    pass


class EventUpdate(BaseEvent):
    pass
