from sqlalchemy import Date, ForeignKey, Column, UUID

from src.model import BaseModel


class Member(BaseModel):
    __tablename__ = 'members'

    user_uuid = Column(UUID, ForeignKey('users.uuid'), index=True, nullable=False)
    event_uuid = Column(UUID, ForeignKey('events.uuid'), index=True, nullable=False)
    date = Column(Date, nullable=False)
