import chainlit as cl

from langchain.chains import LLMChain

#
# from chatbot.agents import get_agent_chain
from chatbot.callbacks import get_langfuse_callback
from chatbot.config import settings
from chatbot.split import pdf_preprocess, content_split, content_insert


@cl.on_chat_start
async def on_chat_start():

    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import StrOutputParser

    # Get session ID
    session_id = cl.user_session.get("id")

    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一位美食家，名字叫做食神小當家，你能夠回應任何關於美食的食物與制作以及食譜和食材。",
            ),
            ("human", "{question}"),
        ]
    )

    chain = LLMChain(
        llm=model,
        prompt=prompt,
        callbacks=[
            get_langfuse_callback(
                session_id=session_id, user_id=settings.USER_EMAIL.split("@")[0]
            )
        ],
        output_parser=StrOutputParser(),
    )

    cl.user_session.set("chain", chain)


# @cl.on_chat_start
# async def on_chat_start():
#     session_id = cl.user_session.get("id")

#     # cl.user_session.set(
#     #     "agent",
#     #     await get_agent_chain(
#     #         session_id=session_id, user_id=settings.USER_EMAIL.split("@")[0]
#     #     ),
#     # )

#     cl.user_session.set(
#         "chain",
#         {
#             "session_id": session_id,
#             "user_id": settings.USER_EMAIL.split("@")[0],
#         },
#     )


@cl.on_chat_start
async def ask_for_beginning():
    # Wait for the user to upload a file
    files = await cl.AskFileMessage(
        content="Please upload financial statements to begin!",
        accept=["application/pdf"],
        max_files=10,
        max_size_mb=3,
    ).send()

    # Process the uploaded files as needed
    # Read PDF files
    for file in files:

        # await cl.Message(
        #     content=f"{file_name} uploaded, totaltext \n {totaltext}"
        # ).send()

        # TODO: Run the preprocessing
        processed_content = pdf_preprocess(content)

        # TODO: Split the processed content
        # 處理後得到List[0]=文字資料 List[1]=表格資料
        split_content = content_split(file)

        # TODO: Insert the content to database
        is_insert_content = content_insert()

        # Let the user know that the system is ready


@cl.on_message
async def on_message(message: cl.Message):

    chain = cl.user_session.get("chain")  # type: LLMChain

    res = await chain.arun(
        question=message.content,
        callbacks=[
            cl.LangchainCallbackHandler(),
        ],
    )

    # print(f"message.content={message.content}")

    await cl.Message(content=res).send()
