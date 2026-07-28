# src/rag/web_search.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# Initialize the underlying search run instance once to save memory
_search_instance = DuckDuckGoSearchRun()

@tool("live_web_search")
def get_web_search_tool(query: str) -> str:
    """
    Use this tool to search the internet for live breaking news updates, 
    active wildfire updates, weather conditions, or evacuation numbers for 2026. 
    Input should be a simple search query string focusing on location names.
    """
    # Force the query to run through the base instance string parser
    return _search_instance.run(query)
