import chainlit as cl

from langchain.chains import LLMChain

#
from chatbot.agents import get_agent_chain
from chatbot.callbacks import get_langfuse_callback
from chatbot.config import settings
from chatbot.split import pdf_preprocess, content_split, content_insert


# @cl.on_chat_start
# async def on_chat_start():
#     from langchain.chat_models import ChatOpenAI
#     from langchain.prompts import ChatPromptTemplate
#     from langchain.schema import StrOutputParser
#     # Get session ID
#     session_id = cl.user_session.get("id")
#
#     model = ChatOpenAI(streaming=True)
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
#             ),
#             ("human", "{question}"),
#         ]
#     )
#     chain = LLMChain(
#         llm=model,
#         prompt=prompt,
#         callbacks=[
#             get_langfuse_callback(
#                 session_id=session_id,
#                 user_id=settings.USER_EMAIL.split("@")[0]
#             )
#         ],
#         output_parser=StrOutputParser()
#     )
#
#     cl.user_session.set("chain", chain)


@cl.on_chat_start
async def on_chat_start():
    session_id = cl.user_session.get("id")

    cl.user_session.set(
        "agent",
        await get_agent_chain(
            session_id=session_id,
            user_id=settings.USER_EMAIL.split("@")[0]
        )
    )


@cl.on_chat_start
async def ask_for_beginning():
    # Wait for the user to upload a file
    files = await cl.AskFileMessage(
        content="Please upload financial statements to begin!",
        accept=["application/pdf"],
        max_files=10
    ).send()

    # Process the uploaded files as needed
    for file in files:
        # Read PDF files
        with open(file.path, "rb") as pdf:
            content = pdf.read()

        # TODO: Run the preprocessing
        processed_content = pdf_preprocess(content, )

        # TODO: Split the processed content
        split_content = content_split(processed_content)

        # TODO: Insert the content to database
        insert_content = content_insert(split_content)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: LLMChain

    res = await chain.arun(
        question=message.content,
        callbacks=[
            cl.LangchainCallbackHandler(),
        ]
    )

    await cl.Message(content=res).send()

