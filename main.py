# main.py
import sys
from src.agent import build_wildfire_agent

def run_engine():
    print("=" * 60)
    print("🔥 WILDFIRE KNOWLEDGE ENGINE 2026 ACTIVE CORE ONLINE 🔥")
    print("=" * 60)
    
    try:
        executor = build_wildfire_agent()
        
        # Test query that requires the agent to combine web context with satellite analytics
        user_query = (
            "What is the status of the wildfire crisis around Bordeaux, France right now? "
            "Please check the live situation and calculate the satellite burn severity index "
            "for the forest coordinates spanning: Lon -0.8 to -0.4, Lat 44.4 to 44.7."
        )
        
        print(f"\n📥 User Prompt:\n{user_query}\n")
        print("⚡ Processing Multi-Modal Routing Path...")
        
        response = executor.invoke({"input": user_query})
        
        print("\n" + "=" * 50)
        print("🎯 FINAL DECODED OUTPUT:")
        print("=" * 50)
        print(response["output"])
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Execution Graph Interrupted: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_engine()
