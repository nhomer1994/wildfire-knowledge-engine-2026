# src/rag/web_search.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

def get_web_search_tool():
    """
    Initialises and returns a free web search tool wrapper
    pre-configured to fetch live breaking news updates.
    """
    print("🌐 Router Engine: Initialising DuckDuckGo Web Search Core...")
    
    # Instantiate the base search API wrapper
    search_api = DuckDuckGoSearchRun()
    
    # Wrap it as a formal LangChain Tool that the agent can read and evaluate
    web_tool = Tool(
        name="live_web_search",
        description=(
            "Use this tool to search the internet for live breaking news updates, "
            "active wildfire updates, weather conditions, or evacuation numbers for 2026. "
            "Input should be a simple search query string."
        ),
        func=search_api.run
    )
    
    return web_tool
