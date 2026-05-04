import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# I am importing my blueprints here
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp
from routes.categorise import categorise_bp
from routes.query import query_bp
from services.chroma_client import get_model
from services.sanitiser import sanitise_text
from services.ingest_documents import ingest_document

# I need to ensure load_dotenv() is called at the very top before any os.getenv() calls
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_app():
    # Setting up the Flask application instance
    app = Flask(__name__)
    
    # I am setting up the limiter to restrict the number of requests to 30 per minute, backed by Redis
    limiter = Limiter(
        get_remote_address, app=app,
        default_limits=['30 per minute'],
        # Commenting out Redis for local dev since Docker isn't running!
        # storage_uri=os.getenv('REDIS_URL', 'redis://localhost:6379')
    )
    
    # Registering my blueprints so the routes are available
    app.register_blueprint(describe_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(generate_report_bp)
    app.register_blueprint(categorise_bp)
    app.register_blueprint(query_bp)

    # Global input sanitisation hook
    @app.before_request
    def sanitise_all_inputs():
        if request.method in ('POST', 'PUT'):
            data = request.get_json(silent=True)
            if not data:
                return
            
            def check_for_injection(obj):
                if isinstance(obj, str):
                    cleaned, is_injection = sanitise_text(obj)
                    if is_injection:
                        return True
                elif isinstance(obj, list):
                    for item in obj:
                        if check_for_injection(item):
                            return True
                elif isinstance(obj, dict):
                    for val in obj.values():
                        if check_for_injection(val):
                            return True
                return False

            if check_for_injection(data):
                return jsonify({
                    "error": "Invalid input detected. Request blocked.",
                    "code": "INJECTION_DETECTED"
                }), 400
    
    # I am pre-loading the SentenceTransformer model at startup so the first request isn't terribly slow!
    get_model()
    
    @app.route('/health')
    def health():
        # A simple health check to tell if my service is running correctly
        return {'status': 'ok'}, 200

    @app.route('/ingest', methods=['POST'])
    def ingest():
        """
        Ingest a document into the ChromaDB vector store.
        Request body: {"text": "doc content", "source": "doc_name"}
        """
        data = request.get_json(silent=True)
        if not data or not data.get('text'):
            return jsonify({"error": "Field 'text' is required."}), 400
        
        text = data['text']
        source = data.get('source', 'unknown_source')
        
        try:
            ingest_document(text, source)
            return jsonify({"message": "Document ingested successfully.", "status": "success"}), 201
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            return jsonify({"error": str(e)}), 500
        
    return app

if __name__ == '__main__':
    app = create_app()
    # threaded=True allows Flask to handle multiple concurrent requests from the Java backend
    # In Docker/production, gunicorn handles this instead (see Dockerfile CMD)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
