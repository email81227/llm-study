from collections import defaultdict

import chainlit as cl

from datetime import datetime
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableConfig

#
from chatbot.agents import get_agent_chain
from chatbot.config import settings


@cl.on_chat_start
async def on_chat_start():
    session_id = cl.user_session.get("id")

    # Add agent to chainlit
    cl.user_session.set(
        "agent",
        await get_agent_chain(
            session_id=session_id,
            user_id=settings.USER_EMAIL.split("@")[0]
        )
    )

    # Add memory to chainlit
    cl.user_session.set(
        "memory",
        ConversationBufferMemory(return_messages=True)
    )


@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory

    chainlit_callback = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["Answer", ":"],
        to_ignore=["Answer", ":"],
    )

    # Getting the current date and time
    now = datetime.now()
    tw_year = now.year - 1911

    res: dict = await cl.make_async(agent.invoke)(
        {
            "input": message.content,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "tw_year": tw_year,
        },
        config=RunnableConfig(
            callbacks=[chainlit_callback]
        )
    )

    elements = []
    figure = cl.user_session.get("figure")
    if figure:
        elements.append(
            cl.Plotly(name="chart", figure=figure, display="inline")
        )

    await cl.Message(
        content=res.get('output'),
        elements=elements
    ).send()

    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res.get('output'))


