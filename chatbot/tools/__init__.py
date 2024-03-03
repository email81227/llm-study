
from langchain.tools import Tool
from typing import List

from chatbot.tools.python_tools import (
    python_compute_tool,
    python_plot_tool
)


def get_tools() -> List[Tool]:
    return [
        python_compute_tool,
        python_plot_tool,
    ]
