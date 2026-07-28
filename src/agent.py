# src/agent.py
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.config import get_llm
from src.rag.retriever import get_internal_knowledge_tool
from src.server.tools import calculate_regional_burn_severity
from src.rag.web_search import get_web_search_tool

class SatelliteInput(BaseModel):
    min_lon: float = Field(..., description="Minimum longitude bounding coordinate float")
    min_lat: float = Field(..., description="Minimum latitude bounding coordinate float")
    max_lon: float = Field(..., description="Maximum longitude bounding coordinate float")
    max_lat: float = Field(..., description="Maximum latitude bounding coordinate float")

@tool("satellite_burn_severity_analyzer", args_schema=SatelliteInput)
def structured_satellite_tool(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> str:
    """
    Calculates the mean Normalized Burn Ratio (NBR) from active Sentinel-2 
    satellite arrays over a bounding box to determine physical vegetation damage.
    """
    return calculate_regional_burn_severity(min_lon, min_lat, max_lon, max_lat)

class WildfireAgentExecutor:
    """Production-grade multi-modal tool orchestration loop."""
    def __init__(self):
        print("🧠 Orchestrator: Initialising Structured Agent Core...")
        self.llm = get_llm()
        
        # Instantiate your tool pool
        self.web_tool = get_web_search_tool
        self.rag_tool = get_internal_knowledge_tool
        self.geo_tool = structured_satellite_tool
        
        # Map tools into a strict routing index map
        self.tools_map = {
            self.web_tool.name: self.web_tool,
            self.rag_tool.name: self.rag_tool,
            self.geo_tool.name: self.geo_tool
        }
        
        # Formally bind tools to inference context channels to pass clean schemas
        self.llm_with_tools = self.llm.bind_tools([self.web_tool, self.rag_tool, self.geo_tool])

    def invoke(self, data_input: dict) -> dict:
        user_input = data_input.get("input", "")
        
        system_prompt = (
            "You are the Wildfire Intelligence Knowledge Engine for the 2026 European Crisis.\n\n"
            "CRITICAL OPERATIONAL BLUEPRINT:\n"
            "1. If the prompt contains explicit coordinates (Lon/Lat bounds), you MUST trigger 'satellite_burn_severity_analyzer'. Do not skip this step.\n"
            "2. Gather ground context using 'live_web_search' or 'internal_knowledge_base'.\n"
            "3. Synthesise data blocks into a professional Engineering Brief containing sections for 'Live Situation', 'Satellite Assessment', and 'Risk Profile'. Never return raw database records or unformatted logs."
        )
        
        messages = [
            SystemMessage(content=system_prompt), 
            HumanMessage(content=user_input)
        ]
        
        # Main execution loop
        for _ in range(4):
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                break
                
            for tool_call in response.tool_calls:
                # 🚀 CRUCIAL FIX: Variables are unpacked immediately at the top of the loop
                name = tool_call["name"]
                args = tool_call["args"]
                t_id = tool_call["id"]
                
                print(f"⚡ Orchestrator Action: Directing control to tool '{name}' with variables: {args}")
                
                if name in self.tools_map:
                    tool_output = self.tools_map[name].invoke(args)
                    messages.append(ToolMessage(content=str(tool_output), tool_call_id=t_id))
                else:
                    messages.append(ToolMessage(content=f"Error: Tool {name} is unindexed.", tool_call_id=t_id))

        return {"output": messages[-1].content}


def build_wildfire_agent():
    """Application entry adapter factory."""
    return WildfireAgentExecutor()
