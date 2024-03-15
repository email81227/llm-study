import asyncio

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FinLAB_TOKEN: str

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


if settings.FinLAB_TOKEN is None:
    print("Please register to FinLAB and get your personal token "
          "in: https://ai.finlab.tw/api_token/ , then "
          "copy the token in your .env file and named FinLAB_TOKEN.")


if settings.OPENAI_API_KEY is None:
    print("Please register to OpenAI and get your personal token, then "
          "copy the token in your .env file and named OPENAI_API_KEY.")


loop = asyncio.get_event_loop()
