import re

from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Dict

from macs.tools.args_wrappers import structured_tool_wrapper


class ScrapeWebsiteInput(BaseModel):
    url: str = Field(..., description="Web-page URL to scrape")


def _scrape_website(**kwargs) -> str:
    try:
        web_loader = WebBaseLoader(kwargs.get("url", ""))
        docs = web_loader.load()
        if not docs:
            return ""

        doc = docs[0]

        clean_text = f"Source: {doc.metadata.get("source", "None")}\n"
        clean_text += f"Title: {doc.metadata.get("title", "None")}\n"
        clean_text += f"Description: {doc.metadata.get("description", "None")}\n"
        clean_text += f"Language: {doc.metadata.get("language", "None")}\n"
        clean_text += "-" * 20 + " Text from the site " + "-" * 20

        page_content = doc.page_content
        clean_text += re.sub(r"\n{3,}", "\n\n", page_content)
        clean_text = re.sub(r"[ \t]+", " ", clean_text)
        clean_text = re.sub(r"[ \t]*\n[ \t]*", "\n", clean_text)
        clean_text = clean_text.strip()
        return clean_text
    except Exception as e:
        return f"Error: {e}"


def get_scrape_website_tool(
    name: str = "ScrapeWebsiteTool",
    description: str = "Extracts all text from an HTML web-page by URL",
) -> StructuredTool:
    return StructuredTool.from_function(
        func=structured_tool_wrapper(_scrape_website),
        name=name,
        description=description,
        args_schema=ScrapeWebsiteInput,
    )
