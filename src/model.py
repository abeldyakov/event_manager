
import uuid as uuid
from sqlalchemy import (
    Column, UUID
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    __abstract__ = True

    uuid = Column(UUID, primary_key=True, default=uuid.uuid4)
