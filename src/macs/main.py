import os

from langchain_community.chat_models import ChatOllama
from langchain.embeddings import HuggingFaceEmbeddings

from macs.tools.search_tool import get_search_tool
from macs.tools.scrape_tool import get_scrape_tool
from macs.tools.website_search_tool import get_website_search_tool
from macs.agents.vulnerability_research_agent import get_vulnerability_research_agent
from macs.agents.impact_analyzer_agent import get_impact_analyzer_agent
from macs.agents.recommendation_expert_agent import get_recommendation_expert_agent
from macs.crew.task import Task
from macs.crew.crew import Crew


os.environ["SERPER_API_KEY"] = "c503b47583ccd2816fe20daf79737eff2461b40e"


manager_llm = ChatOllama(model="mistral")
embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

search_tool = get_search_tool()
scrape_tool = get_scrape_tool()
website_search_tool = get_website_search_tool(
    llm=manager_llm, embeddings_model=embeddings_model
)

vulnerability_researcher_agent = get_vulnerability_research_agent(
    manager_llm, [search_tool, scrape_tool, website_search_tool]
)

impact_analyzer_agent = get_impact_analyzer_agent(
    manager_llm, [search_tool, website_search_tool]
)

recommendation_expert_agent = get_recommendation_expert_agent(
    manager_llm, [search_tool, website_search_tool]
)

search_params = {
    "vendor": "Cisco",
    "product": "IOS XE",
    "timeframe": "last 30 days",
    "severity": "Critical",
}

research_task = Task(
    description=f"""
    Research and identify new critical vulnerabilities with the following parameters:
    - Vendor: {search_params['vendor']}
    - Product: {search_params['product']}
    - Timeframe: {search_params['timeframe']}
    - Severity: {search_params['severity']}

    Focus on:
    1. Technical details
    2. Affected systems
    3. Exploitation methods
    4. Patch availability

    Format the result as a structured list.
    """,
    agent=vulnerability_researcher_agent,
    expected_output="Structured vulnerability list",
)

analysis_task = Task(
    description=f"""
    Analyze the vulnerabilities discovered in the previous task.
    For each one, assess:
    - Business impact
    - Risk level (Critical/High/Medium/Low)
    - Potential consequences
    - Affected industries
    """,
    agent=impact_analyzer_agent,
    expected_output="Structed importain ",
)

recommendation_task = Task(
    description=f"""
    Provide a detailed remediation plan for the vulnerabilities found.
    Include:
    - Step-by-step mitigation
    - Temporary workarounds
    - Long-term recommendations
    """,
    agent=recommendation_expert_agent,
    expected_output="Detailed remediation plan",
)

crew = Crew(
    agents=[
        vulnerability_researcher_agent,
        impact_analyzer_agent,
        recommendation_expert_agent,
    ],
    tasks=[research_task, analysis_task, recommendation_task],
    verbose=2,
)

final_report = crew.run()

print("\n=== FINAL MULTIAGENT OUTPUT ===\n")
print(final_report)
