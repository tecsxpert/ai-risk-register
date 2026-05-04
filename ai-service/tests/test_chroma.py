# I am testing ChromaDB persistence and retrieval to ensure the RAG pipeline is solid.
import sys
import os

# Add parent dir to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.chroma_client import get_collection, get_model
from services.ingest_documents import ingest_document

def test_chroma_flow():
    print("=== ChromaDB Persistence & Retrieval Test ===")
    
    # 1. Ingest a unique test document
    test_text = "The AI Risk Register uses ChromaDB for retrieving domain knowledge about ISO 27001 compliance."
    source_name = "test_doc_001"
    
    print(f"Ingesting test document: '{test_text}'...")
    ingest_document(test_text, source_name)
    
    # 2. Query for a phrase inside that document
    query_text = "What does the tool use for ISO 27001?"
    print(f"Querying for: '{query_text}'...")
    
    collection = get_collection()
    model = get_model()
    query_embedding = model.encode(query_text).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    
    if not results or not results['documents'][0]:
        print("[FAIL] No results returned from ChromaDB.")
        return False
        
    retrieved_doc = results['documents'][0][0]
    print(f"Retrieved: '{retrieved_doc}'")
    
    if "ISO 27001" in retrieved_doc:
        print("[PASS] Correct document retrieved.")
        return True
    else:
        print("[FAIL] Retrieved document does not match expected content.")
        return False

if __name__ == "__main__":
    success = test_chroma_flow()
    sys.exit(0 if success else 1)
