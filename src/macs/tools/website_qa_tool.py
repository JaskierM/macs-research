import json

from functools import partial
from pydantic import BaseModel, Field
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.tools import StructuredTool
from langchain_community.vectorstores import FAISS
from typing import Callable, Tuple, Any, Dict


MAX_CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50


class WebsiteQAInput(BaseModel):
    url: str = Field(..., description="Web-page URL")
    question: str = Field(..., description="Any question about the content of the page")


class JSONAwareStructuredTool(StructuredTool):
    def _to_args_and_kwargs(
        self, tool_input: Any, tool_call_id: str | None = None
    ) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                pass

        return super()._to_args_and_kwargs(tool_input, tool_call_id)


def _make_website_qa(llm, embeddings_model) -> Callable[[str, str], str]:

    def _website_qa(url: str, question: str) -> str:
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
            retriever=vectorstore.as_retriever(),
            return_source_documents=False,
        )

        result = qa_chain.invoke({"query": question})
        return result["result"].strip()

    return _website_qa


def get_website_qa_tool(
    *,
    llm,
    embeddings_model,
    name: str = "WebsiteQA",
    description: str = "Answer a specific question about the content of the web‑page located at url",
) -> StructuredTool:

    tool_fn = _make_website_qa(llm, embeddings_model)
    return JSONAwareStructuredTool.from_function(
        func=tool_fn,
        name=name,
        description=description,
        args_schema=WebsiteQAInput,
    )
