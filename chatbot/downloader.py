
from typing import Any, List, Optional, Tuple

import pandas as pd
import requests

from bs4 import BeautifulSoup


# https://mops.twse.com.tw/server-java/t164sb01?SYEAR=2023&file_name=tifrs-fr1-m1-ci-cr-2330-2023Q4.html#BalanceSheet
def download_fs(eq_code: str, year: int=2023, season: int=4):
    season = f"Q{season}"

    url = (
        f"https://mops.twse.com.tw/server-java/"
        f"t164sb01?SYEAR={year}&"
        f"file_name=tifrs-fr1-m1-ci-cr-{eq_code}-{year}{season}.html"
    )

    resp = requests.get(url)

    if resp.status_code != 200:
        return

    extract_fs(resp)


def columns_name_handler(columns: Any) -> Tuple[Any, List[str]]:
    tab_name = None
    col_names = []

    if isinstance(columns, pd.MultiIndex):
        for tab_name, col_name in columns:
            col_names.append(col_name)

        return tab_name, col_names
    else:
        return None, list(columns)


# def extract_balance_sheet(tab: pd.DataFrame) -> pd.DataFrame:
#     tab_name, cols = columns_name_handler(tab.columns)
#
#     seq_terms = []
#     top_terms = ['資產Assets', '負債及權益liabilities and equity']
#     for il, row in tab.iterrows():
#         elements = row.values
#         if pd.isna(elements[0]):
#             seq_terms.append(seq_terms)
#
#     return


def clean_soup(content):
    for tags in content.findAll(True):
        tags.attrs = {}
    return content


# 財務報表索引
def extract_fs(soup: BeautifulSoup):
    # body > div.container > div.content > span:nth-child(21) > table
    sub_soup = soup.select(
        'body > div.container > div.content > span:nth-child(21) > table'
    )[0]


