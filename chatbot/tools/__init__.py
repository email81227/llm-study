
import langchain

from typing import List

from chatbot.tools.python_tools import (
    python_compute_tool,
    python_plot_tool
)


def get_tools() -> List[langchain.Tool]:
    return [
        python_compute_tool,
        python_plot_tool,
    ]
