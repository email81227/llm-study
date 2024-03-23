from langchain_community.chat_models import ChatOpenAI
from chatbot.config import settings
from chatbot.callbacks import get_langfuse_callback

# https://platform.openai.com/docs/models


def get_openai_gpt(session_id: str = None, user_id: str = None):
    return ChatOpenAI(
        streaming=True,
        callbacks=[
            get_langfuse_callback(session_id, user_id),
        ],
        model_name="gpt-4-turbo-preview",
        # model_name="gpt-3.5-turbo-0125",
        openai_api_key=settings.OPENAI_API_KEY,
        max_tokens=settings.MAX_TOKENS,
        temperature=0.0
    )

# https://huggingface.co/INX-TEXT/Bailong-instruct-7B
# bailong = ChatOpenAI(
#     streaming=True,
#     callbacks=[
#         get_langfuse_callback(),
#     ],
#     model_name="INX-TEXT/Bailong-instruct-7B",
#     openai_api_base="",
#     openai_api_key="EMPTY",
#     max_tokens=settings.MAX_TOKENS,
#     temperature=0.1,
# )

# https://huggingface.co/MediaTek-Research/Breeze-7B-Instruct-64k-v0_1
# breeze = ChatOpenAI(
#     streaming=True,
#     model_name="MediaTek-Research/Breeze-7B-Instruct-64k-v0_1",
#     openai_api_base="",
#     openai_api_key="EMPTY",
#     max_tokens=settings.MAX_TOKENS,
#     temperature=0.1,
# )


