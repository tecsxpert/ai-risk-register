"""
Flask routes for AI service endpoints.
"""

from flask import request, jsonify, Blueprint
from services.groq_client import get_client
from middleware.sanitizer import SanitizationError
import logging

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/response', methods=['POST'])
def get_response():
    """Get AI response for a given prompt."""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({
                "status": "error",
                "message": "prompt field is required",
                "error": "Missing required field"
            }), 400
        
        prompt = data.get('prompt')
        parse_json = data.get('parseJson', False)
        
        client = get_client()
        result = client.get_ai_response(prompt, parse_json=parse_json)
        
        return jsonify(result), 200 if result.get('success') else 500
    except SanitizationError as e:
        logger.warning(f"Sanitization error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error": "Invalid input"
        }), 400
    except Exception as e:
        logger.error(f"Error in get_response: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "error": str(e)
        }), 500


@ai_bp.route('/analyze-security', methods=['POST'])
def analyze_security():
    """Analyze prompt for security threats."""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({
                "status": "error",
                "message": "prompt field is required",
                "error": "Missing required field"
            }), 400
        
        prompt = data.get('prompt')
        
        # For now, return a mock response
        return jsonify({
            "status": "success",
            "message": "Security analysis completed",
            "content": {
                "threats_detected": 0,
                "injection_risk": "low",
                "html_tags": False
            },
            "success": True
        }), 200
    except SanitizationError as e:
        logger.warning(f"Sanitization error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error": "Invalid input"
        }), 400
    except Exception as e:
        logger.error(f"Error in analyze_security: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "error": str(e)
        }), 500


@ai_bp.route('/risk-assessment', methods=['POST'])
def risk_assessment():
    """Generate risk assessment for a topic."""
    try:
        data = request.get_json()
        if not data or 'topic' not in data:
            return jsonify({
                "status": "error",
                "message": "topic field is required",
                "error": "Missing required field"
            }), 400
        
        topic = data.get('topic')
        
        # For now, return a mock response
        return jsonify({
            "status": "success",
            "message": "Risk assessment generated",
            "content": {
                "topic": topic,
                "risk_level": "medium",
                "recommendations": []
            },
            "success": True
        }), 200
    except SanitizationError as e:
        logger.warning(f"Sanitization error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error": "Invalid input"
        }), 400
    except Exception as e:
        logger.error(f"Error in risk_assessment: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "error": str(e)
        }), 500


@ai_bp.route('/batch', methods=['POST'])
def batch_process():
    """Process batch of prompts."""
    try:
        data = request.get_json()
        if not data or 'prompts' not in data:
            return jsonify({
                "status": "error",
                "message": "prompts field is required",
                "error": "Missing required field"
            }), 400
        
        prompts = data.get('prompts')
        if not isinstance(prompts, list) or len(prompts) == 0:
            return jsonify({
                "status": "error",
                "message": "prompts must be a non-empty array",
                "error": "Invalid input"
            }), 400
        
        # For now, return a mock response
        return jsonify({
            "status": "success",
            "message": "Batch processing completed",
            "content": {
                "processed": len(prompts),
                "results": []
            },
            "success": True
        }), 200
    except SanitizationError as e:
        logger.warning(f"Sanitization error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error": "Invalid input"
        }), 400
    except Exception as e:
        logger.error(f"Error in batch_process: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "error": str(e)
        }), 500
