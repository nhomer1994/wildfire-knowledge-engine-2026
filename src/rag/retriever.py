# src/rag/retriever.py
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import Tool
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

def get_internal_knowledge_tool():
    """
    Wraps the vector database retriever as a LangChain Tool asset
    so the routing agent can evaluate and execute it.
    """
    retriever = initialize_vector_retriever()
    
    internal_tool = Tool(
        name="internal_knowledge_base",
        description=(
            "Use this tool to search internal official situation reports, "
            "archived crisis declarations, operational agency briefs, and local "
            "baseline data for the 2026 European wildfire events. "
            "Input should be a simple search query string focusing on locations."
        ),
        # Lambda wrapper allows standard text strings to pass directly into the vector invoke query
        func=lambda query: "\n\n".join([doc.page_content for doc in retriever.invoke(query)])
    )
    
    return internal_tool
