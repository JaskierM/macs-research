from __future__ import annotations

import json

from typing import Any, Dict, Tuple, Type
from langchain.chains import RetrievalQA
from langchain.tools import StructuredTool
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from macs.config.tools import WebsiteQAInput, WebsiteQASettings
from macs.tools.registry import TOOL_REGISTRY


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


class WebsiteQATool(JSONAwareStructuredTool):
    name: str = "website_qa"
    description: str = (
        "Answer a specific question about the text content of the web‑page located at the provided URL."
    )
    args_schema: Type[WebsiteQAInput] = WebsiteQAInput

    def __init__(
        self,
        *,
        llm,
        embed_model,
        settings: WebsiteQASettings | None = None,
    ) -> None:
        super().__init__()
        self._llm = llm
        self._embed_model = embed_model
        self._settings = settings or WebsiteQASettings()

    def _run(self, url: str, question: str) -> str:
        return self._process(url, question)

    async def _arun(self, url: str, question: str) -> str:
        import asyncio

        return await asyncio.to_thread(self._process, url, question)

    def _process(self, url: str, question: str) -> str:
        max_chunk = self._settings.max_chunk_size
        overlap = self._settings.chunk_overlap

        try:
            docs = WebBaseLoader(url).load()
        except Exception as exc:
            return f"[WebsiteQA error] failed to load page: {exc}"

        if not docs:
            return "Unable to scrape or parse the page; no text content found."

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=max_chunk, chunk_overlap=overlap
        )
        chunks = splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, self._embed_model)

        qa_chain = RetrievalQA.from_chain_type(
            llm=self._llm,
            retriever=vectorstore.as_retriever(),
            return_source_documents=False,
        )

        try:
            res = qa_chain.invoke({"query": question})
            return res["result"].strip()
        except Exception as exc:
            return f"[WebsiteQA error] {exc}"


@TOOL_REGISTRY.register("website_qa")
def build_website_qa_tool(*, llm, embed_model) -> StructuredTool:
    return WebsiteQATool(llm=llm, embed_model=embed_model)
