from __future__ import annotations

from typing import Type
from langchain.chains import RetrievalQA
from langchain.tools import StructuredTool
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from macs.config.tools import WebsiteQAInput, WebsiteQAConfig
from macs.provider.registry import PROVIDER_REGISTRY
from macs.tools.registry import TOOL_REGISTRY


class WebsiteQATool(StructuredTool):
    name: str = "website_qa"
    description: str = (
        "Answer a question about the text content of the given web-page URL."
    )
    args_schema: Type[WebsiteQAInput] = WebsiteQAInput
    return_direct: bool = True

    def __init__(self, cfg: WebsiteQAConfig | None = None):
        super().__init__()
        cfg = cfg or WebsiteQAConfig()

        self._provider = PROVIDER_REGISTRY.get(cfg.provider_key)()
        self._embed_model = self._provider.get_embed_model()
        if self._embed_model is None:
            raise ValueError(
                f"Embedding model not found in provider '{cfg.provider_key}'."
            )

        self._chunk_size = cfg.max_chunk_size
        self._overlap = cfg.chunk_overlap

    def _run(self, url: str, question: str) -> str:
        return self._process(url, question)

    async def _arun(self, url: str, question: str) -> str:
        import asyncio

        return await asyncio.to_thread(self._process, url, question)

    def _process(self, url: str, question: str) -> str:
        try:
            docs = WebBaseLoader(url).load()
        except Exception as exc:
            return f"[WebsiteQA error] failed to load page: {exc}."

        if not docs:
            return "No text content found on the page."

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self._chunk_size, chunk_overlap=self._overlap
        )
        chunks = splitter.split_documents(docs)
        vect = FAISS.from_documents(chunks, self._embed_model)

        qa = RetrievalQA.from_chain_type(
            llm=self._provider.get_llm(),
            retriever=vect.as_retriever(),
            return_source_documents=False,
        )
        try:
            return qa.invoke({"query": question})["result"].strip()
        except Exception as exc:
            return f"[WebsiteQA error] {exc}."


@TOOL_REGISTRY.register("website_qa")
def build_website_qa(cfg: WebsiteQAConfig | None = None) -> StructuredTool:
    return WebsiteQATool(cfg)
