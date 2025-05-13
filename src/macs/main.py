from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.travily_search_tool import get_travily_search_tool
from macs.tools.website_qa_tool import get_website_qa_tool
from macs.agents.vulnerability_research_agent import get_vulnerability_research_agent
from macs.agents.impact_analyzer_agent import get_impact_analyzer_agent
from macs.agents.recommendation_expert_agent import get_recommendation_expert_agent
from macs.graph.graph_builder import GraphBuilder

load_dotenv()


manager_llm = ChatOllama(
    model="llama3.1",
    base_url="http://localhost:11434",
    temperature=0.1,
)
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

serper_search_tool = get_serper_search_tool()
tavily_search_tool = get_travily_search_tool()
website_qa_tool = get_website_qa_tool(
    llm=manager_llm, embeddings_model=embeddings_model
)

vulnerability_research_agent = get_vulnerability_research_agent(
    model=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        website_qa_tool,
    ],
)

impact_analyzer_agent = get_impact_analyzer_agent(
    model=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        website_qa_tool,
    ],
)

recommendation_expert_agent = get_recommendation_expert_agent(
    model=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        website_qa_tool,
    ],
)


input_msg = {
    "input": "Research and identify new critical vulnerabilities with the following parameters:"
    "- Vendor: Cisco"
    "- Timeframe: 2025"
    "- Severity: critical"
    "Focus on:"
    "1. Technical details of each vulnerability"
    "2. Affected systems and versions"
    "3. Exploitation methods"
    "4. Current patch status"
    "Format the output as a structured list with clear headers for each vulnerability."
}

graph_builder = GraphBuilder(
    vulnerability_research_agent=vulnerability_research_agent,
    impact_analyzer_agent=impact_analyzer_agent,
    recommendation_expert_agent=recommendation_expert_agent,
)
graph = graph_builder.build()

result = graph.invoke(input_msg, config={"verbose": True})

result
print(result["vulnerabilities_report"])
print(result["impact_analysis"])
print(result["recommendation"])
