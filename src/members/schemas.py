from pydantic import BaseModel, UUID4, Field
import uuid
from datetime import date


class Member(BaseModel):
    user_uuid: UUID4 = Field(default_factory=uuid.uuid4)
    event_uuid: UUID4 = Field(default_factory=uuid.uuid4)
    date: date

    class Config:
        from_attributes = True
