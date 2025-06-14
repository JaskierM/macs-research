def register_all():
    from macs.llm_clients.ollama import build_ollama_llm_client
    
    from macs.tools.serper_search import build_serper_search
    from macs.tools.travily_search import build_tavily_search
    from macs.tools.scrape_website import build_scrape_website
    from macs.tools.website_qa import build_website_qa
    