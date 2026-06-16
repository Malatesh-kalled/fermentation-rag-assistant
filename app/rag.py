from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

from app.config import settings
from app.ingestion import build_vector_store
from app.prompts import QA_TEMPLATE, SYSTEM_PROMPT


def format_documents(documents) -> str:
    formatted = []
    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "unknown source")
        page = document.metadata.get("page", "unknown page")
        formatted.append(
            f"[Source {index}: {source}, page {page}]\n{document.page_content}"
        )
    return "\n\n".join(formatted)


def create_rag_chain():
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    vector_store = build_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": settings.top_k})

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", QA_TEMPLATE),
        ]
    )

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.1,
    )

    return (
        {
            "context": retriever | format_documents,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def answer_question(question: str) -> str:
    chain = create_rag_chain()
    return chain.invoke(question)
