import os
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
print(docs[1],pages[1].metadata)

'''
#打印
path = 'output.txt'
f = open(path, 'w')
print(toteltext, file=f)
print('pdf解析表格'+toteltable, file=f)
f.close()
'''