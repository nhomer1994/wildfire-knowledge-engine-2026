# src/agent.py
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from src.config import get_llm
from src.rag.retriever import get_internal_knowledge_tool
from src.rag.web_search import get_web_search_tool

class WildfireAgentExecutor:
    """
    A robust, import-safe agent executor that utilizes LangChain's native 
    tool-binding and a deterministic tool-calling loop.
    """
    def __init__(self):
        print("🧠 Orchestrator: Initialising Robust Agent Core...")
        self.llm = get_llm()
        
        # Pull your pre-configured tools
        self.web_tool = get_web_search_tool()
        self.rag_tool = get_internal_knowledge_tool()
        
        # Map tools into a dictionary for fast lookup routing
        self.tools_map = {
            self.web_tool.name: self.web_tool,
            self.rag_tool.name: self.rag_tool
        }
        
        # Bind the tools directly to the LLM interface
        self.llm_with_tools = self.llm.bind_tools([self.web_tool, self.rag_tool])

    def invoke(self, data_input: dict) -> dict:
        user_input = data_input.get("input", "")
        
        # Establish structural system context instructions
        system_prompt = (
            "You are the Wildfire Intelligence Knowledge Engine for the 2026 European Crisis.\n"
            "You have access to a hybrid tool suite to verify environmental situations:\n"
            "1. Use 'live_web_search' for breaking event counts, heatwaves, or active alerts.\n"
            "2. Use 'internal_knowledge_base' to read official internal documents or historical parameters.\n"
            "When asked about an event, cross-reference ground-level textual updates with physical "
            "observations to provide a comprehensive engineering brief."
        )
        
        # Maintain message memory stream
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        # Execute the tool-calling loop (Max 3 iterations to avoid infinite run cycles)
        for _ in range(3):
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            
            # If the model didn't request a tool call, we have our final text answer
            if not response.tool_calls:
                break
                
            # Process tool calls sequentially
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                print(f"⚡ Agent Action: Triggering tool '{tool_name}' with args: {tool_args}")
                
                if tool_name in self.tools_map:
                    # Execute the matched tool pipeline function
                    tool_output = self.tools_map[tool_name].run(tool_args)
                    # Feed the output back to the model context stream
                    messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_id))
                else:
                    messages.append(ToolMessage(content=f"Error: Tool '{tool_name}' not found.", tool_call_id=tool_id))
                    
        return {"output": messages[-1].content}

def build_wildfire_agent():
    """Application entry adapter factory."""
    return WildfireAgentExecutor()
