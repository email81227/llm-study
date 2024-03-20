
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PDFPlumberLoader
)
from typing import List
from chatbot.logger import logger


def pdf_loader(file, size, overlap):
    logger.info(f"Loading {file}, size: {size}, overlap: {overlap}.")
    loader = PDFPlumberLoader(file)
    doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=size,
      chunk_overlap=overlap
    )
    new_doc = text_splitter.split_documents(doc)
    return new_doc


def pdfs_loader(files: List[str], size, overlap,
                vectordb: str="chroma", embed: str="hf"):
    docs = []
    for file in files:
        docs.extend(pdf_loader(file, size, overlap))

    logger.info(f"Loaded {len(docs)} documents.")
    if embed == "hf":
        from chatbot.embeddings import hf_embeddings
        logger.info(f"Using Huggingface embedding...")
        embedding = hf_embeddings
    else:
        from chatbot.embeddings import openai_ai_embeddings
        logger.info(f"Using OpenAI embedding...")
        embedding = openai_ai_embeddings

    if vectordb == "faiss":
        from langchain_community.vectorstores import FAISS
        logger.info(f"Save to FAISS vector store...")
        return FAISS.from_documents(docs, embedding)
    else:
        from chatbot.vectorstore import chroma
        logger.info(f"Save to Chroma vector store...")
        return chroma.add_documents(docs)


if __name__ == '__main__':
    import glob

    from chatbot.config import settings

    files = glob.glob(f"{settings.FS_STORE_PATH}/*/*")
    pdfs_loader(files=files, size=512, overlap=32, embed="openai")
