
from chatbot.config import settings
from finlab import data
import finlab

finlab.login(api_token=settings.FinLAB_TOKEN)


# 企業基本資訊
def get_finlab_company_basic_info():

    basic_info = data.get(
        'company_basic_info',
        save_to_storage=True,
        force_download=False
    )
