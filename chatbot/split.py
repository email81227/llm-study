
import pdfplumber

from langchain.vectorstores import Chroma
from typing import List

from chatbot.config import settings
from chatbot.embeddings import hf_embeddings as embeddings


def pdf_preprocess(content: List[str]) -> List[str]:
    return content


def content_split(content: List[str]) -> List[str]:
    return content


def content_insert(content: List[str]) -> bool:
    return content
