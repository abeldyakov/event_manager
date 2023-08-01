from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from src.model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

    events = relationship("Event", secondary="members", back_populates="users")
