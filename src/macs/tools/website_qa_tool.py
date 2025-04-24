from functools import partial
from pydantic import BaseModel, Field, HttpUrl
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.tools import StructuredTool
from typing import Union
from langchain_community.vectorstores import FAISS


MAX_CHUNK_SIZE: int = 800
CHUNK_OVERLAP: int = 80


class WebsiteQAInput(BaseModel):
    url: Union[str, HttpUrl] = Field(..., description="Full URL of the page")
    question: str = Field(..., description="Natural‑language question about that page")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://example.com/advisory.html",
                    "question": "What products are affected?",
                }
            ]
        }
    }


def _website_qa(url: str, question: str, *, llm, embeddings_model):
    try:
        docs = WebBaseLoader(url).load()
    except Exception as e:
        return f"Error: {e}"

    if not docs:
        return "Could not download or parse the page; no text content available."

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=MAX_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings_model)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=False,
    )

    result = qa_chain.invoke({"query": question})

    return result["result"].strip()


def get_website_qa_tool(
    *,
    llm,
    embeddings_model,
    name: str = "website_qa",
    description: str | None = None,
) -> StructuredTool:
    description = description or (
        "Answer a **specific question** about the content of the web‑page located "
        "at `url`.\n\n"
        "Arguments:\n"
        "- **url** *(string)* – full URL of the page.\n"
        "- **question** *(string)* – what you want to know."
    )

    tool_fn = partial(_website_qa, llm=llm, embeddings_model=embeddings_model)

    return StructuredTool.from_function(
        func=tool_fn,
        name=name,
        description=description,
        args_schema=WebsiteQAInput,
        return_direct=False,
    )
