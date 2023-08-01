import pytest as pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.app import app
from src.database import get_session
from src.model import metadata
from settings import settings

test_engine = create_engine(
    f'postgresql+psycopg2://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}',
)

metadata.bind = test_engine

Session = sessionmaker(
    test_engine,
    autocommit=False,
    autoflush=False,
)


def override_get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    with test_engine.connect() as conn:
        metadata.create_all(test_engine)
    yield
    with test_engine.connect() as conn:
        metadata.drop_all(test_engine)



# SETUP
# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

client = TestClient(app)