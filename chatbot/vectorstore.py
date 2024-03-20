
import chromadb
import os
from langchain_community.vectorstores import Chroma

from chatbot.config import settings
if settings.EMBEDDING_PROVIDER == "OpenAI":
    from chatbot.embeddings import openai_ai_embeddings as embedding_function
else:
    from chatbot.embeddings import hf_embeddings as embedding_function


chroma_client = chromadb.Client()

chroma = Chroma(
    client=chroma_client,
    persist_directory=settings.PERSIST_DIRECTORY,
    collection_name=settings.COLLECTION_NAME,
    embedding_function=embedding_function,
)

if os.path.exists(settings.PERSIST_DIRECTORY):
    chroma.get()
