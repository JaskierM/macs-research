import os

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.scrape_website_tool import get_scrape_website_tool
from macs.tools.website_qa_tool import get_website_qa_tool
from langchain_community.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings


os.environ["SERPER_API_KEY"] = "c503b47583ccd2816fe20daf79737eff2461b40e"


def test_serper_search_tool():
    serper_search_tool = get_serper_search_tool()

    result = serper_search_tool.run("Latest news on cybersecurity vulnerabilities")
    print(result)
    assert result
    result = serper_search_tool.run("What is Bitcoin?")
    print(result)
    assert result
    result = serper_search_tool.run("what does microsoft do now?")
    print(result)
    assert result


def test_scrape_website_tool():
    scrape_website_tool = get_scrape_website_tool()

    result = scrape_website_tool.run(
        "https://python.langchain.com/docs/integrations/text_embedding/ollama/"
    )
    print(result)
    assert len(result) > 10

    result = scrape_website_tool.run("https://securitymedia.org/news/")
    print(result)
    assert len(result) > 10


def test_website_qa_tool():
    llm = ChatOllama(
        model="llama3.1",
        base_url="http://localhost:11434",
        temperature=0.1,
    )
    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

    website_qa_tool = get_website_qa_tool(
        llm=llm,
        embeddings_model=embeddings_model,
    )

    query = {
        "url": "https://www.microsoft.com/nl-nl/",
        "question": "What services does the company offer?",
    }
    result = website_qa_tool.run(query)
    print(result)
    assert len(result) > 10

    query = {
        "question": "What command can i use to start the agent?",
        "url": "https://python.langchain.com/docs/tutorials/agents/",
    }
    result = website_qa_tool.run(query)
    print(result)
    assert len(result) > 10


def main():
    test_serper_search_tool()
    test_scrape_website_tool()
    test_website_qa_tool()
