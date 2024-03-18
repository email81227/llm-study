
import ocrmypdf

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from tqdm import tqdm
from typing import List

from chatbot.config import settings
from chatbot.embeddings import hf_embeddings as embedding
from chatbot.logger import logger
from chatbot.vectorstore import chroma


def pdf_ocr(pdf_path: str, output_path: str):
    ocrmypdf.ocr(
        pdf_path,
        output_path
    )


def _insert2vectordb(docs: List[Document]) -> int:
    logger.info(f"Importing {len(docs)} documents...")
    try:
        chroma.add_documents(docs)
        return 0
    except Exception as e:
        return 1


class PDFProcessor:
    def __init__(self):
        self.loader = None
        self.pages: List[Document]
        self.total_pages: int = 0

    def _content_loader(self, file_path: str):
        logger.info(f"loading from {file_path}")

        # loader = PyPDFLoader(file_path)
        # self.file_name = file_path.split('/')[-1]
        # self.pages = loader.load()
        # self.total_pages = len(self.pages)

        logger.info(f"loaded {self.total_pages} pages.")

    def _text_preprocessor(self):
        logger.info(f"Processing {self.file_name}")
        # for i, page in tqdm(enumerate(self.pages)):
        #     content = page.page_content.replace(" ", "")
        #
        #     # TODO: Add more preprocess
        #
        #     # Replace the original content
        #     self.pages[i].page_content = content

    def _content_split(self) -> List[Document]:
        logger.info(f"Splitting {self.file_name}")
        processed = []
        for i, page in tqdm(enumerate(self.pages)):
            for paragraph in page.page_content.split('\n\n'):
                # TODO: Add more split process
                paragraph = paragraph.strip()

                if paragraph:
                    processed.append(Document(
                        page_content=paragraph,
                        metadata=page.metadata
                    ))

        logger.info(f"Total {len(processed)} paragraphs.")
        return processed

    def run(self, file_path: str):
        # self._content_loader(file_path)
        # self._text_preprocessor()
        # docs = self._content_split()

        loader = file_path.endswith(".pdf") and (
                PyPDFLoader(file_path) or TextLoader(file_path)
        )
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128
        )
        texts = loader.load_and_split(splitter)
        return _insert2vectordb(texts)


if __name__ == '__main__':
    processor = PDFProcessor()
    processor.run('financial_statements/202301_2330_AI1_20240304_021719.pdf')
    processor.run('financial_statements/202302_2330_AI1_20240304_021756.pdf')
