import asyncio

from langchain.agents import (
    create_structured_chat_agent,
    create_react_agent,
    AgentExecutor
)
from langchain_core.runnables import Runnable
from chatbot.llm import get_openai_get
from chatbot.prompts.agent_prompts import *
from chatbot.tools import get_tools


async def get_agent_chain(
        session_id: str = None,
        user_id: str = None,
) -> Runnable:
    # Get tools
    tools = get_tools()

    agent = create_structured_chat_agent(
        llm=get_openai_get(session_id, user_id),
        tools=tools,
        prompt=STRUCTURE_PROMPT
    )

    # agent = create_react_agent(
    #     llm=get_openai_get(session_id, user_id),
    #     tools=tools,
    #     prompt=REACT_PROMPT
    # )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor


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
