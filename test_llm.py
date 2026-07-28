# test_llm.py
from src.config import get_llm

try:
    # Initialize the robust community wrapper
    llm = get_llm()
    
    # Test text parsing
    print("📡 Testing token transmission and structural parsing...")
    response = llm.invoke("Hello OpenRouter! Confirming connection.")
    
    print("\n--- LangChain Decoded Response ---")
    print(response.content)
    print("----------------------------------\n")
    print("✅ Success! Your plug-and-play LLM engine is fully operational.")

except Exception as e:
    print(f"\n❌ Structural Validation Failed: {str(e)}")
    print("If you see a model_dump error, let me know immediately.")
