# routes/describe.py
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from datetime import datetime, timezone
import logging

describe_bp = Blueprint('describe', __name__)
logger = logging.getLogger(__name__)

FALLBACK = {
    'title': 'Risk Description Unavailable',
    'description': 'AI analysis temporarily unavailable.',
    'impact': 'Unknown — manual review required.',
    'likelihood': 'unknown', 'category': 'Operational',
    'recommended_owner': 'Risk Manager', 'is_fallback': True
}

@describe_bp.route('/describe', methods=['POST'])
def describe():
    logger.info("Received request at /describe")
    data = request.get_json(silent=True) # silent=True prevents 400 crash
    if not data:
        return jsonify({'error':'Request body must be valid JSON'}), 400
        
    text = data.get('text','').strip()
    if not text:
        return jsonify({'error': 'Field text is required'}), 400
        
    if len(text) < 10:
        return jsonify({'error': 'Input too short (min 10 chars)'}), 400
        
    if len(text) > 3000:
        return jsonify({'error': 'Input too long (max 3000 chars)'}), 400
        
    result = call_groq('describe', text)
    ts = datetime.now(timezone.utc).isoformat()
    
    if result is None:
        logger.warning('Groq call failed, returning fallback response.')
        return jsonify({**FALLBACK, 'generated_at': ts}), 200
        
    return jsonify({**result, 'generated_at': ts}), 200
