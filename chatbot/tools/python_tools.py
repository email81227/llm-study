import ast
import asyncio
import re

import chainlit as cl
import plotly.io as pio
import sys

from contextlib import redirect_stdout
from io import StringIO
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_experimental.tools import PythonREPLTool
from langchain.pydantic_v1 import BaseModel, Field, root_validator
from langchain.tools.base import BaseTool
from typing import Any, Dict, Optional, Type

from chatbot.prompts.py_tool_prompts import PY_COMPUTE_PROMPT, PY_PLOT_PROMPT


def sanitize_input(query: str) -> str:
    """Sanitize input to the python REPL.
    Remove whitespace, backtick & python (if llm mistakes python console as terminal)

    Args:
        query: The query to sanitize

    Returns:
        str: The sanitized query
    """

    # Removes `, whitespace & python from start
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    # Removes whitespace & ` from end
    query = re.sub(r"(\s|`)*$", "", query)
    return query


class PythonInputs(BaseModel):
    query: str = Field(
        description=(
            "Code snippet to run. "
            "If the data is stored, use `pd.load_csv` rather than print "
            "dataset directly."
        )
    )


class PlotlyPythonAstREPLTool(BaseTool):
    """A tool for running python code in a REPL to generate plotly charts."""

    name: str = "plotly_python_repl_ast"
    description: str = PY_PLOT_PROMPT

    globals: Optional[Dict] = Field(default_factory=dict)
    locals: Optional[Dict] = Field(default_factory=dict)
    sanitize_input: bool = True
    args_schema: Type[BaseModel] = PythonInputs

    @root_validator(pre=True)
    def validate_python_version(cls, values: Dict) -> Dict:
        """Validate valid python version."""
        if sys.version_info < (3, 9):
            raise ValueError(
                "This tool relies on Python 3.9 or higher "
                "(as it uses new functionality in the `ast` module, "
                f"you have Python version: {sys.version}"
            )
        return values

    @staticmethod
    def send_chart_and_return(chart):
        print("converting to chart:", chart)
        try:
            fig = pio.from_json(chart)
            cl.user_session.set("figure", fig)
            return (
                "Chart successfully sent to the user. "
                "Do not show any image in your reply, "
                "only present the chart that has been already sent."
            )
        except Exception as e:
            print(e)
            return e

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        try:
            if self.sanitize_input:
                query = sanitize_input(query)
            tree = ast.parse(query)
            module = ast.Module(tree.body[:-1], type_ignores=[])
            exec(ast.unparse(module), self.globals, self.locals)  # type: ignore
            module_end = ast.Module(tree.body[-1:], type_ignores=[])
            module_end_str = ast.unparse(module_end)  # type: ignore
            io_buffer = StringIO()
            try:
                with redirect_stdout(io_buffer):
                    ret = eval(
                        module_end_str,
                        self.globals,
                        self.locals,
                    )
                    if ret is None:
                        return self.send_chart_and_return(io_buffer.getvalue())
                    else:
                        return self.send_chart_and_return(ret)
            except Exception:
                with redirect_stdout(io_buffer):
                    exec(module_end_str, self.globals, self.locals)
                return io_buffer.getvalue()
        except Exception as e:
            return "{}: {}".format(type(e).__name__, str(e))

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._run, query)

        return result


python_compute_tool = PythonREPLTool(description=PY_COMPUTE_PROMPT)

python_plot_tool = PlotlyPythonAstREPLTool()
