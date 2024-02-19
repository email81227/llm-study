from langchain_community.chat_models import ChatOpenAI
from chatbot.config import settings

# https://platform.openai.com/docs/models
gpt = ChatOpenAI(
    streaming=True,
    callbacks=[
        # get_langchain_callback(),
    ],
    # model_name="gpt-4-turbo-preview",
    model_name="pt-3.5-turbo-0125",
    openai_api_key=settings.OPENAI_API_KEY,
    max_tokens=settings.MAX_TOKENS,
    temperature=0.0
)

# https://huggingface.co/INX-TEXT/Bailong-instruct-7B
bailong = ChatOpenAI(
    streaming=True,
    model_name="INX-TEXT/Bailong-instruct-7B",
    openai_api_base="",
    openai_api_key="EMPTY",
    max_tokens=settings.MAX_TOKENS,
    temperature=0.1,
)

# https://huggingface.co/MediaTek-Research/Breeze-7B-Instruct-64k-v0_1
# breeze = ChatOpenAI(
#     streaming=True,
#     model_name="MediaTek-Research/Breeze-7B-Instruct-64k-v0_1",
#     openai_api_base="",
#     openai_api_key="EMPTY",
#     max_tokens=settings.MAX_TOKENS,
#     temperature=0.1,
# )


