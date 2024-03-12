import os
from langchain_openai import OpenAI
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']


#載入文件
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("202302_2330_AI1_20240309_163214.pdf")
pages = loader.load()
#print(pages)


#longchain splitting
from langchain.text_splitter import TokenTextSplitter

text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(pages)
print(len(docs))
#print(docs[1],pages[1].metadata)


#Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

sentence1 = "第幾年度第幾季財報"
sentence2 = "i like canines"
sentence3 = "the weather is ugly outside"

embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)


#Vectorstores
from langchain.vectorstores import Chroma
persist_directory = 'docs/chroma/'

vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory=persist_directory
)
vectordb.persist()
print(vectordb._collection.count())


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

question = "what did they say about matlab?"
compressed_docs = compression_retriever.get_relevant_documents(question)
print(compressed_docs)


