
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from chatbot.prompts.retriever_prompts import FinStatementRetrieverPrompt


metadata_field_info = [
    AttributeInfo(
        name="page",
        description="The page of content belong from.",
        type="string",
    ),
    AttributeInfo(
        name="source",
        description="The source document name.",
        type="string",
    ),
]


def self_query_retriever(llm: ChatOpenAI, vectorstore: Chroma) -> Tool:
    retriever = SelfQueryRetriever.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        document_content_description=(
            "The financial statements in quarterly or yearly."
        ),
        metadata_field_info=metadata_field_info,
    )

    return create_retriever_tool(
        retriever,
        "search_financial_statements",
        description=FinStatementRetrieverPrompt,
    )
