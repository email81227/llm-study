
import os
import requests
import time

from bs4 import BeautifulSoup
from chatbot.logger import logger
from chatbot.config import settings


def download_report(eq_id: str, year: int, mtype: str = 'F', dtype: str = "F04"):
    """
    Able to download report:
    mtype = "A", dtype = "AI1;  Financial statement
    mtype = "F", dtype = "F04;  股東會年報
    mtype = "F", dtype = "F05;  股東會議事錄

    :param eq_id:
    :param year:
    :param mtype:
    :param dtype:
    :return:
    """
    url = 'https://doc.twse.com.tw/server-java/t57sb01'

    if year // 1000 > 0:
        tw_year = year - 1911
    else:
        tw_year = year

    # Parameters
    data = {
        "id": "",
        "key": "",
        "step": "1",
        "co_id": eq_id,
        "year": tw_year,
        "seamon": "",
        "mtype": mtype,
        "dtype": dtype # F04: 股東會年報, F05: 股東會議事錄, F04: 股東會年報
    }
    try:
        # request data
        response = requests.post(url, data=data)
        # Get file name
        content = BeautifulSoup(response.text, 'html.parser')
        files = content.findAll('a')
        logger.info(f"Get file's link: {[f.text for f in files]}")
    except Exception as e:
        logger.info(f"Error: {e}")
        files = []

    for file in files:
        # Parameters again
        data2 = {
            'step': '9',
            'kind': mtype,
            'co_id': eq_id,
            'filename': file.text  # 檔案名稱
        }
        try:
            # request data
            response = requests.post(url, data=data2)
            link = BeautifulSoup(response.text, 'html.parser')
            # Get PDF url
            file_link = link.find('a').get('href')
            logger.info(f"Get download link {file_link} for {file.text}")
        except Exception as e:
            logger.info(f"Error: {e}")

        # 發送 GET 請求
        try:
            response = requests.get('https://doc.twse.com.tw' + file_link)

            store_path = f"{settings.FS_STORE_PATH}/{dtype}"
            if not os.path.exists(f"{settings.FS_STORE_PATH}/{dtype}"):
                os.makedirs(store_path, exist_ok=True)

            # Download PDF
            with open(f"{store_path}/{year}_{eq_id}_{dtype}-{file.text}.pdf", 'wb') as f:
                f.write(response.content)
            logger.info(f"Download {file.text} successfully. "
                        f"Stored in {store_path}. "
                        f"Named {year}_{eq_id}_{dtype}-{file.text}.pdf")
        except Exception as e:
            logger.info(f"Error: {e}")

        time.sleep(2)


if __name__ == '__main__':
    # Example:

    # Financial statement Q1 - Q4 in 2022, save in {project dir}/data/{AI1}
    download_report("2330", 2022, "A", "AI1")

    # 股東會年報 2022
    download_report("2330", 2022, "F", "F04")

    # 股東會議事錄 2022
    download_report("2330", 2022, "F", "F04")
