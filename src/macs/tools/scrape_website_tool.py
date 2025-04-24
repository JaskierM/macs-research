import re

from pydantic import BaseModel, Field
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field, HttpUrl
from typing import Union


class ScrapeWebsiteInput(BaseModel):
    url: Union[str, HttpUrl] = Field(
        ..., description="URL of the page to extract text from"
    )


def _scrape_website(url: str) -> str:
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        if not docs:
            return ""
        raw_text = docs[0].page_content
        clean_text = re.sub(r"\n{3,}", "\n\n", raw_text)
        return clean_text
    except Exception as e:
        return f"Error: {e}"


def get_scrape_website_tool(
    name: str = "ScrapeWebsiteTool",
    description: str = "Extracts all text from an HTML page by URL",
) -> StructuredTool:
    return StructuredTool.from_function(
        func=_scrape_website,
        name=name,
        description=description,
        args_schema=ScrapeWebsiteInput,
    )
