from flask import Flask, request, jsonify
import os
import logging
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from middleware.sanitizer import sanitize_input, SanitizationError
from routes.ai_routes import ai_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize rate limiter - 30 requests per minute
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["30 per minute"],
    storage_uri="memory://",
    strategy="fixed-window"
)

logger.info("Flask app initialized with rate limiting (30 req/min)")

# Register blueprints
app.register_blueprint(ai_bp)


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses (LOW_002 FIX)"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Server'] = 'SecurityEnhanced/1.0'  # Hide version info
    return response


@app.before_request
def sanitize_request_data():
    """
    Middleware to sanitize incoming request data.
    Strips HTML and detects prompt injection attempts.
    """
    # Only sanitize POST/PUT/PATCH requests with JSON data
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.is_json:
            try:
                data = request.get_json()
                if data:
                    # Check and sanitize specific fields
                    fields_to_sanitize = ['prompt', 'message', 'input', 'query', 'text', 'content']
                    for field in fields_to_sanitize:
                        if field in data and isinstance(data[field], str):
                            try:
                                data[field] = sanitize_input(data[field], check_injection=True)
                                logger.info(f"Field '{field}' sanitized successfully")
                            except SanitizationError as e:
                                logger.warning(f"Sanitization failed for field '{field}': {str(e)}")
                                return jsonify({
                                    "error": "Invalid input detected",
                                    "message": str(e),
                                    "status": "error"
                                }), 400
            except Exception as e:
                logger.error(f"Error sanitizing request: {str(e)}")
                # Continue processing if sanitization has non-critical errors
                pass


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    logger.warning(f"Rate limit exceeded: {str(e)}")
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "You have exceeded the rate limit of 30 requests per minute",
        "status": "error"
    }), 429


@app.errorhandler(400)
def bad_request_handler(e):
    """Handle bad request errors."""
    logger.warning(f"Bad request: {str(e)}")
    return jsonify({
        "error": "Bad request",
        "message": str(e),
        "status": "error"
    }), 400


@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(e)}", exc_info=True)
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "status": "error"
    }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
