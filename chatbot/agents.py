import asyncio
import langchain

from chatbot.callbacks import get_langfuse_callback
from chatbot.llm import gpt
from chatbot.prompts import *
from chatbot.tools import get_tools


async  def get_agent_chain(
        session_id: str = None,
        user_id: str = None,
        stream_callback: callable = None,
        top_k_messages: int = 5,
) -> langchain.agents.AgentChain:
    return


if __name__ == '__main__':
    from datetime import datetime

    loop = asyncio.get_event_loop()

    agent_chain = loop.run_until_complete(
        get_agent_chain()
    )
    loop.close()

    user_query = "Hi there."

    # Execute the query from user
    result = agent_chain.invoke({
        "input": user_query,
        "date": datetime.today().strftime("%Y-%m-%d"),
        "time": datetime.today().strftime("%H:%M:%S"),
    })
