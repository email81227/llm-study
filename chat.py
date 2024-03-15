from collections import defaultdict

import chainlit as cl

from datetime import datetime
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableConfig

#
from chatbot.agents import get_agent_chain
from chatbot.config import settings
from chatbot.split import PDFProcessor, content_insert


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

    # Wait for the user to upload a file
    files = await cl.AskFileMessage(
        content="Please upload financial statements to begin!",
        accept=["application/pdf"],
        max_files=10,
        max_size_mb=50,
    ).send()

    file_state = defaultdict(bool)

    # Process the uploaded files as needed
    processor = PDFProcessor()
    paragraphs = []
    for file in files:
        # Read PDF files
        try:
            docs = processor.run(file)

            paragraphs += docs

            file_state[file.name] = True
        except Exception as e:
            file_state[file.name] = False

    # Let the user know that the system is ready
    success_file = ', '.join([k for k, v in file_state.items() if v])
    failed_file = ', '.join([k for k, v in file_state.items() if not v])

    message = f"{success_file} are uploaded successfully."
    if failed_file:
        message += f"{failed_file} are failed."

    await cl.Message(
        content=message
    ).send()


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

    res: dict = await cl.make_async(agent.invoke)(
        {
            "input": message.content,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
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


