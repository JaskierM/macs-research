from macs.registry_loader import register_all

register_all()

from macs.llm_clients.registry import get_llm_client
from macs.tools.registry import get_tool

ollama_llm_client = get_llm_client("ollama")

ollama_llm_client.llm
ollama_llm_client.embed_model

response = await ollama_llm_client.chat(
    messages=[{"role": "user", "content": "What llm model do you use?"}]
)

serper_search = get_tool("serper_search")
tavily_search = get_tool("tavily_search")
scrape_website = get_tool("scrape_website")
website_qa_tool = get_tool("website_qa")

result = serper_search.invoke({"query": "Cybersecurity news"})
result = tavily_search.invoke({"query": "Cybersecurity news"})
result = scrape_website.invoke(
    {
        "url": "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C"
    }
)
result = website_qa_tool.invoke(
    {
        "url": "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F_%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C",
        "question": "What are the most common prevention systems?",
    }
)

# vuln_researcher = build_vuln_researcher()


# input_msg = {
#     "input": "Research and identify new critical vulnerabilities with the following parameters:"
#     "- Vendor: Cisco"
#     "- Timeframe: 2025"
#     "- Severity: critical"
#     "Focus on:"
#     "1. Technical details of each vulnerability"
#     "2. Affected systems and versions"
#     "3. Exploitation methods"
#     "4. Current patch status"
#     "Format the output as a structured list with clear headers for each vulnerability."
# }


# response = vuln_researcher.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Какие критические уязвимости были найдены в Chrome в июне 2024 года?",
#             }
#         ]
#     }
# )

# print(response["messages"][-1].content)
