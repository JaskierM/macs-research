import re

from typing import Type
from langchain.tools import StructuredTool
from langchain_community.document_loaders import WebBaseLoader

from macs.config.tools import ScrapeWebsiteInput
from macs.tools.registry import TOOL_REGISTRY


class ScrapeWebsiteTool(StructuredTool):
    name: str = "scrape_website"
    description: str = "Extracts and cleans all text content from a web page by URL."
    args_schema: Type[ScrapeWebsiteInput] = ScrapeWebsiteInput

    def __init__(self) -> None:
        super().__init__()
        self._web_base_loader = WebBaseLoader

    def _run(self, url: str) -> str:
        try:
            loader = self._web_base_loader(url)
            docs = loader.load()
            if not docs:
                return "No content found."

            doc = docs[0]
            clean_text = f"Source: {doc.metadata.get('source', 'None')}\n"
            clean_text += f"Title: {doc.metadata.get('title', 'None')}\n"
            clean_text += f"Description: {doc.metadata.get('description', 'None')}\n"
            clean_text += f"Language: {doc.metadata.get('language', 'None')}\n"
            clean_text += "-" * 20 + " Text from the site " + "-" * 20 + "\n"

            page_content = doc.page_content
            clean_text += re.sub(r"\n{3,}", "\n\n", page_content)
            clean_text = re.sub(r"[ \t]+", " ", clean_text)
            clean_text = re.sub(r"[ \t]*\n[ \t]*", "\n", clean_text).strip()
            return clean_text

        except Exception as e:
            return f"[ScrapeWebsite error] {e}."

    async def _arun(self, url: str) -> str:
        return self._run(url)


@TOOL_REGISTRY.register("scrape_website")
def build_scrape_website() -> StructuredTool:
    return ScrapeWebsiteTool()
