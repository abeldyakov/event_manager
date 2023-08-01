from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

engine = create_engine(
    f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}',
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

