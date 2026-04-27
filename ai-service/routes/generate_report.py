from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime, timezone
import logging
import json

generate_report_bp = Blueprint('generate_report', __name__)
logger = logging.getLogger(__name__)

FALLBACK = {
    'title': 'Risk Report Unavailable',
    'executive_summary': 'AI analysis temporarily unavailable. Manual review required.',
    'overview': 'Could not process the provided risk items at this time.',
    'top_items': ['Unavailable'],
    'recommendations': ['Please review the risk items manually.', 'Try generating the report again later.'],
    'is_fallback': True
}

@generate_report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    logger.info("Received request at /generate-report")
    data = request.get_json(silent=True) # silent=True prevents 400 crash
    if not data:
        return jsonify({'error':'Request body must be valid JSON'}), 400
        
    items = data.get('items', [])
    if not items or not isinstance(items, list):
        return jsonify({'error': 'Field items is required and must be a non-empty list'}), 400
        
    # Formatting the input list into a readable string for the LLM
    text_input = "\n".join([f"- {str(item)}" for item in items])
        
    result = call_groq('generate_report', text_input)
    ts = datetime.now(timezone.utc).isoformat()
    
    if result is None:
        logger.warning('Groq call failed, returning fallback response.')
        return jsonify({**FALLBACK, 'generated_at': ts}), 200
        
    return jsonify({**result, 'generated_at': ts}), 200
