# I am the /query endpoint. I use RAG to answer user questions about AI risk management.
import logging
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.chroma_client import get_collection, get_model

logger = logging.getLogger(__name__)
query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query_rag():
    """
    RAG query endpoint.
    1. Embed the question.
    2. Retrieve top-3 chunks from ChromaDB.
    3. Generate answer using Groq with retrieved context.
    """
    data = request.get_json(silent=True)
    if not data or not data.get('text', '').strip():
        return jsonify({"error": "Field 'text' is required."}), 400

    question = data['text'].strip()
    
    try:
        # 1. Retrieval
        collection = get_collection()
        model = get_model()
        query_embedding = model.encode(question).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # Format the retrieved chunks into a single context string
        context_chunks = results.get('documents', [[]])[0]
        context = "\n---\n".join(context_chunks) if context_chunks else "No relevant context found."
        
        # 2. Generation
        # I construct the 'user_input' to fit into my prompt template's {user_input} placeholder
        formatted_input = f"Context:\n{context}\n\nQuestion: {question}"
        
        # Note: 'query' key loads 'prompts/query_prompt.txt'
        # call_groq expects a dict, but query returns plain text. 
        # I'll handle plain text response if groq_client returns it.
        # Wait, existing groq_client always tries to json.loads().
        # I'll update query_prompt.txt to return JSON for consistency!
        
        result = call_groq('query', formatted_input, temperature=0.2)
        
        if result is None:
            return jsonify({"answer": "AI service temporarily unavailable.", "sources": []}), 200

        # If call_groq returns a dict (which it does), I'll just return it
        # But I should ensure the prompt asks for JSON.
        
        return jsonify({
            "answer": result.get("answer", str(result)),
            "sources": results.get("metadatas", [[]])[0],
            "is_rag": True
        }), 200

    except Exception as e:
        logger.error(f"Error in /query RAG pipeline: {e}")
        return jsonify({"error": "Failed to process RAG query."}), 500
