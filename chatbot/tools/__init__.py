
from langchain.tools import Tool
from typing import List

from chatbot.tools.python_tools import (
    python_compute_tool,
    python_plot_tool
)

from chatbot.tools.twse_api_tools import (
    t187ap02_L,
    t187ap04_L,
    t187ap17_L,
    t187ap23_L,
    punish,
    BFZFZU_T
)

from chatbot.tools.yfin_api_tools import (
    balance_sheet,
    cashflow,
    dividends,
    income_stmt,
    prices
)

# from chatbot.tools.finlab_tools import


def get_tools() -> List[Tool]:
    return [
        python_compute_tool,
        python_plot_tool,
        t187ap02_L,
        t187ap04_L,
        t187ap17_L,
        t187ap23_L,
        punish,
        BFZFZU_T,
        balance_sheet,
        cashflow,
        dividends,
        income_stmt,
        prices
    ]
