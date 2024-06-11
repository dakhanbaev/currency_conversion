from functools import lru_cache
from fastapi import Depends
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_host: str = 'localhost'
    db_host: str = 'localhost'
    postgres_db: str = 'dias'
    postgres_user: str = 'dias'
    postgres_password: str = 'abc123'
    api_token: str = 'token'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0


@lru_cache
def get_settings():
    return Settings()


settings: Annotated[Settings, Depends(get_settings)] = get_settings()


def get_postgres_uri() -> str:
    port = 5432 if settings.db_host == 'localhost' else 5432
    return (
        f'postgresql+asyncpg://{settings.postgres_user}:'
        f'{settings.postgres_password}@{settings.db_host}:'
        f'{port}/{settings.postgres_db}'
    )


def get_api_url() -> str:
    port = 8000 if settings.api_host == 'localhost' else 80
    return f'http://{settings.api_host}:{port}/api/concurrency_conversion'


def get_redis_uri() -> str:
    return f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}'
