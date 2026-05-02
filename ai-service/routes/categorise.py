# I am the /categorise endpoint. I classify a risk item into one of 8 predefined categories.
import logging
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq

logger = logging.getLogger(__name__)
categorise_bp = Blueprint('categorise', __name__)

# The 8 valid categories — any response outside this set is rejected
VALID_CATEGORIES = {
    "FINANCIAL", "OPERATIONAL", "TECHNICAL", "COMPLIANCE",
    "REPUTATIONAL", "STRATEGIC", "SECURITY", "ENVIRONMENTAL"
}

# Fallback response used when Groq is unavailable or returns invalid JSON
FALLBACK_RESPONSE = {
    "category": "OPERATIONAL",
    "confidence": 0.0,
    "reasoning": "Category could not be determined — AI service unavailable. Manual review required.",
    "is_fallback": True
}

@categorise_bp.route('/categorise', methods=['POST'])
def categorise():
    """
    Classify a risk item into one of 8 predefined categories.
    Request body: {"text": "risk item description"}
    Response: {"category": "SECURITY", "confidence": 0.91, "reasoning": "...", "generated_at": "..."}
    """
    # Input validation
    data = request.get_json(silent=True)
    if not data:
        logger.warning("POST /categorise received no JSON body.")
        return jsonify({"error": "Request body must be JSON with a 'text' field."}), 400

    input_text = data.get("text", "").strip()
    if not input_text:
        logger.warning("POST /categorise received empty 'text' field.")
        return jsonify({"error": "Field 'text' is required and must not be empty."}), 400

    if len(input_text) > 5000:
        logger.warning(f"POST /categorise input too long: {len(input_text)} chars.")
        return jsonify({"error": "Field 'text' must not exceed 5000 characters."}), 400

    logger.info(f"Calling Groq for /categorise. Input length: {len(input_text)} chars.")
    # Using 'categorise' key to load 'prompts/categorise_prompt.txt'
    result = call_groq('categorise', input_text, temperature=0.1)

    ts = datetime.now(timezone.utc).isoformat()

    # Handle Groq failure or invalid JSON
    if result is None or not isinstance(result, dict):
        logger.error("Groq returned None or invalid for /categorise. Returning fallback.")
        return jsonify({**FALLBACK_RESPONSE, "generated_at": ts}), 200

    # Validate and normalise response
    category = str(result.get("category", "")).upper()
    confidence = float(result.get("confidence", 0.0))
    reasoning = result.get("reasoning", "")

    if category not in VALID_CATEGORIES:
        logger.warning(f"Groq returned invalid category '{category}'. Defaulting to OPERATIONAL.")
        category = "OPERATIONAL"
        confidence = 0.0

    return jsonify({
        "category": category,
        "confidence": round(min(max(confidence, 0.0), 1.0), 2),
        "reasoning": reasoning,
        "generated_at": ts,
        "is_fallback": False
    }), 200
