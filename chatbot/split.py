from typing import List
from chatbot.config import settings
import pdfplumber
import pandas as pd


def pdf_preprocess(content: List[str]) -> List[str]:
    return


# TODO: 傳入pdf，處理後得到List[0]=文字資料 List[1]=表格資料
def content_split(file: any) -> List[str]:
    file_name = file.name
    pdf = pdfplumber.open(file.path)  # 開啟 pdf
    # 讀取完整財報pdf內容
    totaltext = ""
    totaltable = ""
    pdf_file_datas = []
    pdf_text_list = []
    pdf_table_list = []
    pdf_page_count = len(pdf.pages)  # 頁數

    print(f"pdf共{pdf_page_count}頁")
    for i in range(len(pdf.pages)):

        print(f"目前第{i+1}頁")
        page = pdf.pages[i]  # 讀取所有頁
        text = page.extract_text()  # 取出文字
        table = page.extract_table()  # 取出表格

        pdf_text_list[:i] = text

        if table != None:
            pdf_table_list[:i] = table
            # df = pd.DataFrame(table[1:], columns=table[0])
            # for column in df:
            #     # df[column] = str(df[column]).replace(" ", "")
            #     # df[column] = str(df[column]).replace("\n", "")
            #     # Select column contents by column
            #     # name using [] operator
            #     columnSeriesObj = df[column]
            #     # print("Column Name : ", column)
            #     # print("Column Contents : ", columnSeriesObj.values)

        totaltext = "".join(str(x) for x in pdf_text_list)
        totaltable = "".join(str(x) for x in pdf_table_list)

        pdf_file_datas[:0] = totaltext
        pdf_file_datas[:1] = totaltable

    return pdf_file_datas


def content_insert() -> bool:
    return
