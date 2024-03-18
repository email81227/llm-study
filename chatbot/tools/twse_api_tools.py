from typing import List

from langchain_core.tools import StructuredTool
from langchain.docstore.document import Document

import json
import requests

from chatbot.prompts.twse_api_prompt import (
    PROMPT_t187ap23_L,
    PROMPT_t187ap04_L,
    PROMPT_punish,
    PROMPT_BFZFZU_T,
    PROMPT_t187ap17_L,
    PROMPT_t187ap02_L,
)
from chatbot.tools.utils import dict2content, OptionalAssetCode

# Swagger: https://openapi.twse.com.tw/
TWSE_OPEN_API_URL = "https://openapi.twse.com.tw/v1/"


# /opendata/t187ap23_L 上市公司違反資訊申報、重大訊息及說明記者會規定專區
def open_data_t187ap23_L(twse_code: str = None) -> List[Document]:
    """
    ex:
    {
        "出表日期": "1130316",
        "發函日期": "1130307",
        "股票代號": "8499",
        "公司名稱": "鼎炫-KY",
        "違規事由": "鼎炫投資控股股份有限公司（鼎炫-KY，公司代號: 8499）之子公司上海泓進信息技術有限公司於113\r\n年1月3日收到上海市第三中級人民法院(2024)滬03破11號民事裁定書受理其破產清算乙案，經查符合\r\n臺灣證券交易所「對有價證券上市公司重大訊息之查證暨公開處理程序」第4條第1項第5款情事，惟該\r\n公司遲至113年3月6日16時36分始代子公司發布該則重大訊息，核已違反前揭處理程序之規定。",
        "違反資訊申報作業辦法條款": "",
        "違反重大訊息之查證暨公開處理程序條款": "4條1項5款\n",
        "裁罰金額(萬)": "3.0"
    },
    :return:
    """
    docs = {}
    resp = requests.get(f"{TWSE_OPEN_API_URL}/opendata/t187ap23_L")
    data = json.loads(resp.text)

    for row in data:
        if row["出表日期"]:
            docs[row['股票代號']] = Document(
                page_content=dict2content(row),
                metadata={
                    '股票代號': row['股票代號'],
                    '公司名稱': row['公司名稱'],
                    '出表日期': row['出表日期'],
                    '發函日期': row['發函日期'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


# /opendata/t187ap04_L 上市公司每日重大訊息
def open_data_t187ap04_L(twse_code: str = None) -> List[Document]:
    """
    ex: {
        "出表日期": "1130317",
        "發言日期": "1130316",
        "發言時間": "50346",
        "公司代號": "3432",
        "公司名稱": "台端",
        "主旨 ": "依臺灣證券交易所股份有限公司臺證上一字第1121801204\r\n號函辦理",
        "符合條款": "第51款",
        "事實發生日": "1130316",
        "說明": "1.事實發生日:113/03/16\n2.公司名稱:台端興業股份有限公司\n3.與公司關係(請輸入本公司或子公司):本公司\n4.相互持股比例:不適用\n5.發生緣由:依臺灣證券交易所股份有限公司臺證上一字第1121801204號函辦理，每周\n          定期發布重大訊息公告持有之每檔基金餘額、申購與贖回交易情形及應收\n          基金贖回款之收回情形與餘額。\n6.因應措施:\n(一)本公司及子公司依據所投資基金(截至113.03.16止)已公布之最近期淨值計算之投\n    資餘額計美金53,286仟元(折合新台幣1,683,846仟元)，其公允價值評估為0元。\n                                          USD      NTD    公允  交易  發行　\n             基金名稱              簡稱   仟元     仟元   價值  機構  單位\n    =============================  ==== ======  ========= ==== ====== ====\n    Spectra SPC Powerfund          (PF) 21,984    694,702   0    AA    STI\n    Asian Strategic Long Term Fund (GP)  8,151    257,572   0    AA   CCIB\n    Asian Strategic Orient Fund    (GH)  9,099    287,530   0    AA   CCIB\n    Longchamp Absolute Return Unit\n       Trust Fund                  (LC) 14,052    444,042   0  CCAM-N CCAM\n                                        ------  --------- ----\n                                 合計   53,286  1,683,846   0\n                                        ======  ========= ====\n        (1)AA：Ayers Alliance Financial Group Ltd.\n        (2)STI：STI PF Limited\n        (3)CCIB：City Credit Investment Bank Limited\n        (4)CCAM-N：City Credit Asset Management Nominee Co., Ltd.\n        (5)CCAM：CCAM Co., Ltd.\n        (6)已公布之最近期淨值基準日：\n           (PF)=112.02.14 (GP)=112.03.28 (GH)=112.03.30 (LC)=112.07.07\n(二)本公司及子公司本年度截至113.03.16止，無新增申購及贖回基金交易。\n(三)本公司截至113.03.16止，有兩筆尚未收回款項之應收基金贖回款金額計\n    美金2,041仟元(折合新台幣64,486仟元)，其經減損評估後金額為0元。\n      基金簡稱   交易日  USD仟元  NTD仟元 攤銷後成本 交易機構 發行單位\n     =========  =======  ======= ======== ========== ======== ========\n       PF      112.02.15  1,032   32,600        0       AA       STI\n       LC      112.02.20  1,009   31,886        0     CCAM-N    CCAM\n                          ------ -------- ----------\n                    合計  2,041   64,486        0\n                          ====== ======== ==========\n7.其他應敘明事項(若事件發生或決議之主體係屬公開發行以上公司，本則重大訊息同時\n  符合證券交易法施行細則第7條第9款所定對股東權益或證券價格有重大影響之事項):\n(一)本公司將密切注意上述四檔基金後續之發展，並委請專業人士協助本公司主張權利\n    ，以維護全體股東之權益。\n(二)有關於本公司財務業務相關訊息，本公司均依相關規定公告，若有收到進一步通知\n    或其他應公告事項，請投資人依本公司公告之資訊為準。"
    },
    :return:
    """
    docs = {}

    resp = requests.get(f"{TWSE_OPEN_API_URL}/opendata/t187ap04_L")

    data = json.loads(resp.text)

    for row in data:
        if row["出表日期"]:
            docs[row['股票代號']] = Document(
                page_content=dict2content(row),
                metadata={
                    '股票代號': row['股票代號'],
                    '公司名稱': row['公司名稱'],
                    '出表日期': row['出表日期'],
                    '發言日期': row['發言日期'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


# 1. /Announcement/BFZFZU_T 投資理財節目異常推介個股
def announcement_BFZFZU_T(twse_code: str = None) -> List[Document]:
    """
    ex: {
        "Number": "0",
        "Code": "",
        "Name": "",
        "Date": ""
    }
    :return:
    """
    docs = {}
    resp = requests.get(f"{TWSE_OPEN_API_URL}/Announcement/BFZFZU_T")
    data = json.loads(resp.text)

    for row in data:
        if row["Date"]:
            docs[row['Code']] = Document(
                page_content=dict2content(row),
                metadata={
                    'Code': row['Code'],
                    'Name': row['Name'],
                    'Date': row['Date'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


# 2. /opendata/t187ap02_L 上市公司持股逾 10% 大股東名單
def open_data_t187ap02_L(twse_code: str = None) -> List[Document]:
    """
    ex: {
        "出表日期": "1130225",
        "公司代號": "1102",
        "公司名稱": "亞泥",
        "大股東名稱": "遠東新世紀股份有限公司"
    },
    :return:
    """
    docs = {}
    resp = requests.get(f"{TWSE_OPEN_API_URL}/opendata/t187ap02_L")
    data = json.loads(resp.text)

    for row in data:
        if row["出表日期"]:
            docs[row['股票代號']] = Document(
                page_content=dict2content(row),
                metadata={
                    '公司代號': row['公司代號'],
                    '公司名稱': row['公司名稱'],
                    '出表日期': row['出表日期'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


# 2. /announcement/punish 集中市場公布處置股票
def announcement_punish(twse_code: str = None) -> List[Document]:
    """
    ex: {
        "Number": "1",
        "Date": "1130308",
        "Code": "069954",
        "Name": "中興電中信38購01",
        "NumberOfAnnouncement": "1",
        "ReasonsOfDisposition": "連續三次",
        "DispositionPeriod": "113/03/11～113/03/22",
        "DispositionMeasures": "第一次處置",
        "Detail": "１處置原因：該有價證券之交易，連續三個營業日達本公司「公布注意交易資訊」標準。２處置期間：自民國一百十三年三月十一日起至一百十三年三月二十二日﹝十個營業日，如遇：ａ有價證券最後交易日在處置期間，僅處置至最後交易日，ｂ有價證券停止買賣、全日暫停交易則順延執行，ｃ開休市日變動則調整處置迄日〕。３處置措施：ａ以人工管制之撮合終端機執行撮合作業（約每五分鐘撮合一次）。ｂ投資人每日委託買賣該有價證券數量單筆達十交易單位或多筆累積達三十交易單位以上時，應就其當日已委託之買賣，向該投資人收取全部之買進價金或賣出證券。",
        "LinkInformation": "\n提供處置有價證券連結資訊\n1.處置原因：提供公布日期近一個月之「公布注意交易資訊」數據標準\n2.公開資訊觀測站：提供財務業務與重大訊息之精華版資訊\n"
    },
    :return:
    """
    docs = {}
    resp = requests.get(f"{TWSE_OPEN_API_URL}/announcement/punish")
    data = json.loads(resp.text)

    for row in data:
        if row["Date"]:
            docs[row['Code']] = Document(
                page_content=dict2content(row),
                metadata={
                    'Code': row['Code'],
                    'Name': row['Name'],
                    'Date': row['Date'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


# 2. /opendata/t187ap17_L 上市公司營益分析查詢彙總表(全體公司彙總報表)
def open_data_t187ap17_L(twse_code: str = None) -> List[Document]:
    """{
        "出表日期": "1130317",
        "年度": "112",
        "季別": "4",
        "公司代號": "1101",
        "公司名稱": "台泥",
        "營業收入(百萬元)": "109314.34",
        "毛利率(%)(營業毛利)/(營業收入)": "18.78",
        "營業利益率(%)(營業利益)/(營業收入)": "9.18",
        "稅前純益率(%)(稅前純益)/(營業收入)": "13.13",
        "稅後純益率(%)(稅後純益)/(營業收入)": "9.15"
    },

    :return:
    """
    docs = {}
    resp = requests.get(f"{TWSE_OPEN_API_URL}/opendata/t187ap17_L")
    data = json.loads(resp.text)

    for row in data:
        if row["出表日期"]:
            docs[row['公司代號']] = Document(
                page_content=dict2content(row),
                metadata={
                    '公司代號': row['公司代號'],
                    '公司名稱': row['公司名稱'],
                    '出表日期': row['出表日期'],
                    '年度': row['年度'],
                    '季別': row['季別'],
                }
            )

    if twse_code:
        if docs.get(twse_code, None):
            return [docs[twse_code]]
    else:
        return list(docs.values())

    return [Document(
        page_content=f"未找到任何相關資訊"
    )]


t187ap04_L = StructuredTool.from_function(
    open_data_t187ap04_L,
    description=PROMPT_t187ap04_L,
    return_direct=False,
    args_schema=OptionalAssetCode
)


t187ap23_L = StructuredTool.from_function(
    open_data_t187ap23_L,
    description=PROMPT_t187ap23_L,
    return_direct=False,
    args_schema=OptionalAssetCode
)


t187ap02_L = StructuredTool.from_function(
    open_data_t187ap02_L,
    description=PROMPT_t187ap02_L,
    return_direct=False,
    args_schema=OptionalAssetCode
)


t187ap17_L = StructuredTool.from_function(
    open_data_t187ap17_L,
    description=PROMPT_t187ap17_L,
    return_direct=False,
    args_schema=OptionalAssetCode
)


BFZFZU_T = StructuredTool.from_function(
    announcement_BFZFZU_T,
    description=PROMPT_BFZFZU_T,
    return_direct=False,
    args_schema=OptionalAssetCode
)


punish = StructuredTool.from_function(
    announcement_punish,
    description=PROMPT_punish,
    return_direct=False,
    args_schema=OptionalAssetCode
)
