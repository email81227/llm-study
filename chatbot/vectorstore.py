

import chromadb
import uuid
from collections import defaultdict
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List

from chatbot.config import settings
from chatbot.embeddings import hf_embeddings as embedding_function

persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection(
    settings.COLLECTION_NAME
)


chroma = Chroma(
    client=persistent_client,
    collection_name=settings.COLLECTION_NAME,
    embedding_function=embedding_function,
)


def chroma_insert(clt: chromadb.Collection, docs: List[Document]) -> None:
    _t = defaultdict(list)