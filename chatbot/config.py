import asyncio

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    MEMORY_KEY: str = "chat_history"
    MAX_TOKENS: int = 2048

    class Config:
        case_sensitive = True
        extra = "allow"
        env_file = ".env"


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()


loop = asyncio.get_event_loop()
