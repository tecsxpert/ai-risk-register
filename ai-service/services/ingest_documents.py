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
    chunks = chunk_text(text)
    
    # I am collecting all chunks and their embeddings for a single batch insert
    ids = [str(uuid.uuid4()) for _ in chunks]
    embeddings = [get_model().encode(chunk).tolist() for chunk in chunks]
    metadatas = [{'source': source_name} for _ in chunks]
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )
