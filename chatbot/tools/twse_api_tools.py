
from langchain_core.tools import StructuredTool
from langchain.docstore.document import Document

import json
import pandas as pd
import requests

from chatbot.prompts.twse_api_prompt import (
    PROMPT_t187ap23_L,
    PROMPT_t187ap04_L
)

# Swagger: https://openapi.twse.com.tw/
TWSE_OPEN_API_URL = "https://openapi.twse.com.tw/v1/"


# 上市公司違反資訊申報、重大訊息及說明記者會規定專區
def open_data_t187ap23_L() -> pd.DataFrame:
    docs = []

    resp = requests.get(
        f'{TWSE_OPEN_API_URL}/opendata/t187ap23_L'
    )

    data = json.loads(resp.text)

    for row in data:
        docs.append(Document(
            page_content=row['違規事由'],
            metadata=row
        ))

    return docs


t187ap23_L = StructuredTool.from_function(
    open_data_t187ap23_L,
    description=PROMPT_t187ap23_L,
    return_direct=False
)


# 上市公司違反資訊申報、重大訊息及說明記者會規定專區
def open_data_t187ap04_L() -> pd.DataFrame:
    docs = []

    resp = requests.get(
        f'{TWSE_OPEN_API_URL}/v1/opendata/t187ap04_L'
    )

    data = json.loads(resp.text)

    for row in data:
        docs.append(Document(
            page_content=row['主旨'],
            metadata=row
        ))
    return docs


t187ap04_L = StructuredTool.from_function(
    open_data_t187ap04_L,
    description=PROMPT_t187ap04_L,
    return_direct=False
)


# TODO:
# 1. /Announcement/BFZFZU_T 投資理財節目異常推介個股
# 2. /opendata/t187ap02_L 上市公司持股逾 10% 大股東名單
# 3. /announcement/punish 集中市場公布處置股票
# 4. /opendata/t187ap17_L 上市公司營益分析查詢彙總表(全體公司彙總報表)

