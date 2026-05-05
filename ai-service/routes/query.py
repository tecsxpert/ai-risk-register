# I am the /query endpoint. I use RAG to answer user questions about AI risk management.
import logging
import time
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.chroma_client import get_collection, get_model
from services.ai_cache import get_cached, set_cached
from services.response_builder import build_meta, estimate_tokens

logger = logging.getLogger(__name__)
query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query_rag():
    """
    I am my RAG query endpoint.
    1. I check my cache first.
    2. I embed the question and retrieve the top-3 relevant chunks from my ChromaDB.
    3. I generate an answer using Groq with the retrieved context.
    4. I cache the final result.
    """
    data = request.get_json(silent=True)
    if not data or not data.get('text', '').strip():
        return jsonify({"error": "The 'text' field is required."}), 400

    question = data['text'].strip()

    # I'm checking my cache first.
    cached_response = get_cached("query", question)
    if cached_response is not None:
        logger.info("I've served POST /query from my Redis cache.")
        return jsonify(cached_response), 200
    
    try:
        # I'm starting my retrieval process.
        start_time = time.time()
        collection = get_collection()
        model = get_model()
        query_embedding = model.encode(question).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # I'm formatting my retrieved chunks into a single context string.
        context_chunks = results.get('documents', [[]])[0]
        
        # I'm checking if the best match is actually relevant (Distance threshold check)
        distances = results.get('distances', [[]])[0]
        if not context_chunks or (distances and distances[0] > 0.6):
            logger.info(f"I found no relevant documents (Best distance: {distances[0] if distances else 'N/A'}).")
            response_time_ms = (time.time() - start_time) * 1000
            ts = datetime.now(timezone.utc).isoformat()
            return jsonify({
                "answer": "I cannot find any relevant information in my security knowledge base to answer that specific question.",
                "sources": [],
                "is_rag": False,
                "generated_at": ts,
                "meta": build_meta(response_time_ms, False, 1.0, 0)
            }), 200

        context = "\n---\n".join(context_chunks)
        
        # I'm starting my generation phase.
        formatted_input = f"Context:\n{context}\n\nQuestion: {question}"
        
        # I'm calling Groq with a very low temperature (0.1) for maximum factual grounding.
        result = call_groq('query', formatted_input, temperature=0.1)
        response_time_ms = (time.time() - start_time) * 1000
        ts = datetime.now(timezone.utc).isoformat()
        
        if result is None:
            # I'm returning a fallback if my AI service is unavailable.
            response_body = {
                "answer": "My AI service is temporarily unavailable.", 
                "sources": [],
                "generated_at": ts,
                "meta": build_meta(response_time_ms, False, 0.0, 0)
            }
            return jsonify(response_body), 200

        response_body = {
            "answer": result.get("answer", str(result)),
            "sources": results.get("metadatas", [[]])[0],
            "is_rag": True,
            "generated_at": ts,
            "meta": build_meta(
                response_time_ms=response_time_ms,
                cached=False,
                confidence=0.8, # I assume a 0.8 confidence for RAG responses.
                tokens_used=estimate_tokens(str(result))
            )
        }

        # I'm storing the successful answer in my cache.
        set_cached("query", question, response_body)
        
        return jsonify(response_body), 200

    except Exception as e:
        logger.error(f"I hit an error in my /query RAG pipeline: {e}")
        return jsonify({"error": "I failed to process your RAG query."}), 500

