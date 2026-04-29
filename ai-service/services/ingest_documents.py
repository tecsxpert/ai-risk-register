import uuid
from services.chroma_client import get_collection, get_model

def chunk_text(text, chunk_size=500, overlap=50):
    chunks, start = [], 0
    # I chunk the text here to fit within the context window, keeping a 50 char overlap!
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap # overlap keeps context
    return chunks

def ingest_document(text: str, source_name: str):
    collection = get_collection()
    
    # I am iterating through the chunks, embedding them, and storing them in ChromaDB
    for chunk in chunk_text(text):
        embedding = get_model().encode(chunk).tolist()
        collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{'source': source_name}]
        )
