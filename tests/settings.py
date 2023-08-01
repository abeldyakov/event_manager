from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    jwt_secret: str = ''
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    TEST_DB_HOST: str = 'localhost'
    TEST_DB_PORT: int = 5433
    TEST_DB_NAME: str = 'test_events'
    TEST_DB_USER: str = 'postgres'
    TEST_DB_PASSWORD: str = '12345678'


settings = Settings()
