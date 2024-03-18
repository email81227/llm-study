
from langchain_community.embeddings import HuggingFaceEmbeddings

from chatbot.config import settings


hf_embeddings = HuggingFaceEmbeddings(
    model_name=settings.EMBEDDING_MODEL,
    model_kwargs={'device': settings.DEVICE},
    encode_kwargs={'normalize_embeddings': False}
)


if __name__ == '__main__':
    text = "This is a test document."
    query_result = hf_embeddings.embed_query(text)

    print(query_result)
