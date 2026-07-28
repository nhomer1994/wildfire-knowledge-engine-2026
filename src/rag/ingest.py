# src/rag/ingest.py
import os
from langchain_core.documents import Document

def load_wildfire_reports():
    """
    Reads the local 2026 wildfire crisis report data 
    and converts it into standard LangChain Document structures.
    """
    file_path = "data/sample_reports/wildfires_2026.txt"
    
    # Check if the folder and file exist to prevent crash loops
    if not os.path.exists(file_path):
        print(f"⚠️ RAG Ingest Warning: Sample file not found at {file_path}. Creating an empty library.")
        return []
        
    print(f"📚 RAG Ingest: Loading situation updates from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    # Split the file into separate reports based on the blank lines between them
    raw_reports = raw_text.strip().split("\n\n")
    documents = []
    
    for report in raw_reports:
        if not report.strip():
            continue
            
        # Parse the region name from the text to use as helpful metadata
        lines = report.split("\n")
        region = "Unknown Region"
        for line in lines:
            if line.startswith("Region:"):
                region = line.replace("Region:", "").strip()
                break
                
        # Build the structured document asset
        doc = Document(
            page_content=report,
            metadata={"source": "EFFIS Mock Feed", "region": region}
        )
        documents.append(doc)
        
    print(f"✅ RAG Ingest Success: Formatted {len(documents)} context document layers.")
    return documents
