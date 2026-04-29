from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

recommend_bp = Blueprint('recommend', __name__)

FALLBACK_LIST = [
    {
        "action_type": "Mitigate",
        "description": "Fallback: Review the risk details manually and apply standard mitigation procedures.",
        "priority": "medium"
    },
    {
        "action_type": "Accept",
        "description": "Fallback: Acknowledge the risk temporarily until the system recovers.",
        "priority": "low"
    },
    {
        "action_type": "Avoid",
        "description": "Fallback: Escalate to management to prevent further exposure.",
        "priority": "high"
    }
]

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(silent=True)
    if not data or not data.get('text', '').strip():
        return jsonify({'error': 'Field text is required'}), 400
    
    # I am calling Groq with temperature 0.5 for slightly creative recommendations!
    result = call_groq('recommend', data['text'].strip(), temperature=0.5)
    
    # I am falling back gracefully if the API fails or doesn't return a list
    if result is None or not isinstance(result, list):
        return jsonify({
            'recommendations': FALLBACK_LIST,
            'is_fallback': True
        }), 200
        
    # I always slice result[:3] to enforce the max 3 items API contract!
    return jsonify({
        'recommendations': result[:3],
        'is_fallback': False
    }), 200
