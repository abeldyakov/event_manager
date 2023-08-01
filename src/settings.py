from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_USER: str = ''
    DB_NAME: str = ''
    DB_PASSWORD: str = ''

    jwt_secret: str = ''
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    TEST_DB_HOST: str = 'localhost'
    TEST_DB_PORT: int = 5432
    TEST_DB_USER: str = ''
    TEST_DB_NAME: str = ''
    TEST_DB_PASSWORD: str = ''


settings = Settings(
    _env_file='/.env',
    _env_file_encoding='utf-8',
)
