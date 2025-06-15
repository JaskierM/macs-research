from macs.registry_loader import register_all

register_all()

from macs.llm_clients.registry import get_llm_client
from macs.tools.registry import get_tool
from macs.agents.registry import get_agent
from macs.graph.registry import get_graph

# ollama_llm_client = get_llm_client("ollama")


# response = await ollama_llm_client.chat(
#     messages=[{"role": "user", "content": "What llm model do you use?"}]
# )

# serper_search = get_tool("serper_search")
# tavily_search = get_tool("tavily_search")
# scrape_website = get_tool("scrape_website")
# website_qa_tool = get_tool("website_qa")

# result = serper_search.invoke({"query": "Cybersecurity news"})
# result = tavily_search.invoke({"query": "Cybersecurity news"})
# result = scrape_website.invoke(
#     {
#         "url": "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C"
#     }
# )
# result = website_qa_tool.invoke(
#     {
#         "url": "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C",
#         "question": "What are the most common prevention systems?",
#     }
# )

# vuln_researcher = get_agent("vuln_researcher")

input_msg = (
    "Research and identify new critical vulnerabilities with the following parameters:"
    "- Vendor: Cisco"
    "- Timeframe: 2025"
    "- Severity: critical"
    "Focus on:"
    "1. Technical details of each vulnerability"
    "2. Affected systems and versions"
    "3. Exploitation methods"
    "4. Current patch status"
    "Format the output as a structured list with clear headers for each vulnerability."
)

vuln_research = get_graph("vuln_research")

result = await vuln_research.ainvoke(
    {
        "messages": [{"role": "user", "content": input_msg}],
        "session_id": "1",
    },
    config={"configurable": {"thread_id": "1"}},
)

vuln_research.get_graph().nodes
vuln_research.get_state(config={"configurable": {"thread_id": "1"}}).values

