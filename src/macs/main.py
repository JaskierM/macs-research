import os


# from macs.tools.serper_search_tool import get_serper_search_tool
# from macs.tools.travily_search_tool import get_travily_search_tool
# from macs.tools.website_qa_tool import get_website_qa_tool
from macs.llm.ollama import build_ollama_llm, OllamaSettings


ollama_llm = build_ollama_llm()

await ollama_llm.chat(
    messages=[
        {"role": "user", "content": "hello"}
    ]
)

OllamaSettings()


# manager_llm = ChatOllama(
#     model=os.getenv("MANAGER_LLM_MODEL"),
#     base_url=os.getenv("MANAGER_LLM_BASE_URL"),
#     temperature=0.1,
# )
# embeddings_model = OllamaEmbeddings(model=os.getenv("EMBEDDINGS_MODEL"))

base_agent_params = dict(
    model=manager_llm,
    tools=[
        get_serper_search_tool(),
        get_travily_search_tool(),
        get_website_qa_tool(llm=manager_llm, embeddings_model=embeddings_model),
    ],
    debug=True,
)

graph = get_graph("vuln_research_system", base_agent_params)


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

graph.invoke(input_msg)
