from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain.tools import StructuredTool

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.travily_search_tool import get_travily_search_tool
from macs.tools.scrape_website_tool import get_scrape_website_tool
from macs.tools.website_qa_tool import get_website_qa_tool

load_dotenv()


def test_serper_search_tool(serper_search_tool: StructuredTool):
    result = serper_search_tool.run(
        '{"query": "Latest news on cybersecurity vulnerabilities"}'
    )
    print(result)
    assert result
    result = serper_search_tool.run('{"query": "What is Bitcoin?"}')
    print(result)
    assert result
    result = serper_search_tool.run('{"query": "what does microsoft do now?"}')
    print(result)
    assert result


def test_travily_search_tool(travily_search_tool: StructuredTool):
    result = travily_search_tool.run('{"query": "Cybersecurity vulnerabilities"}')
    print(result)
    assert result
    result = travily_search_tool.run('{"query": "What is Bitcoin?"}')
    print(result)
    assert result
    result = travily_search_tool.run('{"query": "what does microsoft do now?"}')
    print(result)
    assert result


def test_scrape_website_tool(scrape_website_tool: StructuredTool):
    result = scrape_website_tool.run(
        '{"url": "https://python.langchain.com/docs/integrations/text_embedding/ollama/"}'
    )
    print(len(result))
    assert len(result) > 10

    result = scrape_website_tool.run('{"url": "https://securitymedia.org/news/"}')
    print(len(result))
    assert len(result) > 10


def test_website_qa_tool(website_qa_tool: StructuredTool):
    result = website_qa_tool.run(
        '{"url": "https://www.microsoft.com/nl-nl/", "question": "What services does the company offer?"}'
    )
    print(result)
    assert result


def main():
    llm = ChatOllama(
        model="gemma3:4b",
        base_url="http://localhost:11434",
        temperature=0.1,
    )
    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

    serper_search_tool = get_serper_search_tool()
    travily_search_tool = get_travily_search_tool()
    scrape_website_tool = get_scrape_website_tool()
    website_qa_tool = get_website_qa_tool(llm=llm, embeddings_model=embeddings_model)

    test_serper_search_tool(serper_search_tool)
    test_travily_search_tool(travily_search_tool)
    test_scrape_website_tool(scrape_website_tool)
    test_website_qa_tool(website_qa_tool)
