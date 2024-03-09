import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

# Load PDF
import os
#os.chdir('/')  # Colab 換路徑使用

import pdfplumber
file_path= "./202302_2330_AI1_20240309_163214.pdf"
docs = pdfplumber.open(file_path)   # 開啟 pdf
print(docs.pages)  #顯示頁數

#讀取完整財報pdf內容
toteltext = ''
toteltable= ''

for i in range(len(docs.pages)):
  page = docs.pages[i]           # 讀取所有頁
  text = page.extract_text()    # 取出文字
  table = page.extract_table()  # 取出表格
  if table != None:
    toteltable += str(table) 
  toteltext += text 

#打印
path = 'output.txt'
f = open(path, 'w')
print(toteltext, file=f)
print('pdf解析表格'+toteltable, file=f)
f.close()
