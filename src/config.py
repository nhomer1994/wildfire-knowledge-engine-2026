# src/config.py
import os
from langchain_openrouter import ChatOpenRouter

def get_llm():
    """
    Initialises and returns a LangChain chat model wrapper.
    Uses the 'openrouter/free' slug to dynamically fallback to 
    the best available zero-cost model on the OpenRouter platform.
    """
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    
    if openrouter_key:
        print("🤖 System Status: Initialising OpenRouter Auto-Free Router...")
        return ChatOpenRouter(
            openrouter_api_key=openrouter_key,
            # This dynamic endpoint handles underlying model name rotations automatically
            model_name="openrouter/free",
            temperature=0
        )
    else:
        raise ValueError(
            "CRITICAL ERROR: No OPENROUTER_API_KEY environment secret detected! "
            "Please check your GitHub Codespaces Secrets configuration."
        )
