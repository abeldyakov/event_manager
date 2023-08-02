from sqlalchemy import (
    Date,
    ForeignKey,
    String, select, func
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, object_session

from sqlalchemy import (
    Column, UUID
)

from ..model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    events = relationship("Event", secondary="members", back_populates="users")


class Event(BaseModel):
    __tablename__ = 'events'

    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("User", secondary="members", back_populates="events")

    @hybrid_property
    def members_count(self):
        return object_session(self).query(Member).filter(
            Member.event_uuid == self.uuid).count()

    @members_count.expression
    def courses_count(cls):
        return select([func.count(Member.user_uuid)]).where(
            Member.event_uuid == cls.uuid).label('members_count')


class Member(BaseModel):
    __tablename__ = 'members'

    user_uuid = Column(UUID, ForeignKey('users.uuid'), index=True, nullable=False)
    event_uuid = Column(UUID, ForeignKey('events.uuid'), index=True, nullable=False)
    date = Column(Date, nullable=False)
