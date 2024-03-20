
from langchain.tools.retriever import create_retriever_tool
from chatbot.prompts.retriever_prompts import RetrieverPrompt


def get_vector_db_retriever():
    from chatbot.vectorstore import chroma

    return chroma.as_retriever()


search_document_tool = create_retriever_tool(
    get_vector_db_retriever(),
    "search_company_release",
    RetrieverPrompt,
)
