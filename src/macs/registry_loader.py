def register_all():
    from macs.llm_clients.ollama import build_ollama_llm_client
    
    from macs.tools.serper_search import build_serper_search
    from macs.tools.travily_search import build_tavily_search
    from macs.tools.scrape_website import build_scrape_website
    from macs.tools.website_qa import build_website_qa
    
    from macs.agents.vuln_researcher import build_vuln_researcher
    from macs.agents.impact_analyzer import build_impact_analyzer
    from macs.agents.recommendation_expert import build_recommendation_expert
    
    from macs.graph.vuln_research import build_vuln_research
    