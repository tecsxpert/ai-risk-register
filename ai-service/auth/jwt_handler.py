"""
JWT authentication handler for Flask API security.
Implements token generation, validation, and user authentication.
"""

import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


class JWTHandler:
    """Handles JWT token generation, validation, and user authentication."""
    
    @staticmethod
    def generate_token(user_id: str, username: str, role: str = 'user') -> str:
        """
        Generate a JWT token for authenticated user.
        
        Args:
            user_id: Unique user identifier
            username: Username for logging/identification
            role: User role (user, admin)
            
        Returns:
            JWT token string
        """
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'role': role,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            logger.info(f"JWT token generated for user: {username} with role: {role}")
            return token
        except Exception as e:
            logger.error(f"Token generation failed: {str(e)}")
            raise
    
    @staticmethod
    def validate_token(token: str) -> Tuple[bool, Optional[Dict]]:
        """
        Validate and decode JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            Tuple of (is_valid, payload_or_error)
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            logger.info(f"Token validated for user: {payload.get('username')}")
            return True, payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: Token expired")
            return False, {'error': 'Token expired'}
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: Invalid token - {str(e)}")
            return False, {'error': 'Invalid token'}
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return False, {'error': 'Token validation error'}
    
    @staticmethod
    def extract_token_from_header(auth_header: str) -> Optional[str]:
        """
        Extract JWT token from Authorization header.
        
        Args:
            auth_header: Authorization header value
            
        Returns:
            Token string or None if not found
        """
        if not auth_header:
            return None
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.warning("Invalid Authorization header format")
            return None
        
        return parts[1]


def require_jwt(f):
    """
    Decorator to require JWT authentication for endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("Missing Authorization header")
            return jsonify({'error': 'Missing Authorization header', 'status': 'error'}), 401
        
        token = JWTHandler.extract_token_from_header(auth_header)
        if not token:
            logger.warning("Invalid Authorization header format")
            return jsonify({'error': 'Invalid Authorization header', 'status': 'error'}), 401
        
        is_valid, payload = JWTHandler.validate_token(token)
        if not is_valid:
            logger.warning(f"JWT validation failed: {payload}")
            return jsonify(payload), 401
        
        # Store user info in request context
        request.user_id = payload['user_id']
        request.username = payload['username']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(required_role: str):
    """
    Decorator to require specific role for endpoints.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            if not hasattr(request, 'user_role'):
                logger.warning("User role not found in request")
                return jsonify({'error': 'Unauthorized', 'status': 'error'}), 403
            
            if request.user_role != required_role and request.user_role != 'admin':
                logger.warning(f"Access denied for user with role: {request.user_role}")
                return jsonify({'error': 'Insufficient permissions', 'status': 'error'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
