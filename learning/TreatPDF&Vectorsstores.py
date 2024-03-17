import os
from langchain_openai import OpenAI
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"
print(llm_name)


#載入文件
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("202302_2330_AI1_20240309_163214.pdf")
pages = loader.load()
#print(pages)


#longchain splitting
from langchain.text_splitter import TokenTextSplitter

text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(pages)
print(len(docs))
#print(docs[1],pages[1].metadata)


def pretty_print_docs(docs):
    print(f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]))

# 建立vector db
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=docs, embedding=embedding)
retriever_vector = vectordb.as_retriever()


#索引方式-compression上下文壓縮

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Wrap our vectorstore
llm = OpenAI(temperature=0, model="gpt-3.5-turbo-instruct")
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectordb.as_retriever()
)

question = "這財報介紹了哪些內容？"
compressed_docs = compression_retriever.get_relevant_documents(question)
print(compressed_docs)
