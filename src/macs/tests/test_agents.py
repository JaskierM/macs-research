from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.travily_search_tool import get_travily_search_tool
from macs.tools.website_qa_tool import get_website_qa_tool
from macs.agents.vulnerability_research_agent import get_vulnerability_research_agent

load_dotenv()


def test_vulnerability_research_agent(
    vulnerability_research_agent: AgentExecutor, input_query: str
):
    result = vulnerability_research_agent.invoke(
        {"messages": [{"role": "user", "content": input_query}]},
    )
    return result


def test_impact_analyzer_agent(impact_analyzer_agent: AgentExecutor, input_query: str):
    result = impact_analyzer_agent.invoke(
        {"messages": [{"role": "user", "content": input_query}]},
    )
    return result


def test_recommendation_expert_agent(
    recommendation_expert_agent: AgentExecutor, input_query: str
):
    result = recommendation_expert_agent.invoke(
        {"messages": [{"role": "user", "content": input_query}]},
    )
    return result


def main():
    llm = ChatOllama(
        model="llama3.1",
        base_url="http://localhost:11434",
        temperature=0.1,
    )
    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

    serper_search_tool = get_serper_search_tool()
    travily_search_tool = get_travily_search_tool()
    website_qa_tool = get_website_qa_tool(llm=llm, embeddings_model=embeddings_model)

    vulnerability_research_agent = get_vulnerability_research_agent(
        llm=llm,
        tools=[
            serper_search_tool,
            travily_search_tool,
            website_qa_tool,
        ],
    )

    user_query = (
        "Research and identify new critical vulnerabilities with the following parameters:"
        "- Vendor: Cisco"
        "- Timeframe: 2023-2025 years"
        "- Severity: critical"
        "Focus on:"
        "1. Technical details of each vulnerability"
        "2. Affected systems and versions"
        "3. Exploitation methods"
        "4. Current patch status"
        "Format the output as a structured list with clear headers for each vulnerability."
    )

    result = test_vulnerability_research_agent(
        vulnerability_research_agent,
        user_query,
    )
    print(len(result["messages"]))
    print(result["messages"][-1].content)
