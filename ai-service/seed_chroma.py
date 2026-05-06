import os
import sys

# Add the current directory to sys.path to allow importing services
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from services.ingest_documents import ingest_document
from services.chroma_client import get_collection_count

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge_docs')

def seed():
    print("=== ChromaDB Seeding Script ===")
    
    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"ERROR: Knowledge directory not found at {KNOWLEDGE_DIR}")
        return

    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith('.txt')]
    if not files:
        print("No .txt files found to ingest.")
        return

    print(f"Found {len(files)} documents. Starting ingestion...")
    
    for filename in files:
        file_path = os.path.join(KNOWLEDGE_DIR, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"  Ingesting {filename}...")
            ingest_document(content, filename)
        except Exception as e:
            print(f"  FAILED to ingest {filename}: {e}")

    final_count = get_collection_count()
    print(f"\nSeeding complete. Total chunks in collection: {final_count}")

if __name__ == "__main__":
    seed()
