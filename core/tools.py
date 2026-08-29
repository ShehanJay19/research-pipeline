import os
from dotenv import load_dotenv
from tavily import TavilyClient
from core.budget import budget
load_dotenv()
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def web_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return a list of {title, url, content} dicts."""
    budget.check_search_budget()
    
    response = tavily_client.search(query=query, max_results=max_results)
    budget.record_search_call()
    return [
        {"title": r["title"], "url": r["url"], "content": r["content"]}
        for r in response["results"]
    ]