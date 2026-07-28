# src/rag/retriever.py
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from src.rag.ingest import load_wildfire_reports

def initialize_vector_retriever():
    """
    Initialises an in-memory vector space using free local embeddings
    and populates it with our 2026 wildfire crisis documents.
    """
    print("🧠 RAG Engine: Spinning up local Hugging Face embedding vector nodes...")
    # This open-source model executes completely free inside your cloud container
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Instantiate the transient memory database grid
    vector_store = InMemoryVectorStore(embeddings)
    
    # Load our processed text documents
    docs = load_wildfire_reports()
    
    if docs:
        print("📥 RAG Engine: Matrix indexing documents into memory vectors...")
        vector_store.add_documents(docs)
        
    return vector_store.as_retriever(search_kwargs={"k": 1})

# Initialize the underlying retriever instance once to save memory
_retriever_instance = initialize_vector_retriever()

@tool("internal_knowledge_base")
def get_internal_knowledge_tool(query: str) -> str:
    """
    Use this tool to search internal official situation reports, 
    archived crisis declarations, operational agency briefs, and local 
    baseline data for the 2026 European wildfire events. 
    Input should be a simple keyword search query string focusing on location names.
    """
    # Execute the text matrix lookup matching user query strings
    matched_docs = _retriever_instance.invoke(query)
    
    # Unpack and combine the results into a clean string string for the LLM
    if not matched_docs:
        return "No matching internal records discovered for this query location."
        
    return "\n\n".join([doc.page_content for doc in matched_docs])
