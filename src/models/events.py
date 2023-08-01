from sqlalchemy import Date, String, Column
from sqlalchemy.orm import relationship

from src.model import BaseModel


class Event(BaseModel):
    __tablename__ = 'events'

    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("User", secondary="members", back_populates="events")
