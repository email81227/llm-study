import asyncio
import os

from functools import lru_cache
from pydantic_settings import BaseSettings

try:
    import torch

    if torch.cuda.is_available():
        DEVICE = 'cuda'
    else:
        DEVICE = 'cpu'

except ModuleNotFoundError:
    DEVICE = 'cpu'


class Settings(BaseSettings):
    # FinLAB_TOKEN: str

    FORCE_OCR_PDF: bool = True

    DEVICE: str = DEVICE
    EMBEDDING_PROVIDER: str = "OpenAI"
    # EMBEDDING_PROVIDER: str = "HF"
    # EMBEDDING_MODEL: str = "sentence-transformers/LaBSE"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    COLLECTION_NAME: str = "FinState"
    PERSIST_DIRECTORY: str = 'chroma/FinState'
    FS_STORE_PATH: str = 'data'

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


if not os.path.exists(settings.FS_STORE_PATH):
    os.makedirs(settings.FS_STORE_PATH, exist_ok=True)


@lru_cache()
def get_settings():
    return Settings()


# if settings.FinLAB_TOKEN is None:
#     print("Please register to FinLAB and get your personal token "
#           "in: https://ai.finlab.tw/api_token/ , then "
#           "copy the token in your .env file and named FinLAB_TOKEN.")


if settings.OPENAI_API_KEY is None:
    print("Please register to OpenAI and get your personal token, then "
          "copy the token in your .env file and named OPENAI_API_KEY.")


loop = asyncio.get_event_loop()
