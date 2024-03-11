import asyncio

from functools import lru_cache
from pydantic_settings import BaseSettings

try:
    import torch

    if torch.cuda.is_available():
        DEVICE = 'gpu'
    else:
        DEVICE = 'cpu'

except ModuleNotFoundError:
    DEVICE = 'cpu'


class Settings(BaseSettings):

    FORCE_OCR_PDF: bool = True

    DEVICE: str = DEVICE
    EMBEDDING_MODEL: str = "sentence-transformers/LaBSE"
    # EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str

    MEMORY_KEY: str = "chat_history"
    MAX_TOKENS: int = 2048

    USER_NAME: str
    USER_EMAIL: str
    OPENAI_API_KEY: str

    class Config:
        case_sensitive = True
        extra = "allow"
        env_file = ".env"


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()


loop = asyncio.get_event_loop()
