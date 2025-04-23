from pydantic import BaseModel, Field
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import StructuredTool

MAX_PAGE_CONTENT = 10000


class ScrapeWebsiteInput(BaseModel):
    url: str = Field(..., description="URL of the page to extract text from")


def scrape_website(url: str) -> str:
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content[:MAX_PAGE_CONTENT]
    except Exception as e:
        return f"Error: {e}"


def get_scrape_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=scrape_website,
        name="ScrapeWebsiteTool",
        description="Extracts text from an HTML page by URL",
        args_schema=ScrapeWebsiteInput,
    )
