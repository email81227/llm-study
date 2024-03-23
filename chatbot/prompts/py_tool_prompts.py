

"""
Question to test the prompt PY_COMPUTE_PROMPT:
    "幫我計算150*250的答案"
"""
PY_COMPUTE_PROMPT = (
    "This works for answering the statistics, correlation between sequences, and doing calculations. "
    "You should get the result by print it out with `print(...)` at the end of script.\n"
)

"""
Question to test the prompt PY_PLOT_PROMPT:
    "幫我把 [1, 2, 3, 4, 5, 4, 3, 2, 1] 畫成折線圖"
"""
PY_PLOT_PROMPT = (
    "Useful when the user ask to visualise the data points from sources or provided.\n"
    "First, import the following modules from Plotly as the beginning of input:\n\n"
    "```\n"
    "import pandas as pd\n"
    "import plotly.graph_objects as go\n"
    "import plotly.io as pio\n "
    "```"
    "Next, add the line to get the data and add generate the fig: \n"
    "```fig = go.Figure()```\n```"
    "Finally, print the fig to json for output at the end of script."
    "```print(fig.to_json())```\n"
)
