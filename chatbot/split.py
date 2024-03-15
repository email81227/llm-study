
import ocrmypdf

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from tqdm import tqdm
from typing import List

from chatbot.config import settings
from chatbot.embeddings import hf_embeddings as embedding
from chatbot.logger import logger


def pdf_ocr(pdf_path: str, output_path: str):
    ocrmypdf.ocr(
        pdf_path,
        output_path
    )


class PDFProcessor:
    def __init__(self):
        self.pages: List[Document]
        self.total_pages: int = 0

    def _content_loader(self, file_path: str):
        logger.info(f"loading from {file_path}")

        loader = PyPDFLoader(file_path)
        self.file_name = file_path.split('/')[-1]
        self.pages = loader.load()
        self.total_pages = len(self.pages)

        logger.info(f"loaded {self.total_pages} pages.")

    def _text_preprocessor(self):
        logger.info(f"Processing {self.file_name}")
        for i, page in tqdm(enumerate(self.pages)):
            content = page.page_content.replace(" ", "")

            # TODO: Add more preprocess

            # Replace the original content
            self.pages[i].page_content = content

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
        self._content_loader(file_path)
        self._text_preprocessor()
        return self._content_split()


if __name__ == '__main__':
    from chatbot.vectorstore import chroma, collection
    processor = PDFProcessor()

    docs = (
        [] +
        processor.run('financial_statements/202301_2330_AI1_20240304_021719.pdf') +
        processor.run('financial_statements/202302_2330_AI1_20240304_021756.pdf')
    )

    db = chroma.add(docs)
