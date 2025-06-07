from macs.llm.ollama import build_ollama_llm
from macs.tools.serper_search import build_serper_search
from macs.tools.travily_search import build_tavily_search
from macs.tools.scrape_website import build_scrape_website
from macs.tools.website_qa import build_website_qa_tool


ollama_llm = build_ollama_llm()
ollama_llm_chat = ollama_llm._chat
ollama_llm_embed = ollama_llm._embed


await ollama_llm.chat(messages=[{"role": "user", "content": "hello"}])


serper_search = build_serper_search()
tavily_search = build_tavily_search()
scrape_website = build_scrape_website()


website_qa_tool = build_website_qa_tool(
    llm=ollama_llm_chat, embed_model=ollama_llm_embed
)

serper_search.invoke({"query": "Cybersecurity news"})
tavily_search.invoke({"query": "Cybersecurity news"})
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
print(result)

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
